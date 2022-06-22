from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions, status  # 권한 설정
from rest_framework.response import Response
from datetime import datetime
from django.db.models import Q


from django.contrib.auth import login, authenticate, logout

from user.models import User as UserModel
from product.models import Product as ProductModel

from product.serializers import ProductSerializer

# from DRF_day2.permissions import RegistedMoreThanAWeekUser


class ProductView(APIView):

    # product 정보 조회
    def get(self, request):
        products = ProductModel.objects.filter(
            Q(start_view__lte=datetime.now(), end_view__gte=datetime.now())|
            Q(author=request.user)
        )

        serializer = ProductSerializer(products, many=True, context={"request":request}).data
        
        return Response(serializer, status=status.HTTP_200_OK)

    # product 정보 작성
    def post(self, request):
        request.data['author'] = request.user.id
        product_serializer = ProductSerializer(data=request.data)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        # user_serializer.is_valid(raise_exception=True)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # product 정보 수정
    def put(self, request, product_id):
        product = ProductModel.objects.get(id=product_id)
        product_serializer = ProductSerializer(product, data=request.data, partial=True)

        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        # user_serializer.is_valid(raise_exception=True)

        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request):
        return Response({"message": "delete success!!"})

    