from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('professors/', views.professors, name='professors'),
    path('professorView/<int:professor_id>/', views.professor_view, name='professor_view'),
    path('signUp/', views.signupScreen, name='signupScreen'),] + debug_toolbar_urls(),
    
