from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.registerPage, name='register'),
    path('',views.home, name= 'home' ),
    path('blog/<int:pk>/', views.blog, name = 'blog'),
    path('create-blog/', views.createBlog, name = 'create-blog'),
    path('update-blog/<int:pk>/', views.updateBlog, name = 'update-blog'),
    path('delete-blog/<int:pk>/', views.deleteBlog, name='delete-blog'),
    path('profile/<int:pk>/', views.userProfile, name='profile'),
    path('edit-profile/', views.editProfile, name='edit-profile'),

    path('create-project/', views.createProject, name='create-project'),
    path('project/<int:pk>/', views.projectDetail, name='project-detail'),

    path('project/<int:project_id>/create-log/',views.createDevLog,name='create-devlog'),
]
