from django.contrib import admin
from accounts.models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id' )
    list_filter = ('email',)


admin.site.register(Account, AccountAdmin)