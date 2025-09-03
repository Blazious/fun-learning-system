from rest_framework import generics, permissions
from .models import MentorshipProgram
from .serializers import MentorshipProgramSerializer


class MentorshipProgramListView(generics.ListAPIView):
	queryset = MentorshipProgram.objects.filter(is_public=True).order_by('-created_at')
	serializer_class = MentorshipProgramSerializer
	permission_classes = [permissions.IsAuthenticated]

# Create your views here.
