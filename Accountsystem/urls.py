"""
URL configuration for Accountsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from Accountapp import views
from Accountsystem import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.showresult, name="submitfile"),
    path("form", views.home, name="home"),
    path("submit/", views.accounting_form, name="accounting"),
    path("submitfile/", views.showresult, name="submitfile"),
    path("editfile/<int:id>", views.edit, name="editfile"),
    path("deletefile/<int:id>", views.deleterecord, name="deletefile"),
    path("updatefile", views.ufile, name="updatefile"),
    path("summaryfile/<str:selected_date>", views.summary, name="summaryfile"),
    path("summarytable", views.tsummary, name="summarytable"),
    path("get_subheads/", views.get_subheads, name="get_subheads"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
