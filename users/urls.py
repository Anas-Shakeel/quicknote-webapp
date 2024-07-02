from django.urls import path
from . import views

 
urlpatterns = [
    path("", views.index, name="users_index"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup_user, name="signup"),
    path("change_username/", views.change_username, name="change_username"),
    path("change_password/", views.change_password, name="change_password"),
    path("delete_account/", views.delete_account, name="delete_account"),
]
