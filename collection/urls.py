from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/list/', views.adminlist, name="collection_list"),
    path('admin/username/', views.username, name="collection_username"),
    path('add/', views.add, name="collectionadd"),

    path('insert/', views.insert, name="collectioninsert"),

    path('update/', views.update, name="collectionupdate"),

    path('delete/', views.delete, name="collectiondelete"),

    path('admin/batch/', views.batch, name="collectionbatch"),

]
