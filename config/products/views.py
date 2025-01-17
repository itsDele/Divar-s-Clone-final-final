from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Advertisement
from .serializers import AdvertisementSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from accounts.models import User


class AdvertisementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        advertisements = Advertisement.objects.filter(user=request.user)
        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        data["is_active"] = True
        price = data["price"]
        price = int(price)
        if price <= 0:
            return Response(
                {"message": "Price must be greater than 0"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AdvertisementSerializer(data=data)
        if serializer.is_valid():
            advertisement = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        pk = request.data.get("id")
        advertisement = get_object_or_404(Advertisement, pk=pk)
        serializer = AdvertisementSerializer(advertisement, data=request.data)
        if serializer.is_valid():
            advertisement = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = request.data.get("id")
        advertisement = get_object_or_404(Advertisement, pk=pk)
        advertisement.delete()
        return Response({"message": "Advertisement deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class AllAdvertisementsView(APIView):

    def get(self, request):
        category = request.query_params.get("category")
        city = request.query_params.get("city")
        ad_status = request.query_params.get("status")
        price = request.query_params.get("price")
        title = request.query_params.get("title")

        advertisements = Advertisement.objects.filter()
        if category:
            advertisements = advertisements.filter(category=category)
        if city:
            advertisements = advertisements.filter(city=city)
        if ad_status:
            advertisements = advertisements.filter(status=ad_status)
        if price:
            advertisements = advertisements.filter(price__gte=price)
        if title:
            advertisements = advertisements.filter(title__contains=title)

        serializer = AdvertisementSerializer(advertisements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ad_id = request.query_params.get("ad_id")
        advertisement = get_object_or_404(Advertisement, pk=ad_id)

        ad_owner = User.objects.get(pk=advertisement.id)
        ad_owner_phone = ad_owner.phone_number
        ad_owner_phone = str(ad_owner.phone_number)

        ad_info = {
            "owner_phone": ad_owner_phone,
            "owner_name": ad_owner.username,
            "owner_email": ad_owner.email,
        }

        serializer = AdvertisementSerializer(advertisement)

        response_data = serializer.data
        response_data.update(ad_info)

        return Response(response_data, status=status.HTTP_200_OK)