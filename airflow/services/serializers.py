from rest_framework import serializers
from airflow .models import SearchResult


class SearchResultReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchResult
        fields = ('id','provider', 'data', 'search_id')
