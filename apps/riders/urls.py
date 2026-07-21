from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_rider),
    path("", views.rider_list),
    path("<int:pk>/", views.rider_detail),
    path("<int:pk>/update/", views.update_rider),
    path("<int:pk>/delete/", views.delete_rider),
    path("<int:rider_id>/upload-photo/", views.upload_rider_photo, name="upload-rider-photo"),
    path("<int:rider_id>/photo/", views.rider_photo, name="rider-photo"),
]