from django.contrib import admin
from .models import ApplicationUser, ReportMaster, ReportUserMapping, User, TableRelationMaster
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.

@admin.register(User)
class UserModelAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'user_type', 'name', 'phone_number')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(ApplicationUser)
class ApplicationUsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'ussername', 'user_type','db_type','is_active')
    list_display_links = ('ussername',)
    search_fields = ('id', 'ussername',)
    fields = ['id', 'ussername', 'password', 'user_type','db_type','db_name','db_username','db_password','db_hostname',\
               'db_uri','is_active','created_on','updated_on','created_by','updated_by']
    readonly_fields = ('id','created_on','updated_on','created_by','updated_by',)
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True

@admin.register(ReportMaster)
class ReportMasterAdmin(admin.ModelAdmin):
    list_display = ('report_id', 'report_name', 'created_on')
    list_display_links = ('report_name',)
    search_fields = ('report_id', 'report_name',)
    fields = ['report_id','report_name','column_list' ,'created_on','updated_on','created_by','updated_by']
    readonly_fields = ('report_id','created_on','updated_on','created_by','updated_by',)
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
@admin.register(ReportUserMapping)
class ReportUserMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','report' ,'created_on')
    list_display_links = ('user',)
    search_fields = ('id', )
    fields = ['id','user','report' ,'created_on','updated_on','created_by','updated_by']
    readonly_fields = ('id','user','report','created_on','updated_on','created_by','updated_by',)
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return True
    
@admin.register(TableRelationMaster)
class TableRelationMasterAdmin(admin.ModelAdmin):
    list_display = ('id', 'schema','appuserid', 'table_name','column_name','foreign_table_name','foreign_column_name')
    list_display_links = ('schema',)
    search_fields = ('id', 'ussername',)
    fields = ['schema', 'table_name','column_name','foreign_table_name','foreign_column_name','child_data_type','parent_data_type']
    #readonly_fields = ('id', 'schema', 'table_name','column_name','foreign_table_name','foreign_column_name','child_data_type','parent_data_type','created_on','updated_on','created_by','updated_by',)
    
    def has_add_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False