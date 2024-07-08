from django.urls import path
from .views import (
    ListUsersApiView, 
    MyTokenObtainPairView, 
    LoginApiView, 
    CreateUsersApiView, 
    RetrieveUserApiView,
    ListOrganization,
    RetriveOrganizationsView
    
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/list/', ListUsersApiView.as_view(), name='list-api'),
    path('api/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/login/', LoginApiView.as_view(), name='login'),
    path('auth/register/', CreateUsersApiView.as_view(), name='create-users'),
    path('api/users/<int:id>/', RetrieveUserApiView.as_view(), name= 'retrive-users'),
    path('api/organization/', ListOrganization.as_view(), name='list-organ'),
    path('api/organization/<int:id>', RetriveOrganizationsView.as_view(), name='retrieve-organ'),
]