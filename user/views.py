from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions  # 권한 설정
from rest_framework.response import Response

from django.contrib.auth import login, authenticate, logout

from user.models import UserProfile as UserProfileModel
from user.models import User as UserModel
from user.models import Hobby as HobbyModel

from user.serializers import UserSerializer

from DRF_day2.permissions import RegistedMoreThanAWeekUser

# Create your views here.
class UserView(APIView):
    # permission_classes = [permissions.AllowAny] # 모두 허용
    # permission_classes = [permissions.IsAuthenticated] # 로그인된 사용자만
    # permission_classes = [permissions.IsAdminUser] # 관리자만
    permission_classes = [RegistedMoreThanAWeekUser]

    # 사용자 정보 조회
    def get(self, request):
        user = request.user
        
        # 역참조를 사용했을때
        # OneToOne 필드는 예외로 _set이 붙지 않는다.
        # hobbys = user.userprofile.hobby.all()
        # hobbys = str(hobbys)

        # 역참조를 사용하지 않았을때
        # user_profile = UserProfile.objects.get(user=user)
        # hobbys = user_profile.hobby.all()

        # for hobby in hobbys:
		    # exclde : 매칭 된 쿼리만 제외, filter와 반대
		    # annotate : 필드 이름을 변경해주기 위해 사용, 이외에도 원하는 필드를 추가하는 등 다양하게 활용 가능
		    # values / values_list : 지정한 필드만 리턴 할 수 있음. values는 dict로 return, values_list는 tuple로 ruturn
		    # F() : 객체에 해당되는 쿼리를 생성함. (스트링을 쿼리로 바꿔준다)
            # user__username : user 프로필 안에 있는 username
            # hobby_members = hobby.userprofile_set.exclude(user=user).annotate(username=F('user__username')).values_list('username', flat=True)
            # hobby_members = list(hobby_members)
            # print(f"hobby : {hobby.name} / hobby members : {hobby_members}")

        return Response(UserSerializer(user).data)
    
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
