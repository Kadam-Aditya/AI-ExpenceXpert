# Generated by Django 4.2.4 on 2024-01-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0002_userpreference_goal_userpreference_risk'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpreference',
            name='goal',
        ),
        migrations.RemoveField(
            model_name='userpreference',
            name='risk',
        ),
        migrations.AddField(
            model_name='userpreference',
            name='investment_goal',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='userpreference',
            name='risk_preference',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
