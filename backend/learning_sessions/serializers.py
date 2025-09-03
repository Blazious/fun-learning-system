from rest_framework import serializers
from .models import Session


class SessionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Session
		fields = [
			'id', 'title', 'description', 'session_type', 'status',
			'scheduled_date', 'duration_minutes', 'meeting_platform', 'is_public',
			'created_at'
		]


