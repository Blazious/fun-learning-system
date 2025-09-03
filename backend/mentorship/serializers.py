from rest_framework import serializers
from .models import MentorshipProgram


class MentorshipProgramSerializer(serializers.ModelSerializer):
	class Meta:
		model = MentorshipProgram
		fields = ['id', 'name', 'description', 'program_type', 'status', 'start_date', 'end_date']


