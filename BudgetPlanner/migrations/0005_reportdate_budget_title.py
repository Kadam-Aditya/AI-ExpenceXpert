# Generated by Django 4.2.4 on 2024-01-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BudgetPlanner', '0004_reportdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportdate',
            name='budget_title',
            field=models.CharField(default='NULL', max_length=50),
        ),
    ]
