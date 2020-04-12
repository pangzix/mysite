from django.urls import path
from .views import post_comment

app_name = 'comment'

urlpatterns = [
    path('post-comment/<int:article_id>/',post_comment,name='post_comment'),
    path('post-comment/<int:article_id>/<int:parent_comment_id>/',post_comment,name='comment_reply'),
]