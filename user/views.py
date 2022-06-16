from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정
from rest_framework.response import Response

from django.contrib.auth import login, authenticate, logout

def sum(num1, num2):
    return num1+num2

# Create your views here.
class UserView(APIView):
    # permission_classes = [permissions.AllowAny] # 모두 허용
    permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만
    # permission_classes = [permissions.IsAdminUser] # 관리자만
    # 사용자 정보 조회
    def get(self, request):
        result = sum(**request.data)
        return Response({'message':f'result num is {result}!!'})
    
    # 회원 가입
    def post(self, request):
        return Response({'message':'post method!!'})
    
    # 회원 정보 수정
    def put(self, request):
        return Response({'message':'put method!!'})
    
    # 회원 탈퇴
    def delete(self, request):
        return Response({'message':'delete method!!'})



class UserAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    # 로그인
    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')

        user = authenticate(request, username=username, password=password)
        # user = authenticate(request, **request.data)

        if not user:
            return Response({"error": "id 또는 pw를 확인해주세요."})

        login(request, user)

        return Response({"message": "login success!!"})

    # 로그아웃
    def delete(self, request):
        logout(request)
        return Response({"message": "logout success!!"})
