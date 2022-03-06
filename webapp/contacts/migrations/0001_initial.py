# Generated by Django 4.0.2 on 2022-03-06 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('diocese', models.CharField(max_length=100)),
                ('sexe', models.CharField(max_length=100)),
                ('person_contacter_name', models.CharField(max_length=100)),
                ('paroisse', models.CharField(max_length=100)),
                ('person_contacter_phone', models.CharField(max_length=100)),
            ],
        ),
    ]