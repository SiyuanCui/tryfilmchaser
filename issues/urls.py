from django.urls import path, include
from . import views

urlpatterns = [
    # Background list page
    path('admin/list/', views.adminlist, name="issues_list"),
    # 后台评论人页面
    path('admin/author/', views.author, name="issues_author"),
    # 前台添加页面
    path('add/', views.add, name="issuesadd"),

    # Data insertion
    path('insert/', views.insert, name="issuesinsert"),

    # Data insertion
    path('update/', views.update, name="issuesupdate"),
    path('adminupdt/', views.adminupdt, name="adminupdt"),

    # Delete data
    path('delete/', views.delete, name="issuesdelete"),

]
