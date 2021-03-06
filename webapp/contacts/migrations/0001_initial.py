# Generated by Django 4.0.2 on 2022-03-12 17:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dortoires', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=20)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=100)),
                ('diocese', models.CharField(max_length=100)),
                ('sexe', models.CharField(max_length=100)),
                ('person_contacter_name', models.CharField(max_length=100)),
                ('paroisse', models.CharField(max_length=100)),
                ('person_contacter_phone', models.CharField(max_length=100)),
                ('allergies', models.CharField(max_length=255, null=True)),
                ('groupe_sanguin', models.CharField(max_length=3, null=True)),
                ('maladies', models.CharField(max_length=500, null=True)),
                ('produit', models.BooleanField(default=False)),
                ('create_date', models.DateField(default=datetime.date.today)),
                ('createat', models.DateTimeField(default=datetime.datetime.now)),
                ('dortoir', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dortoires.dortoire')),
            ],
        ),
    ]
