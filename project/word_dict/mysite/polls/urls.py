from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find', views.find, name='find'),
    path('save', views.save, name='save'),
    path('save_expr', views.save_expr, name='save_expr'),
    path('save_subject', views.save_subject, name='save_subject'),
    path('search_subject', views.search_subject, name='search_subject'),
    path('remove_subject', views.remove_subject, name='remove_subject'),
    path('search', views.search, name='search'),
    path('search_expr', views.search_expr, name='search_expr'),
    path('remove', views.remove, name='remove'),
    path('remove_expr', views.remove_expr, name='remove_expr'),
]