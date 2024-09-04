from django.urls import path, include
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('professors/', views.professors, name='professors'),
    path('professorView/<int:professor_id>/', views.professor_view, name='professor_view'),
    path('signUp/', views.signupScreen, name='signupScreen'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

    
