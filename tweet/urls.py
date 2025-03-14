from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import the auth_views correctly

urlpatterns = [
    path('', views.tweet_list, name="tweet_list"),
    path('create/', views.tweet_create, name="tweet_create"),
    path('tweet/<int:pk>/', views.tweet_detail, name="tweet_detail"),
    path('tweet/<int:pk>/edit/', views.tweet_edit, name="tweet_edit"),
    path('tweet/<int:pk>/delete/', views.tweet_delete, name="tweet_delete"),
    path('register/', views.user_register, name="user_register"),
    path('login/', auth_views.LoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
