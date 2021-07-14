from django.urls import path

from .views import *

app_name = "tumblrapp"

urlpatterns = [
    path('posts/all', PostCrudView.as_view()),  # To get all posts
    path('posts/<str:type>/all', PostCrudView.as_view()),  # To get all posts by blogtype
    path('posts/<int:pk>', PostCrudView.as_view()),  # To get required post
    path('posts/create', PostCrudView.as_view()),  # To create a post
    path('posts/<int:pk>/files/all', PostFileCrudView.as_view()),  # To get all files in a post
    path('posts/<int:pk>/files/add', PostFileCrudView.as_view()),  # To add file to a post
    path('posts/<int:pk>/files/<int:pk2>', PostFileCrudView.as_view()),  # To get required file in a post
    path('download_file/<int:pk>', DownloadFile.as_view()),  # To download a file
]
