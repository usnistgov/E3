from django.urls import path

from frontend import views

urlpatterns = [
    # Wire up the API using automatic URL routing
    path('login/', views.email_login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('delete/', views.delete_user, name="delete"),
    path('revoke-key/', views.revoke_key, name="revoke-key")
]
