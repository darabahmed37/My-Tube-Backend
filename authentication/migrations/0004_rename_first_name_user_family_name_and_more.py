# Generated by Django 4.0.6 on 2022-08-01 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_rename_openid_user_id_rename_imageurl_user_picture_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='family_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='last_name',
            new_name='given_name',
        ),
    ]