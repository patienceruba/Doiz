from django.urls import path
from . import views
urlpatterns = [
    path('home', views.home, name="home"),
    path("add", views.addRecord, name='add'),
    path("delete/<str:pk>/", views.deleteRow, name="delete"),
    path('update/<str:pk>/', views.updateRecord, name="update"),
    path("search", views.search, name="search"),
    path("calendar", views.calendar, name="calendar"),
    path('pdfs/', views.pdf_list, name='pdf_list'),
    path("event", views.event, name="event"),
   path('dashboard/', views.dashboard_view, name='dashboard'), 
    path('tasks/done/', views.task_done_view, name='task_done'),
    path('today', views.today_view, name="today")
]
