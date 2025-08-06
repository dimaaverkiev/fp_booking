from django.contrib import admin
from accounts.models import User, LandlordUser, TenantUser

admin.site.register(User)
admin.site.register(LandlordUser)
admin.site.register(TenantUser)

