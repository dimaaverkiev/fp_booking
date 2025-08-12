from django.urls import path
from reviews.views import UpdateDeleteReviewView, LandlordListReviewView, CreateListReviewView

urlpatterns = [
    path('list_create_reviews/', CreateListReviewView.as_view(), name='list_create_reviews'),
    path('landlord_list_reviews/', LandlordListReviewView.as_view(), name='landlord_list_reviews'),
    path('update_delete_review/', UpdateDeleteReviewView.as_view(), name='update_delete_review'),
]