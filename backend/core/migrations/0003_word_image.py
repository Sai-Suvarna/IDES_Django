# Generated by Django 4.1.3 on 2024-06-03 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_word_delete_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='word_images/'),
        ),
    ]