"""reciation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reciation import views
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('addwords/', views.addwords, name='addwords'),
    url(r'^$', views.home,name='home'),
    path('display/', views.display, name='display'),
    path('delete/',views.delete,name="delete"),
    path('ediWords/',views.ediWords,name="ediWords"),
    path('spell/',views.spell,name="spell"),
    path('check/',views.check, name="check"),
    path('recite/',views.recite,name="recite"),
    path('printList',views.printList,name="printList"),
    path('recite1d',views.one_day_words_recite,name="recite1"),
    path('spell1d',views.one_day_words_spell,name="spell1"),
]
