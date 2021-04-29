from .models import CSVFile
from rest_framework import serializers


class CSVModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVFile
        fields = ('file_name', )
