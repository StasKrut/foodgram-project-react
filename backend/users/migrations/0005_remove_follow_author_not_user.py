# Generated by Django 3.2.16 on 2022-12-23 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221223_1251'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='author_not_user',
        ),
    ]