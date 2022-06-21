from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status

# join_date 가 DatetimeField 일때는 timezone을 사용한다
# (datatime)user.join_data > datetime.now() => X
# (datatime)user.join_data > timezone.now() => O

class RegistedMoreThanThreeDaysUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return bool(user.join_date < (timezone.now() - timedelta(days=1)))



class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)

class IsAdminOrIsAuthenticatedReadOnly(BasePermission):
    """
    admin 사용자는 모두 가능, 로그인 사용자는 조회만 가능
    """
    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:   # 로그인 안되어있으면
            response ={
                    "detail": "서비스를 이용하기 위해 로그인 해주세요.",
                }
            raise GenericAPIException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response)

        if user.is_admin or user.join_date < (timezone.now() - timedelta(days=7)):   # 로그인 7이후 + 어드민
            return True
            
        elif user.is_authenticated and request.method in self.SAFE_METHODS:     # 로그인 + SAFE_METHODS
            return True
        
        return False

        