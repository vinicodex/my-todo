from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/', views.signup_user, name='home'),
    path('login/', views.login_user, name='loginuser'),
    path("logout/", views.logout_user, name='logoutuser'),

    path('create/', views.create_todos, name='createtodos'),

    path('todos/', views.current_todos, name='todos'),
    path('completed_todos/', views.completed_todos, name='completed_todos'),


    path('todo/<int:pk>', views.view_todo, name='view_todo'),
    path('todo/<int:pk>/complete', views.complete_todo, name='complete_todo'),
    path('todo/<int:pk>/delete', views.delete_todo, name='delete_todo'),

]
