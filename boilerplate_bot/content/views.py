from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet, ViewSet

from .models import Button, ButtonLog, Content, RandomText
from .serializers import (ButtonSerializer, ContentSerializer,
                          RandomTextSerializer)

User = get_user_model()


class ButtonViewSet(ViewSet):

    @action(detail=False)
    def start_list(self, request, tg_id, *args, **kwargs):
        """Выдаёт инлайн-кнопки меню по команде "start"."""
        User.objects.get_or_create(tg_id=tg_id)
        buttons = Button.objects.filter(parent=None)
        serializer = ButtonSerializer(buttons, many=True)
        return Response(serializer.data)

    def list(self, request, tg_id, button_id, *args, **kwargs):
        """Выдаёт инлайн-кнопки."""
        try:
            Button.objects.get(pk=button_id)
            buttons = Button.objects.filter(
                parent=button_id
            )
            serializer = ButtonSerializer(buttons, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request, tg_id, button_id, *args, **kwargs):
        """Создаёт лог в ButtonLog с телеграм-id пользователя,
        title кнопки и датой нажатия.
        """
        user = User.objects.get_or_create(tg_id=tg_id)[0]
        button = get_object_or_404(Button, pk=button_id)
        if ButtonLog.objects.create(user=user, button=button):
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ContentViewSet(ViewSet):

    def list(self, request, button_id, *args, **kwargs):
        """Выдача контента кнопки."""
        content = Content.objects.filter(
            button=button_id
        ).order_by('order_of_send')
        serializer = ContentSerializer(content, many=True)
        return Response(serializer.data)

    def partial_update(self, request, content_id, *args, **kwargs):
        """Запись телеграм-id медиа-файла в Content."""
        content = Content.objects.get(pk=content_id)
        serializer = ContentSerializer(
            content, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )


class RandomTextViewSet(ReadOnlyModelViewSet):

    def retrieve(self, request, *args, **kwargs):
        """Выдача рандомного текста."""
        queryset = RandomText.objects.order_by('?').first()
        serializer_class = RandomTextSerializer(queryset)
        return Response(serializer_class.data)
