
from django.contrib import admin
from django.urls import path

from .views import (
    StudentCreateView,
    StudentDetailView,
    StudentListView
)

app_name = 'student'
urlpatterns = [
    # path('',article_list_view, name="article-list"),
    # path('',ArticleListView.as_view(), name='article-list'),
    # path('<int:my_id>/',article_detail_view, name='article-detail')
    path('<int:my_id>/', StudentDetailView.as_view(), name='student-detail'),
    path('create/', StudentCreateView.as_view(), name='student-create'),
    path('', StudentListView.as_view(), name='student-list'),

    # path('',CourseView.as_view(), name='article-list'),
    # path('',CourseView.as_view(template_name='filename.html'), name='article-list')
]
