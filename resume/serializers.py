from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file', 'uploaded_at', 'extracted_text']
        read_only_fields = ['uploaded_at', 'extracted_text']
