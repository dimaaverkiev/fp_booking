from django.urls import path
from apartments.views.apartment_views import CreateListApartmentView, DetailApartmentView, UpdateDeleteApartmentView



urlpatterns = [
    # All active Apartments for authenticated users
    path('', DetailApartmentView.as_view(), name='detail'),

    # Apartment list filter owner and create new Apartment
    path('create_apartment/', CreateListApartmentView.as_view(), name='create_apartment'),

    # Update and Delete (is_active False) Apartment and Address
    path('update_delete_apartment/<int:pk>/', UpdateDeleteApartmentView.as_view(), name='update_delete'),
]