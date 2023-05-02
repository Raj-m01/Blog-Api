from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.db.models import Q
from django.core.paginator import Paginator

from .Serializers import BlogSerializer
from .models import Blog
# Create your views here.

class BlogView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, user=None):
        
        try:
            blogs = Blog.objects.all().order_by('?')

            if user is not None:
                blogs = blogs.filter(user = user)
            else:
                pg_number = request.GET.get('page',1)
                paginator = Paginator(blogs,5)
                blogs = paginator.page(pg_number)
                
            if request.GET.get('search'):
                search = request.GET.get('search')
                print(search)
                blogs = blogs.filter(Q(title__icontains = search) | Q(blog_text__icontains = search))
               
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e :
             print(e)
             return Response(data={}, status=status.HTTP_400_BAD_REQUEST)

         

    def post(self, request):

        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            print(request.user)

            if not serializer.is_valid():
                content = {
                    'message' : "Something went wrong",
                    'data' : serializer.errors
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            content = {
                    'message' : "Blog Created",
                    'data' : serializer.data
                }
            return Response(content, status=status.HTTP_201_CREATED)

        except Exception as e :
                print(e)
                content = {
                    'message' : "Something went wrong",
                    'data' : serializer.errors
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)





        
    def patch(self, request):
         
        try:
            data = request.data

            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                content = {
                    'data' : {},
                    'message' : 'This blog does not exists.'
                }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                content = {
                    'data' : {},
                    'message' : 'You cannot edit this blog'
                }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
            
            serializer = BlogSerializer(data=data,instance=blog[0],partial=True)

            if not serializer.is_valid():
                content = {
                    'data' : {},
                    'message' : 'Something went wrong.'
                }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            content = {
                    'data' : {},
                    'message' : 'Blog edited successfully'
                }
            return Response(content,status=status.HTTP_200_OK)
         
        except Exception as e :
            print(e)
            content = {
                    'data' : {serializer.errors},
                    'message' : 'Something went wrong.'
                }
            return Response(content,status=status.HTTP_400_BAD_REQUEST)
         
    def delete(self, request):

        try:
            data = request.data

            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                content = {
                    'data' : {},
                    'message' : 'This blog does not exists.'
                }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                content = {
                    'data' : {},
                    'message' : 'You cannot delete this blog'
                }
                return Response(content,status=status.HTTP_400_BAD_REQUEST)
            
            blog[0].delete()

            content = {
                    'data' : {},
                    'message' : 'Blog deleted successfully'
                }
            return Response(content,status=status.HTTP_200_OK)
         
        except Exception as e :
            print(e)
            content = {
                    'data' : {},
                    'message' : 'Something went wrong.'
                }
            return Response(content,status=status.HTTP_400_BAD_REQUEST)
