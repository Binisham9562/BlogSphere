from django.urls import path
from .views import register, login_view, logout_view, home, CustomPasswordResetView, CustomPasswordResetDoneView, protected_view,frontpage,create_profile

urlpatterns = [
    path('',frontpage, name='frontpage'),
    path('home/',home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('create_profile/', create_profile, name='create_profile'),
    path('logout/', logout_view, name='logout'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('protected/', protected_view, name='protected'),  # Protected view
]