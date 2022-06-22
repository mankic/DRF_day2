from rest_framework import serializers

# from user.models import User as UserModel
from product.models import Product as ProductModel


class ProductSerializer(serializers.ModelSerializer):
    
    # author = serializers.SlugRelatedField(
    #     read_only = True,
    #     slug_field = 'username',
    # )
            
    class Meta:
        model = ProductModel
        fields = ["author","title","thumbnail","desc","created","start_view","end_view"]
    