from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/add/', views.adminadd, name="columns_add"),
    path('admin/updt/', views.adminupdt, name="columns_updt"),
    path('admin/list/', views.adminlist, name="columns_list"),

    path('insert/', views.insert, name="columnsinsert"),

    path('update/', views.update, name="columnsupdate"),

    path('delete/', views.delete, name="columnsdelete"),

]
