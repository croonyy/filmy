from rest_framework import serializers

from rbac import models as rbac_md
from rbac.models import Test


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'


# class TestSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     code = serializers.JSONField()
#     code2 = serializers.CharField(max_length=1000)
#
#     def create(self, validated_data):
#         return rbac_md.Test.objects.create(**validated_data)
#
#     class Meta:
#         model = Test
#         fields = '__all__'


# 还有另一种创建序列化器的方法，就是一步一步添加，当然上面这种代码会少很多
# 一步一步增加序列化
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    User_id = serializers.IntegerField()
    name = serializers.CharField(max_length=32)
    age = serializers.IntegerField()
    num = serializers.IntegerField()
    password = serializers.IntegerField()

    def create(self, validated_data):
        return rbac_md.User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.User_id = validated_data.get('User_id', instance.User_id)
        instance.name = validated_data.get('name', instance.name)
        instance.age = validated_data.get('age', instance.age)
        instance.num = validated_data.get('num', instance.num)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance
