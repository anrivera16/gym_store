# Generated by Django 3.2.5 on 2021-08-06 12:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text="Your employee's name.", max_length=100)),
                ('department', models.CharField(choices=[('hr', 'Human Resources'), ('finance', 'Finance'), ('engineering', 'Engineering'), ('marketing', 'Marketing'), ('sales', 'Sales')], help_text='What department your employee belongs to.', max_length=20)),
                ('salary', models.PositiveIntegerField(help_text="Your employee's annual salary.")),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]