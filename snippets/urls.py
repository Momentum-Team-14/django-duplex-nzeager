from django.urls import path
from . import views

urlpatterns = [
    # snippets
    path('', views.list_snippet, name='list_snippet'),
    path('snippets/<int:pk>', views.detail_snippet, name='detail_snippet'),
    path('snippets/new', views.create_snippet, name='create_snippet'),
    path('snippets/<int:pk>/edit/', views.edit_snippet, name='edit_snippet'),
    path('snippets/<int:pk>/delete/', views.delete_snippet, name='delete_snippet'),
    # languages
    path('languages/list', views.list_language, name='list_language'),
    path('languages/<int:pk>', views.detail_language, name='detail_language'),
    path('languages/new', views.create_language, name='create_language'),
    path('languages/<int:pk>/edit/', views.edit_language, name='edit_language'),
    path('languages/<int:pk>/delete/',
         views.delete_language, name='delete_language'),
]
