from django.urls import path
from .views import CommentNoticeListView,CommentNoticeUpdateView

app_name = 'notice'

urlpatterns = [
    path('list/',CommentNoticeListView.as_view(),name='list'),
    path('update/',CommentNoticeUpdateView.as_view(),name='update'),
]