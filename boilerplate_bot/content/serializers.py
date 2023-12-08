from rest_framework import serializers


from .models import Button, Content, RandomText


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = [
            'pk',
            'button',
            'material_type',
            'file_url',
            'file_id',
            'text',
        ]


class ButtonSerializer(serializers.ModelSerializer):
    parent_title = serializers.ReadOnlyField(source='parent.title')

    class Meta:
        model = Button
        fields = [
            'pk',
            'title',
            'link',
            'random_text',
            'parent',
            'parent_title',
        ]


class RandomTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomText
        fields = [
            'text',
        ]
