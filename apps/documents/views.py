from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import RiderDocument
from .serializers import RiderDocumentSerializer


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_document(request):
    serializer = RiderDocumentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(uploaded_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rider_documents(request, rider_id):
    documents = RiderDocument.objects.filter(
        rider_id=rider_id
    ).order_by("-created_at")

    serializer = RiderDocumentSerializer(
        documents,
        many=True
    )

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_document(request, pk):
    try:
        document = RiderDocument.objects.get(pk=pk)
    except RiderDocument.DoesNotExist:
        return Response(
            {"detail": "Document not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    document.delete()

    return Response(
        {"detail": "Document deleted successfully."},
        status=status.HTTP_204_NO_CONTENT,
    )
