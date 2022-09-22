from base64 import urlsafe_b64decode
from django.http import HttpResponse
from django.shortcuts import redirect, render
from accounts.utils import send_verfication_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

from .forms import UserForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied


# Create your views here.


def registerUser(request):
    # if request.user.is_authenticated:
    #     messages.warning(request, "You already logged in!")
    #     return redirect('team_dashboard')
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(password)
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = form.cleaned_data['role']
            user.save()

            # Send Verfication Email
            mail_subject = "Please activate your account"
            email_template = 'accounts/emails/account_verfication_email.html'
            send_verfication_email(request, user, mail_subject, email_template)
            messages.success(
                request, "Your Account Has Been Registered Sucessfully")
            return redirect('registerUser')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def login(request):
    if request.method == 'POST':
        # Get Form Data
        email = request.POST['email']
        password = request.POST['password']

        # Check to see if email/password exist
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are logged in")
            print("SUCCESS")
            return redirect('team_dashboard')
        else:
            messages.error(request, "Invalid Login")
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out")
    return redirect('login')


def team_dashboard(request):
    return render(request, 'accounts/team_dashboard.html')


def activate(request, uidb64, token):
    # Activate the user by setting the is_active status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! Your account is activated.')
        return redirect('request_password')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            # Get the user id from the session of whos password needs reset
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, "Password has been reset")
            return redirect('login')
        else:
            messages.error(request, "Password Do Not Match")
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')


def request_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)

            # Send reset password email
            mail_subject = "Reset Your Password"
            email_template = "accounts/emails/reset_password_email.html"
            send_verfication_email(request, user, mail_subject, email_template)

            messages.success(
                request, "Password Reset Link Has Been Sent to Your Email Address")
            return redirect('login')
        else:
            messages.error(
                request, "Account Does Not Exist")
            return redirect('forgot_password')
    return render(request, 'accounts/request_password.html')


def reset_password_validate(request, uidb64, token):
    # Validate the user by decoding the token and the user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, "Please reset your password")
        return redirect('reset_password')
    else:
        messages.error(request, "This Link Has Expired")
        return redirect('login')
