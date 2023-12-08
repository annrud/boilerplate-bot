from django.urls import path

from .views import ButtonViewSet, ContentViewSet, RandomTextViewSet

urlpatterns = [
    path(
        'button/telegram/<int:tg_id>/',
        ButtonViewSet.as_view({
            'get': 'start_list',
        })
    ),
    path(
        'button/<int:button_id>/telegram/<int:tg_id>/',
        ButtonViewSet.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    path(
        'content/button/<int:button_id>/',
        ContentViewSet.as_view({
            'get': 'list',
        })
    ),
    path(
        'content/<int:content_id>/',
        ContentViewSet.as_view({
            'post': 'partial_update',
        })
    ),
    path(
        'random/',
        RandomTextViewSet.as_view({
            'get': 'retrieve',
        })
    ),
]
