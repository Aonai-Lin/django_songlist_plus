from django.urls import path
from zing_it import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('playlist/<int:id>', views.playlist, name="playlist"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('check-login/', views.check_login_status, name='check_login_status'),
    
]