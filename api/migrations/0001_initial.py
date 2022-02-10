# Generated by Django 4.0.2 on 2022-02-09 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('created_by', models.CharField(max_length=64)),
                ('confirmed', models.BooleanField(default=False)),
                ('budget', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TripUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.PositiveIntegerField(default=None)),
                ('end_date', models.PositiveIntegerField(default=None)),
                ('budget', models.PositiveIntegerField(default=None)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.trip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='trip',
            name='users',
            field=models.ManyToManyField(through='api.TripUser', to='api.User'),
        ),
    ]
