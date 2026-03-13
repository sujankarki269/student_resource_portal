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
]