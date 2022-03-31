from rest_framework import serializers
from .models import Post, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class PostSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = ['id','title','description', 'status','created_at','updated_at']