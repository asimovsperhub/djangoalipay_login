# Generated by Django 3.0.4 on 2020-03-27 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('nike_name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=5)),
                ('province', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('avatar', models.CharField(max_length=200)),
                ('phone', models.IntegerField(max_length=11)),
                ('emial', models.EmailField(max_length=50)),
            ],
        ),
    ]