from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정
from rest_framework.response import Response

from blog.models import Article

# Create your views here.
class ArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response()