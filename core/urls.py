from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('a-propos/', views.about, name='about'),
    path('projets/', views.projects, name='projects'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('cv/', views.cv, name='cv'),
]
