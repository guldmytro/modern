from django.urls import path
from . import views
app_name = 'pages'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('feadback/', views.feadback, name='feadback'),
    path('send-message/', views.send_message, name='send_message')
]