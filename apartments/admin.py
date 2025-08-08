from django.contrib import admin
from apartments.models import Apartment, ApartmentAddress, Category, FederalState


admin.site.register(Apartment)
admin.site.register(ApartmentAddress)
admin.site.register(Category)
admin.site.register(FederalState)



