from rest_framework.permissions import BasePermission
from datetime import datetime, timedelta
from django.utils import timezone

# join_date 가 DatetimeField 일때는 timezone을 사용한다
# (datatime)user.join_data > datetime.now() => X
# (datatime)user.join_data > timezone.now() => O

class RegistedMoreThanThreeDaysUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        return bool(user.join_date < (timezone.now() - timedelta(days=1)))

        