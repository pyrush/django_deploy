# Generated by Django 3.2.6 on 2021-08-28 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Creation Date and Time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='Modification Date and Time')),
                ('name', models.CharField(max_length=51, verbose_name='Name')),
                ('image', models.ImageField(upload_to='images', verbose_name='image')),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name': 'Image',
                'verbose_name_plural': 'Images',
            },
        ),
        migrations.DeleteModel(
            name='DumyModel',
        ),
    ]
