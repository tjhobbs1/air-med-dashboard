# Generated by Django 4.1 on 2022-11-17 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication_board', '0002_alter_flight_table'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Flight',
            new_name='Communication_Board',
        ),
        migrations.AlterModelTable(
            name='communication_board',
            table=None,
        ),
    ]