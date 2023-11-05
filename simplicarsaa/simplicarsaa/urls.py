from django.contrib import admin
from django.urls import path
from django.urls import include, path
from rest_framework import routers
from simplicarbackend import views
from simplicarbackend.views import login_or_register
from simplicarbackend.views import ActiveVehicles
from django.conf import settings
from django.conf.urls.static import static
from simplicarbackend.consumers import BiddingConsumer



router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('get_csrf_token/', views.get_csrf_token, name='get_csrf_token'),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('all_active_vehicles/', ActiveVehicles),
    path('login_or_register/', login_or_register),
    path('single-car/', views.car_detail),
    path('update-bid/', views.update_current_bid),
    path('bidding/', BiddingConsumer.as_asgi()),
    path('list-vehicle/', views.add_vehicle),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

