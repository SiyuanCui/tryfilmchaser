from django.urls import path, include
from . import views

urlpatterns = [
    path('sh/', views.sh, name="sh"),
    path('checkno/', views.checkno, name='checkno'),
    path('upload/', views.UploadFile, name="uploadFile"),
    path('selectUpdateSearch/', views.selectUpdateSearch),
    path('captcha/', views.captcha),
    path('mod/', views.mod),

]
