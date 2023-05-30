from rest_framework import serializers

from rbac import models as md


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = md.Test
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = md.Permission
        fields = '__all__'
