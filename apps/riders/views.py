from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Rider
from .serializers import RiderSerializer
from django.db.models import Q

def get_rider(pk):
    try:
        return Rider.objects.select_related(
            "next_of_kin",
            "motorcycle"
        ).get(pk=pk)
    except Rider.DoesNotExist:
        return None


@api_view(["POST"])
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


