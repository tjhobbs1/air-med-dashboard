# Generated by Django 4.1 on 2022-11-17 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication_board', '0005_alter_communication_board_date_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communication_board',
            name='date_closed',
            field=models.DateField(blank=True, null=True),
        ),
    ]
