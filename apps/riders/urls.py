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
    path("pending/", views.pending_riders, name="pending-riders"),
    path("<int:rider_id>/approve/", views.approve_rider, name="approve-rider"),
    path("<int:rider_id>/reject/", views.reject_rider, name="reject-rider"),
]