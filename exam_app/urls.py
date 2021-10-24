from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.front, name='front'),
    path('questions/', views.questions, name='questions'),
    path('login/', views.login, name='login'),
    path('roomview/<int:myid>', views.room_view, name='room_view'),
    path('ans_check/<int:myid2>', views.ans_check, name='ans_check'),
    path('result_data/<int:myid3>', views.result_data, name='result_data'),
    path('view_details/<int:myid4>/<int:student_id>', views.view_details, name='view_details'),
   path('delete_room/<int:room_id>', views.delete_room,name='room_delete'),
   path('room/edit/<int:pk>', views.Editroom,name='room_edit'),

]