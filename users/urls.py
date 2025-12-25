from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Authentication endpoints
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forget/', views.forget_password_view, name='forget'),
    path('reset/', views.reset_password_view, name='reset'),
    
    # Profile endpoints
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_detail'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
    # Post endpoints
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:post_id>/delete/', views.delete_post_view, name='delete_post'),
]