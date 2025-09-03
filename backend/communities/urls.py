from django.urls import path
from .views import CommunityListView

app_name = 'communities'

urlpatterns = [
    path('', CommunityListView.as_view(), name='community-list'),
]
