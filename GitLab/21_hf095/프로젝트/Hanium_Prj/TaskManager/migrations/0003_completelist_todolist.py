# Generated by Django 3.1.7 on 2021-08-17 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TaskManager', '0002_commentfreeboard_commentquestionboard'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompleteList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True, null=True)),
                ('end_date', models.TextField(db_column='END_DATE')),
                ('end_time', models.TextField(db_column='END_TIME')),
            ],
            options={
                'db_table': 'complete_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('content', models.TextField(blank=True)),
                ('reg_time', models.TextField(blank=True, db_column='reg_time', null=True)),
                ('reg_date', models.TextField(blank=True, db_column='reg_date', null=True)),
            ],
            options={
                'db_table': 'todo_list',
                'managed': False,
            },
        ),
    ]
