# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class AccountsUser(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     password = models.CharField(max_length=128)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     username = models.CharField(unique=True, max_length=50)
#     email = models.CharField(unique=True, max_length=100)
#     phone_number = models.CharField(max_length=12)
#     role = models.SmallIntegerField(blank=True, null=True)
#     date_joined = models.DateTimeField()
#     last_login = models.DateTimeField()
#     created_date = models.DateTimeField()
#     modified_date = models.DateTimeField()
#     is_admin = models.BooleanField()
#     is_staff = models.BooleanField()
#     is_active = models.BooleanField()
#     is_superadmin = models.BooleanField()

#     class Meta:
#         managed = False
#         db_table = 'accounts_user'


class Airmedflights(models.Model):
    transport_date = models.CharField(max_length=100, blank=True, null=True)
    flight_num = models.CharField(primary_key=True, max_length=50)
    base = models.CharField(max_length=100, blank=True, null=True)
    hour = models.IntegerField()
    flight_date = models.CharField(max_length=100, blank=True, null=True)
    flight_month = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=100, blank=True, null=True)
    call_sign = models.CharField(max_length=250, blank=True, null=True)
    vehicle = models.CharField(max_length=100, blank=True, null=True)
    call_type = models.CharField(max_length=250, blank=True, null=True)
    initial_priority = models.CharField(max_length=100, blank=True, null=True)
    outcome = models.CharField(max_length=100, blank=True, null=True)
    final_disposition = models.CharField(max_length=250, blank=True, null=True)
    primary_cancel_reason_for_miss = models.CharField(
        max_length=250, blank=True, null=True)
    secondary_cancel_reason_for_miss = models.CharField(
        max_length=250, blank=True, null=True)
    referrer_name = models.CharField(
        max_length=350, blank=True, null=True)
    requesting_agency = models.CharField(
        max_length=350, blank=True, null=True)
    pickup_location = models.CharField(
        max_length=350, blank=True, null=True)
    pickup_zip = models.IntegerField()
    pickup_county = models.CharField(
        max_length=350, blank=True, null=True)
    pickup_state = models.CharField(
        max_length=10, blank=True, null=True)
    pickup_lat = models.DecimalField(max_digits=20, decimal_places=15)
    pickup_long = models.DecimalField(max_digits=20, decimal_places=15)
    delorme_lat = models.CharField(
        max_length=100, blank=True, null=True)
    delorme_long = models.CharField(
        max_length=100, blank=True, null=True)
    receiving_agency = models.CharField(max_length=250, blank=True, null=True)
    dropoff_location = models.CharField(max_length=250, blank=True, null=True)
    call_start_time = models.CharField(max_length=250, blank=True, null=True)
    standby_time = models.CharField(max_length=250, blank=True, null=True)
    end_standby_time = models.CharField(max_length=250, blank=True, null=True)
    launch_page_time = models.CharField(max_length=250, blank=True, null=True)
    dispatch_time = models.CharField(max_length=250, blank=True, null=True)
    flight_accepted_time = models.CharField(
        max_length=250, blank=True, null=True)
    depart_base = models.CharField(max_length=250, blank=True, null=True)
    arrive_pt_location = models.CharField(
        max_length=250, blank=True, null=True)
    depart_pt_on_board = models.CharField(
        max_length=250, blank=True, null=True)
    depart_receiving_facility = models.CharField(
        max_length=250, blank=True, null=True)
    arrive_at_base = models.CharField(
        max_length=250, blank=True, null=True)
    cancel_time = models.CharField(
        max_length=250, blank=True, null=True)
    pilot = models.CharField(
        max_length=300, blank=True, null=True)
    medical_1 = models.CharField(
        max_length=300, blank=True, null=True)
    medical_2 = models.CharField(
        max_length=300, blank=True, null=True)
    medical_3 = models.CharField(
        max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'airmedflights'
        app_label = 'flight_data'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.SmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AccountsUser, models.DO_NOTHING)

#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = False
#         db_table = 'django_session'


# class Flight(models.Model):
#     transport_date = models.DateTimeField()
#     flight_num = models.CharField(primary_key=True, max_length=100)
#     base = models.CharField(max_length=100)

#     class Meta:
#         managed = False
#         db_table = 'flight'


# class Test(models.Model):
#     sname = models.CharField(max_length=50, blank=True, null=True)
#     roll_num = models.IntegerField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'test'
