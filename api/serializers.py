from rest_framework import serializers

from record.models import Sheet, Category

class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = ['id', 'name', 'user']
        read_only_fields = ['user']

        def create(self, validated_data):

            return Sheet.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.save()
            return instance

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'axis', 'upper', 'lower', 'description', 'sheet', 'user']
        read_only_fields = ['user']

        def create(self, validate_data):
            return Category.objects.create(**validate_data)

        def update(self, instance, validate_data):
            instance.name = validate_data.get('name', instance.name)
            instance.axis = validate_data.get('axis', instance.axis)
            instance.upper = validate_data.get('upper', instance.upper)
            instance.lower = validate_data.get('lower', instance.lower)
            instance.sheet = validate_data.get('sheet', instance.sheet)
            instance.save()
            return instance