from django.urls import path
from .views import article_list,article_detail,article_create,article_safe_detete,article_update

app_name = 'article'

urlpatterns = [
    path('article-list/',article_list,name='article_list'),
    path('article-detail/<int:id>/',article_detail,name='article_detail'),
    path('article-create/',article_create,name='article_create'),
    path('article-safe-detete/<int:id>/',article_safe_detete,name='article_safe_delete'),
    path('article-update/<int:id>/',article_update,name='article_update'),

]