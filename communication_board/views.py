from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Communication_Board
from .forms import CommunicationAdminForm
import datetime


def board_admin(request):
    form = CommunicationAdminForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            communication = Communication_Board()

            communication.date_opened = form.cleaned_data['date_opened']
            communication.base = form.cleaned_data['base']
            communication.issue_category = form.cleaned_data['issue_category']
            communication.transport_related = form.cleaned_data['transport_related']
            communication.reported_issue = form.cleaned_data['reported_issue']
            communication.reported_by_person1 = form.cleaned_data['reported_by_person1']
            communication.reported_by_person2 = form.cleaned_data['reported_by_person2']
            communication.issue_status = form.cleaned_data['issue_status']
            communication.follow_up_information = form.cleaned_data['follow_up_information']
            communication.assigned_to_person1 = form.cleaned_data['assigned_to_person1']
            communication.assigned_to_person2 = form.cleaned_data['assigned_to_person2']
            communication.updated = datetime.datetime.now()
            communication.date_closed = form.cleaned_data['date_closed']

            communication.save()

            return redirect('success')
        else:
            return render(request, 'communication_board/board_admin.html', {"form": form, 'error': 'Everything is required'})
    context = {
        'form': form
    }
    return render(request, 'communication_board/board_admin.html', context)


def board(request):
    get_day_of_week = (datetime.datetime.now()).isoweekday()
    print(get_day_of_week)
    objects = Communication_Board.objects.all()
    context = {
        'objects': objects,
        'date': get_day_of_week
    }
    return render(request, 'communication_board/board.html', context)


def success(request):
    return render(request, 'communication_board/success.html')
