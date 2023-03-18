from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/add/', views.adminadd, name="admins_add"),
    path('admin/updt/', views.adminupdt, name="admins_updt"),
    path('admin/updtself/', views.adminupdtself, name="admins_updtself"),
    path('admin/list/', views.adminlist, name="admins_list"),

    path('insert/', views.insert, name="adminsinsert"),

    path('update/', views.update, name="adminsupdate"),

    path('delete/', views.delete, name="adminsdelete"),

]
