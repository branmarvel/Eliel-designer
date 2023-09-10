from django.urls import path
from register import views
app_name = 'register'
urlpatterns = [
    path('', views.mi_vista, name='inicio'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Corrected 'dashboard' spelling

]
