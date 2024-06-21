from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CASCADE

# Create your models here.
 
class User(AbstractUser):
    ADMIN = 'ADMIN'
    SUPER_ADMIN = 'SUPER_ADMIN'
   

    USER_TYPE_CHOICE = (
        (ADMIN, 'ADMIN'),
        (SUPER_ADMIN, 'SUPER_ADMIN'),
    )

    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICE, default=ADMIN)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=40)

    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Django-Admin Users'

    def __str__(self):
        return self.username
    
class ApplicationUser(models.Model): 
    ORACLE = 'ORACLE'
    POSTGRES = 'POSTGRES'
    MYSQL = 'MYSQL'
    DATABASE_CHOICES = (
        (ORACLE,'ORACLE'),
        (POSTGRES, 'POSTGRES'),
        (MYSQL, 'MYSQL')
    )

    id = models.AutoField(primary_key=True, unique=True)
    ussername = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    user_type = models.CharField(max_length = 200)
    db_type = models.CharField(max_length = 200, choices=DATABASE_CHOICES)
    db_name = models.CharField(max_length = 200, default='db')
    db_username = models.CharField(max_length = 200, default='usr')
    db_password = models.CharField(max_length = 200, default='pwd')
    db_hostname = models.CharField(max_length = 200, default='localhost')
    db_uri = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
       
    class Meta:
        db_table = 'application_users'
        verbose_name = 'Application Users'
        verbose_name_plural = 'Application Users'
        
    def __str__(self):
        return f'{self.id}'
        
class ReportMaster(models.Model):
    report_id = models.AutoField(primary_key=True, unique=True)
    report_name = models.CharField(max_length = 200)
    column_list = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    
    class Meta:
        db_table = 'report_master'
        verbose_name = 'Report Master'
        verbose_name_plural = 'Report Master'

    def __str__(self):
        return f'{self.report_id}'
    
class ReportUserMapping(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, db_constraint=False, null=True, blank=True)
    report = models.ForeignKey(ReportMaster, on_delete=models.SET_NULL, db_constraint=False, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    
    class Meta:
        db_table = 'report_user_mapping'
        verbose_name = 'Report User Mapping'
        verbose_name_plural = 'Report User Mapping'

    def __str__(self):
        return f'{self.id}'
    
class TableRelationMaster(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    schema = models.CharField(max_length = 200, null=True, blank=True)
    appuserid = models.ForeignKey(ApplicationUser, on_delete=models.SET_NULL, db_constraint=False, null=True, blank=True)
    table_name = models.CharField(max_length = 200, null=True, blank=True)
    column_name = models.CharField(max_length = 200, null=True, blank=True)
    foreign_table_name = models.CharField(max_length = 200, null=True, blank=True)
    foreign_column_name = models.CharField(max_length = 200, null=True, blank=True)
    child_data_type = models.CharField(max_length = 200, null=True, blank=True)
    parent_data_type = models.CharField(max_length = 200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    updated_by = models.ForeignKey(User, null=True, blank=True, on_delete=CASCADE, related_name='+')
    
    class Meta:
        db_table = 'table_relation_master'
        verbose_name = 'Table Relation Master'
        verbose_name_plural = 'Table Relations Master'

    def __str__(self):
        return f'{self.id}'
    

    