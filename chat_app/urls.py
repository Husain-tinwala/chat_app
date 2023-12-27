from django.contrib import admin
from django.urls import path
from app.views import index,chat_page
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name = 'home'),
    path('chat/<str:username>/',chat_page,name ='chat')
]
