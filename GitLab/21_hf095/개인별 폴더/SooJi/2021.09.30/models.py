# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models


# Create your models here.
# 사용자(User) 모델
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
    date_joined = models.DateTimeField(auto_now_add=True, blank=True, null=False)

    class Meta:
        managed = False
        db_table = 'auth_user'


# 눈 깜빡임 통계 데이터 테이블
class BlinkData(models.Model):
    id = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id', primary_key=True)
    b_time = models.DateTimeField(null=False)
    username = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'blink_data'
        unique_together = (('id', 'b_time'),)


# 졸음 통계 데이터 테이블
class DrowsinessData(models.Model):
    id = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='id', primary_key=True)
    d_time = models.DateTimeField(null=False)
    username = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drowsiness_data'
        unique_together = (('id', 'd_time'),)


# 자유게시판 테이블
class Freeboard(models.Model):
    uid = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True, null=False)
    hits = models.IntegerField(null=False, default=0)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'freeboard'

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()


# 질문게시판 테이블
class Questionboard(models.Model):
    uid = models.OneToOneField(AuthUser, models.DO_NOTHING, db_column='uid')
    title = models.CharField(max_length=120)
    contents = models.TextField()
    registered_date = models.DateTimeField(auto_now_add=True, null=False)
    hits = models.IntegerField(null=False, default=0)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'questionboard'

    @property
    def increase_hits(self):
        self.hits += 1
        self.save()


# 자유게시판 댓글 테이블
class CommentFreeboard(models.Model):
    pid = models.OneToOneField(Freeboard, models.DO_NOTHING, db_column='pid', primary_key=True)
    uid = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    comments = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'comment_freeboard'
        unique_together = (('pid', 'uid', 'created_date'),)


# 질문게시판 댓글 테이블
class CommentQuestionboard(models.Model):
    pid = models.OneToOneField(Questionboard, models.DO_NOTHING, db_column='pid', primary_key=True)
    uid = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, null=False)
    comments = models.TextField()
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'comment_questionboard'
        unique_together = (('pid', 'uid', 'created_date'),)

# To Do 테이블
class TodoList(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    username = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=False)
    reg_time = models.TextField(db_column='reg_time', blank=True, null=True)
    reg_date = models.TextField(db_column='reg_date', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'todo_list'

# CompleteTodo 테이블
class CompleteList(models.Model):
    uid = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uid')
    username = models.CharField(max_length=150)
    content = models.TextField(blank=True, null=True)
    end_date = models.TextField(db_column='END_DATE', null=False)  # Field name made lowercase.
    end_time = models.TextField(db_column='END_TIME', null=False)  # Field name made lowercase.
    tid = models.IntegerField(db_column='tid', null=True)

    class Meta:
        managed = False
        db_table = 'complete_list'