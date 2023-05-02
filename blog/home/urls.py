from django.contrib import admin
from django.urls import path
from .views import BlogView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/',BlogView.as_view()),
    # path('blogs/<str:user>/',BlogView.as_view()),
]