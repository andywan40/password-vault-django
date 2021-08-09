from django.contrib import admin
from password.models import Password

class PasswordAdmin(admin.ModelAdmin):
    list_display = ('id','account', 'name', 'website','username', 'password','is_favorite','description', 'notes', )
    list_filter = ('account', 'is_favorite',)
    search_fields = ['account', 'name',]


admin.site.register(Password, PasswordAdmin)