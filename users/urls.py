from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('register', views.RegistrationView.as_view(), name='register'),
    path('activate-email-sent', views.AccuntActivationSent, name='activate-email-sent'),
    path('activate/<str:uidb64>/<str:token>', views.ActivateAccount.as_view(), name='activate-account'),
    # Password Reset
    path("password-reset", views.PasswordResetView.as_view(), name="password-reset"),
    path('password-reset/done/', 
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), 
        name='password-reset-done'
    ),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="password_reset/password_reset_confirm.html"),
        name='password-reset-confirm'
    ),
    # Profile Views
    path('profile', views.ProfileView.as_view(), name='profile'),
]
