from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Rider
from .serializers import RiderSerializer
from django.db.models import Q
from apps.accounts.permissions import role_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

def get_rider(pk):
    try:
        return Rider.objects.select_related(
            "next_of_kin",
            "motorcycle"
        ).get(pk=pk)
    except Rider.DoesNotExist:
        return None


@api_view(["POST"])
@role_required(["SUPER_ADMIN", "REGISTRATION_OFFICER"])
def register_rider(request):
    serializer = RiderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def rider_list(request):
    search = request.GET.get("search", "")
    page = int(request.GET.get("page", 1))
    page_size = 20

    riders = Rider.objects.select_related(
        "next_of_kin",
        "motorcycle"
    )

    if search:
        riders = riders.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(nin__icontains=search) |
            Q(motorcycle__plate_number__icontains=search)
        )

    total = riders.count()

    start = (page - 1) * page_size
    end = start + page_size

    serializer = RiderSerializer(
        riders[start:end],
        many=True
    )

    return Response({
        "count": total,
        "page": page,
        "page_size": page_size,
        "results": serializer.data
    })


@api_view(["GET"])
def rider_detail(request, pk):
    rider = get_rider(pk)

    if rider is None:
        return Response(
            {"error": "Rider not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = RiderSerializer(rider)
    return Response(serializer.data)


@api_view(["PUT", "PATCH"])
def update_rider(request, pk):
    rider = get_rider(pk)

    if rider is None:
        return Response(
            {"error": "Rider not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = RiderSerializer(
        rider,
        data=request.data,
        partial=request.method == "PATCH"
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_rider(request, pk):
    rider = get_rider(pk)

    if rider is None:
        return Response(
            {"error": "Rider not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    rider.delete()

    return Response(
        {"message": "Rider deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )





@api_view(["POST"])
@permission_classes([IsAuthenticated])
def upload_rider_photo(request, rider_id):
    try:
        rider = Rider.objects.get(id=rider_id)
    except Rider.DoesNotExist:
        return Response(
            {"detail": "Rider not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if "photo" not in request.FILES:
        return Response(
            {"detail": "No photo uploaded."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Delete old photo if it exists
    if rider.photo:
        old_photo_path = os.path.join(settings.MEDIA_ROOT, rider.photo.name)

        if os.path.isfile(old_photo_path):
            os.remove(old_photo_path)

    # Save the new photo
    rider.photo = request.FILES["photo"]
    rider.save()

    return Response(
        {
            "message": "Photo uploaded successfully.",
            "photo": rider.photo.url,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rider_photo(request, rider_id):
    try:
        rider = Rider.objects.get(id=rider_id)
    except Rider.DoesNotExist:
        return Response(
            {"detail": "Rider not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if not rider.photo:
        return Response(
            {"detail": "No photo available."},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            "photo": rider.photo.url
        }
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_rider(request, rider_id):
    try:
        rider = Rider.objects.get(id=rider_id)
    except Rider.DoesNotExist:
        return Response(
            {"detail": "Rider not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    if rider.status == "APPROVED":
        return Response(
            {"detail": "Rider is already approved."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    rider.status = "APPROVED"
    rider.approved_by = request.user
    rider.approved_at = timezone.now()
    rider.save()

    return Response({
        "message": "Rider approved successfully."
    })



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_rider(request, rider_id):
    try:
        rider = Rider.objects.get(id=rider_id)
    except Rider.DoesNotExist:
        return Response(
            {"detail": "Rider not found."},
            status=status.HTTP_404_NOT_FOUND,
        )

    rider.status = "REJECTED"
    rider.approved_by = request.user
    rider.approved_at = timezone.now()
    rider.save()

    return Response({
        "message": "Rider rejected successfully."
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pending_riders(request):
    riders = Rider.objects.filter(
        status="PENDING"
    ).order_by("-created_at")

    serializer = RiderSerializer(
        riders,
        many=True
    )

    return Response(serializer.data)