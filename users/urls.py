from django.urls import path
from .views import UserLoginView, UserCreateView, UserDetailsView, UserListView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/<int:pk>/', UserDetailsView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),


    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view())
]