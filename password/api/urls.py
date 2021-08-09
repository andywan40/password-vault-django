from django.urls import path, include
from password.api import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.PasswordViewSet, basename='passwords')

app_name='password'
urlpatterns = [
    path('', include(router.urls)),
    # path('', views.password_list, name='password-list'),
    # path('<int:pk>/', views.password_detail, name='password-detail'),
]