from django.urls import path, include
from . import views

urlpatterns = [
    # Add page in the background
    path('admin/add/', views.adminadd, name="picture_add"),
    path('admin/updt/', views.adminupdt, name="picture_updt"),
    # Background list page
    path('admin/list/', views.adminlist, name="picture_list"),

    # Data insertion
    path('insert/', views.insert, name="pictureinsert"),

    # Data insertion
    path('update/', views.update, name="pictureupdate"),

    # Delete data
    path('delete/', views.delete, name="picturedelete"),

]
