# Generated by Django 5.0 on 2024-04-01 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0006_job_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='description',
            field=models.CharField(default='no', max_length=250),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='job_desc',
        ),
    ]
