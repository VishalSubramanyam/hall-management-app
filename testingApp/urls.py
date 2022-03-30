from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

urlpatterns = [
    path('', views.dashboard),
    path('register', views.register, name='registration-page'),
    path('login', auth_views.LoginView.as_view(
        template_name='users/login.html', authentication_form=LoginForm,
        redirect_authenticated_user=True,
    ), name='login-page'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout-page'),
    path('dashboard', views.dashboard, name='dashboard-page'),
    path('hall-fees', views.under_construction, name='hall-fees'),
    path('mess-dues', views.under_construction, name='mess-dues'),
    path('file-complaint', views.file_complaint, name='file-complaint'),
    path('view-complaints', views.view_complaints, name='view-complaints'),
    path('file-atr', views.file_atr, name='file-atr'),
    path('access-denied', views.access_denied, name='access-denied')
]
