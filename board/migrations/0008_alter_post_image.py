# Generated by Django 4.1 on 2022-12-21 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='uploads'),
        ),
    ]
