# Generated by Django 4.1.5 on 2023-01-11 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to=''),
        ),
    ]
