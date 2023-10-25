from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from simplicarbackend import views
from simplicarbackend.views import test

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('test/', test)
]
