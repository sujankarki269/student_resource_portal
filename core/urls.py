from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('notes/', views.notes_list, name='notes'),
    path('assignments/', views.assignments_list, name='assignments'),
    path('programs/', views.programs_list, name='programs'),
    path('tutorials/', views.tutorials_list, name='tutorials'),
    path('download/<str:model>/<int:pk>/', views.download_file, name='download'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
]