"""healthware URL Configuration

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
from django.urls.conf import include
from accounts import urls as acc_url
from functionality import urls as fun_url
from django_email_verification import urls as email_urls
from appointment import urls as appo_urls
from calling import urls as call_urls
from django.conf import settings
from django.conf.urls.static import static
from prescription import urls as pre_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include(acc_url)),
    path('functionality/', include(fun_url)),
    path('appointment/', include(appo_urls)),
    path('calling/', include(call_urls)),
    path('email/', include(email_urls)),
    path('prescription/', include(pre_urls)),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)