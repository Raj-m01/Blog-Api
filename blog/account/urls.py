from django.contrib import admin
from django.urls import path
from .views import SignUpView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',SignUpView.as_view()),
    path('login/',LoginView.as_view())
]
