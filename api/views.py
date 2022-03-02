from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Post
from api.serializers import PostSerializer



# Create your views here.
@api_view(['GET'])
def records(request):
    print(request)
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def single_record(request,id):
    if request.method == 'GET':
        post = Post.objects.get(pk=id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

@api_view(['POST'])
def add_record(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(query)
    serializer = PostSerializer(posts, many=Ture)
    return Response(serializer.data)
        
