from django.urls import path, include
from accounts.api import views
#from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('', views.AccountViewSet,)

app_name='accounts'
urlpatterns = [
    path('register/', views.registration_view, name='register'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logoutView.as_view(), name='logout'),
    #path('login/', obtain_auth_token, name='login'),
    # path('whoami/', views.WhoAmIView.as_view(), name="whoami"),
    # path('accounts/', include(router.urls)),
]
