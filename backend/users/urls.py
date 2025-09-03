from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # User registration and authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/detail/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Alumni verification
    path('verification/', views.AlumniVerificationView.as_view(), name='verification-create'),
    path('verification/list/', views.AlumniVerificationListView.as_view(), name='verification-list'),
    path('verification/<uuid:pk>/', views.AlumniVerificationDetailView.as_view(), name='verification-detail'),
    
    # Admin views
    path('admin/users/', views.UserListView.as_view(), name='admin-user-list'),
    path('admin/users/<uuid:pk>/', views.UserDetailView.as_view(), name='admin-user-detail'),
    path('admin/verification/', views.AdminVerificationListView.as_view(), name='admin-verification-list'),
    path('admin/verification/<uuid:pk>/', views.AdminVerificationDetailView.as_view(), name='admin-verification-detail'),
    
    # Utility endpoints
    path('stats/', views.user_stats, name='user-stats'),
    path('add-points/', views.add_points, name='add-points'),
]
