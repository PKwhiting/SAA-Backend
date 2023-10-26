from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from simplicarbackend import views
from simplicarbackend.views import test
from simplicarbackend.views import login_or_register

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', test),
    path('login_or_register/', login_or_register),
]
