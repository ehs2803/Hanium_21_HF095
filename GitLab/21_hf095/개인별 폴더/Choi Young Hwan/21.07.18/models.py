# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


# Create your models here.
class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class BlinkData(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    b_time = models.DateTimeField()
    b_count = models.IntegerField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'blink_data'


class DrowsinessData(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    d_time = models.DateTimeField()
    d_count = models.IntegerField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'drowsiness_data'


class Freeboard(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField()
    hits = models.IntegerField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'freeboard'


class Questionboard(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField()
    hits = models.IntegerField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'questionboard'


class DailyTodo(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    username = models.CharField(max_length=150)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    content = models.TextField(blank=True, null=True)
    is_complete = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'daily_todo'
