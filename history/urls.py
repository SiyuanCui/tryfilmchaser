from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/visitor/', views.visitor, name="history_visitor"),
    # Front add page
    path('add/', views.add, name="historyadd"),

    # Data insertion
    path('insert/', views.insert, name="historyinsert"),

    # Data insertion
    path('update/', views.update, name="historyupdate"),

    # Delete data
    path('delete/', views.delete, name="historydelete"),

]
