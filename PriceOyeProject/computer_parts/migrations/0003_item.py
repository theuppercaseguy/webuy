# Generated by Django 5.0.2 on 2024-02-25 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computer_parts', '0002_customuser_is_verified'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('tags', models.CharField(max_length=100)),
                ('image_location', models.CharField(max_length=200)),
                ('url', models.URLField()),
            ],
        ),
    ]