from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('club', views.ClubModalViewset, basename='club')

urlpatterns = [
    path('', views.apiOverview, name='api-overview'),
    path('viewset/', include(router.urls)),
    #path('viewset/list/', views.ClubViewset.as_view(), name='playerList'),
    #path('list/', views.PlayerListAPIView.as_view(), name='playerList'),
    path('list/<int:id>/', views.GenericAPIView.as_view(), name='playerList'),
    #path('detail/<int:id>/', views.PlayerDetailAPIView.as_view(), name='playerDetail'),
    #path('detail/<int:pk>/', views.playerDetail, name='playerDetail'),
    path('create/', views.playerCreate, name='playerCreate'),
    #path('index/', views.index)
]
