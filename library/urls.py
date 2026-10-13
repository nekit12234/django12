from django.urls import path

from . import views

app_name = 'library'

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.book_list, name='book_list'),
    path('books/<slug:slug>/', views.book_detail, name='book_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('readers/', views.reader_list, name='reader_list'),
    path('readers/<int:pk>/', views.reader_detail, name='reader_detail'),
    path('about/', views.about, name='about'),
]