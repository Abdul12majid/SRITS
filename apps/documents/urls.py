from django.urls import path

from . import views 

urlpatterns = [
    path("upload/", views.upload_document, name="upload-document", ),
    path("rider/<int:rider_id>/", views.rider_documents, name="rider-documents",),
    path("<int:pk>/", views.delete_document, name="delete-document",),
]