# Generated by Django 5.0 on 2024-03-31 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_user_fields_user_skill'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='job_seeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.city')),
                ('exp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic.exp')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
