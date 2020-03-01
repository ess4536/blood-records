from rest_framework import serializers

from record.models import Sheet

class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = ['id', 'name', 'user']

        def create(self, validated_data):

            return Sheet.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.user = validated_data.get('user', instance.user)
            instance.save()
            return instance