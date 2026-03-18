from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes'),
    path('assignments/', views.assignments_list, name='assignments'),
    path('programs/', views.programs_list, name='programs'),
    path('tutorials/', views.tutorials_list, name='tutorials'),
    path('download/<str:model>/<int:pk>/', views.download_file, name='download'),
    path('profile/', views.profile, name='profile'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('tutorials/', views.tutorials_list, name='tutorials'),
    path('tutorials/category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('tutorials/post/<slug:slug>/', views.blog_post_detail, name='blog_post_detail'),
    path('publications/', views.publications_list, name='publications'),
]