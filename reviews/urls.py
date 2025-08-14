from django.urls import path
from reviews.views import UpdateDeleteReviewView, LandlordListReviewView, CreateListReviewView, ApartmentListReviewView




urlpatterns = [
    path('list_create_reviews/', CreateListReviewView.as_view(), name='list_create_reviews'),
    path('landlord_list_reviews/', LandlordListReviewView.as_view(), name='landlord_list_reviews'),
    path('update_delete_review/<int:pk>/', UpdateDeleteReviewView.as_view(), name='update_delete_review'),
    path('apartment/<int:apartment_id>/', ApartmentListReviewView.as_view(), name='apartment_list_review'),
]