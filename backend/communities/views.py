from rest_framework import generics, permissions
from .models import Community
from .serializers import CommunitySerializer


class CommunityListView(generics.ListAPIView):
	queryset = Community.objects.filter(is_public=True, is_active=True).order_by('-member_count')
	serializer_class = CommunitySerializer
	permission_classes = [permissions.IsAuthenticated]

# Create your views here.
