# Generated by Django 4.1 on 2022-08-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_activity', '0002_alter_timer_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previoustimers',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
