from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Rider
from .serializers import RiderSerializer

@api_view(["POST"])
def register_rider(request):
    serializer = RiderSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def rider_list(request):
    riders = Rider.objects.all().order_by("-id")
    serializer = RiderSerializer(riders, many=True)

    return Response(serializer.data)

@api_view(["GET"])
def rider_detail(request, pk):
    try:
        rider = Rider.objects.get(pk=pk)
    except Rider.DoesNotExist:
        return Response(
            {"error": "Rider not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = RiderSerializer(rider)

    return Response(serializer.data)