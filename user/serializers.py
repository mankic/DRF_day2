from rest_framework import serializers

from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel

from blog.models import Article as ArticleModel
from blog.models import Comment as CommentModel

from blog.serializers import UserArticleSerializer

VALID_EMAIL_LIST = ['naver.com','gmail.com','daum.net']

class HobbySerializer(serializers.ModelSerializer):
    same_hobby_users = serializers.SerializerMethodField()
    def get_same_hobby_users(self,obj):
        # obj : hobby model 의 object
        
        # user_list = []
        # for user_profile in obj.userprofile_set.all():
        #     user_list.append(user_profile.user.username)

        # return user_list

        user = self.context["request"].user

        # for 축약
        return [user_profile.user.username for user_profile in obj.userprofile_set.exclude(user=user)]

    class Meta:
        model = HobbyModel
        fields = ["name","same_hobby_users"]


class UserProfileSerializer(serializers.ModelSerializer):
    # 매니투매니 관계이므로 쿼리셋으로 return  # input data 쿼리셋이면 many=True
    hobby = HobbySerializer(many=True, read_only=True)   # read_only 하지않으면 회원가입시(create)에 hobby 생성되버림
    get_hobbys = serializers.ListField(required=False)   # hobby 를 선택할 수 있게   
    class Meta:
        model = UserProfileModel
        fields = ["age","birthday","hobby","get_hobbys"]


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()   # 원투원관계의 경우 object로 return
    articles = UserArticleSerializer(many=True, source='article_set', read_only=True)
    
    # validate : 기존 validation + custom validation
    def validate(self, data):
        # try:
        #     http_method = self.context.['request'].method
        # except:
        #     http_method = ''
        # if http_method == "POST":
        if data.get("email","").split("@")[-1] not in VALID_EMAIL_LIST:
            raise serializers.ValidationError(
                detail={"error": "네이버 이메일만 가입 가능 합니다."}
            )
        return data

    # 기존함수 덮어씀   # validate 된 data가 들어간다.
    # 회원가입시 userprofile 까지 입력할 수 있게
    def create(self,validated_data):
        user_profile = validated_data.pop("userprofile")
        # print(user_profile)     # OrderedDict([('age', 20), ('birthday', datetime.date(2000, 1, 1)), ('get_hobbys', [1, 2])])
        # print(validated_data)   # {'username': 'test3', 'password': '1234', 'email': 'test3@naver.com'}
        password = validated_data.pop("password")
        get_hobbys = user_profile.pop("get_hobbys",[])

        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()

        user_profile = UserProfileModel.objects.create(user=user, **user_profile)

        # ManyToMany 관계에서 데이터 추가할때 .add() 사용
        user_profile.hobby.add(*get_hobbys)   # [1,2,3,4] 언패킹해서 hobby 에 추가
        return user
        # return UserModel(**validated_data)  # 검증된 데이터를 UserModel에 넣어서 보여주기


    def update(self, instance, validated_data):
        user_profile = validated_data.pop("userprofile")
        get_hobbys = user_profile.pop("get_hobbys",[])

        # instance에는 입력된 object가 담긴다.
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)   # instance.username = "value"
        instance.save()

        user_profile_obj = instance.userprofile
        for key, value in user_profile.items():
            setattr(user_profile_obj, key, value)   # 역참조
        user_profile_obj.save()
        return instance

# post에서 .save() 할때 def create 호출 
# put에서 .save() 할때 def update 호출. serializer 지정할때 object 같이 넣어준다

    class Meta:
        model = UserModel
        # fields = '__all__'  # 모든필드 가져온다
        fields = ["username","password","email","join_date","userprofile","articles"]
        # auto now add 속성은 기본적으로 read_only 상태이다.
        extra_kwargs = {
            # write_only : 해당 필드를 쓰기 전용으로 만들어 준다.
            # 쓰기 전용으로 설정 된 필드는 직렬화 된 데이터에서 보여지지 않는다.
            'password': {'write_only': True}, # default : False
            'email': {
                # error_messages : 에러 메세지를 자유롭게 설정 할 수 있다.
                'error_messages': {
                    # required : 값이 입력되지 않았을 때 보여지는 메세지
                    'required': '이메일을 입력해주세요.',
                    # invalid : 값의 포맷이 맞지 않을 때 보여지는 메세지
                    'invalid': '알맞은 형식의 이메일을 입력해주세요.'
                    },
                    # required : validator에서 해당 값의 필요 여부를 판단한다.
                    'required': False # default : True
                    },
            }