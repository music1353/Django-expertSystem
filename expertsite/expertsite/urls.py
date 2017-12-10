"""expertsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from expertapp.views import index, user, admin
from expertapp.views import list_database_ajax, user_symptom_ajax, admin_add_ajax, admin_del_ajax

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^index$', index),
    url(r'^user$', user),
    url(r'^admin$', admin),
    url(r'^list_database_ajax$', list_database_ajax),
    url(r'^user_symptom_ajax$', user_symptom_ajax),
    url(r'^admin_add_ajax$', admin_add_ajax),
    url(r'^admin_del_ajax$', admin_del_ajax)
]
