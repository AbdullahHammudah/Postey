from rest_framework import viewsets
from rest_framework.response import Response
from app.apiResponse import prepareResponse
from app import settings
from api.models import *
from api.serializers import *
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank




class posts(viewsets.ModelViewSet):

    queryset = Post()
    serializer_class = PostSerializer()

    def records(self, request):
        """
        - Read all posts, Search, Sort, and page collection of posts
        params: 'page', 'search', 'order', 'type'
        """
        posts = Post.objects.all().exclude(status=StatusChoises.DELETED)
        sort_by = request.GET.get('type')
        page = int(request.GET.get('page')) if 'page' in request.GET else 1
        startRecord = (page -1) * settings. PER_PAGE
        endRecord = startRecord + settings.PER_PAGE

        # Search 
        if 'search'in request.GET:
            query = request.GET.get('search')
            vector = SearchVector('title', 'description')
            searchQuery = SearchQuery(query)

            posts = Post.objects\
                .exclude(status=StatusChoises.DELETED)\
                .annotate(rank=SearchRank(vector,searchQuery))\
                .filter('rank__gte=0.001')\
                .order_by('-rank')

        # Sorting
        if 'order' in request.GET == 'desc':
            posts = posts.exclude(status=StatusChoises.DELETED).all().order_by(sort_by.desc())

        serializer = PostSerializer(posts.all()[startRecord:endRecord], many=True)
        return Response(serializer.data)

    def record(self, request, id):
        """
        GET post by id
        """
        post = Post.objects.exclude(
            status=StatusChoises.DELETED).filter(id=id).first()
        if post:
            serializer = PostSerializer(post, many=False)
            return Response(prepareResponse({'total':1}, serializer.data))
        else:
            return Response(prepareResponse({'status':404, 'instance':request.get_full_path()}, {}, False), 404)
    
    def create(self, request):
        """
        Create new post
        """ 
        post = Post()
        for attr, value in request.data.items():
            if attr not in Post.protected():
                setattr(post, attr, value)
        try:
            post.save()
            serializer = PostSerializer(post, many=False)
        except Exception as error:
            return Response(prepareResponse({'status':422, 'instance':request.get_full_path()}, error, False), 422)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def update(self, request, id):
        post = Post.objects.exclude(
            status=StatusChoises.DELETED).filter(id=id).first()
        if post:
            for attr, value in request.data.items():
                if attr not in Post.protected():
                    setattr(post, attr, value)
            try:
                post.save()
                serializer = PostSerializer(post, many=False)
                return Response(prepareResponse({'total':1},serializer.data), 201)
            except Exception as error:
                return Response(prepareResponse({'status':422, 'instance':request.get_full_path()}, error, False), 422)
        else:
            return Response(prepareResponse({"status": 404, "instance": request.get_full_path()}, {}, False), 404)

    def delete(self, request, id=None):
        post = Post.objects.filter(id=id).exclude(
            status=StatusChoises.DELETED).first()

        if post:
            Post.objects.filter(id=id).update(status=StatusChoises.DELETED)
            return Response(prepareResponse({'total':0} , {}, ), 201)

        
