# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


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
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BlinkData(models.Model):
    id = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id', primary_key=True)
    b_time = models.DateTimeField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'blink_data'
        unique_together = (('id', 'b_time'),)


class DailyTodo(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    username = models.CharField(max_length=150)
    starttime = models.DateTimeField()
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'daily_todo'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DrowsinessData(models.Model):
    id = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id', primary_key=True)
    d_time = models.DateTimeField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'drowsiness_data'
        unique_together = (('id', 'd_time'),)


class Freeboard(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    register_date = models.DateTimeField()
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

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()


class CommentQuestionboard(models.Model):
    pid = models.OneToOneField('Questionboard', models.DO_NOTHING, db_column='pid', primary_key=True)
    uid = models.IntegerField()
    created_date = models.DateTimeField()
    comments = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'comment_questionboard'
        unique_together = (('pid', 'uid', 'created_date'),)
