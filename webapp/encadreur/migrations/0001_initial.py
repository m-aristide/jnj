# Generated by Django 4.0.2 on 2022-05-11 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CodeEncadreur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True, unique=True)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
