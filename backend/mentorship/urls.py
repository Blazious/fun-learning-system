from django.urls import path
from .views import MentorshipProgramListView

app_name = 'mentorship'

urlpatterns = [
    path('programs/', MentorshipProgramListView.as_view(), name='program-list'),
]
