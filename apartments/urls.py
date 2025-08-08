from django.urls import path
from apartments.views.apartment_views import CreateApartmentView, DetailApartmentView, UpdateDeleteApartmentView
from apartments.views.apartment_address_views import CreateApartmentAddressView, UpdateDeleteApartmentAddressView
from apartments.views.category_views import CreateFederalStateListView, UpdateFederalStateListView



urlpatterns = [
    path('', DetailApartmentView.as_view(), name='detail'),
    path('create_apartment/', CreateApartmentView.as_view(), name='create_apartment'),
    path('update_delete_apartment/<int:pk>/', UpdateDeleteApartmentView.as_view(), name='update_delete'),
    path('create_address/', CreateApartmentAddressView.as_view(), name='create_address'),
    path('update_delete_address', UpdateDeleteApartmentAddressView.as_view(), name='update_delete_address'),
]