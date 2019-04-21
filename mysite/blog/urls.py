from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'blog'

urlpatterns = [
    # post views

    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('new_post/', views.post_create, name='post_create'),
    path('my_list/', views.my_list, name='my_list'),
    path('edit/', views.edit, name='edit'),
]