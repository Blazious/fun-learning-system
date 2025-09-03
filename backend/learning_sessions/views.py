from rest_framework import generics, permissions
from .models import Session
from .serializers import SessionSerializer


class SessionListView(generics.ListAPIView):
	queryset = Session.objects.filter(is_public=True).order_by('-scheduled_date')
	serializer_class = SessionSerializer
	permission_classes = [permissions.IsAuthenticated]

