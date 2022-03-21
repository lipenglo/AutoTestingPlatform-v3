"""BackService URL Configuration

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
# from django.urls import path
from django.conf.urls import url, include

import login.urls
import home.urls
import upLoad.urls
import routerPar.urls
import role.urls
import userManagement.urls
import info.urls
import ProjectManagement.urls
import PageManagement.urls
import FunManagement.urls
import WorkorderManagement.urls
import PageEnvironment.urls
import DebugTalk.urls
import GlobalVariable.urls
import SystemParams.urls
import Notice.urls
import DataBaseEnvironment.urls

import Api_IntMaintenance.urls
import Api_TestReport.urls
import Api_CaseMaintenance.urls
import Api_TimingTask.urls
import Api_BatchTask.urls

import Ui_ElementMaintenance.urls
import Ui_ElementEvent.urls
import Ui_CaseMaintenance.urls


urlpatterns = [
    # path('admin/', admin.site.urls),
    url('api/login/', include(login.urls)),
    url('api/home/', include(home.urls)),
    url('api/upLoad/', include(upLoad.urls)),
    url('api/router/', include(routerPar.urls)),
    url('api/role/', include(role.urls)),
    url('api/userManagement/', include(userManagement.urls)),
    url('api/info/', include(info.urls)),
    url('api/ProjectManagement/', include(ProjectManagement.urls)),
    url('api/PageManagement/', include(PageManagement.urls)),
    url('api/FunManagement/', include(FunManagement.urls)),
    url('api/WorkorderManagement/', include(WorkorderManagement.urls)),
    url('api/PageEnvironment/', include(PageEnvironment.urls)),
    url('api/DebugTalk/', include(DebugTalk.urls)),
    url('api/GlobalVariable/', include(GlobalVariable.urls)),
    url('api/SystemParams/', include(SystemParams.urls)),
    url('api/Notice/', include(Notice.urls)),
    url('api/DataBaseEnvironment/', include(DataBaseEnvironment.urls)),

    url('api/ApiIntMaintenance/', include(Api_IntMaintenance.urls)),
    url('api/ApiTestReport/', include(Api_TestReport.urls)),
    url('api/ApiCaseMaintenance/', include(Api_CaseMaintenance.urls)),
    url('api/ApiTimingTask/', include(Api_TimingTask.urls)),
    url('api/ApiBatchTask/', include(Api_BatchTask.urls)),

    url('api/UiElementMaintenance/', include(Ui_ElementMaintenance.urls)),
    url('api/UiElementEvent/', include(Ui_ElementEvent.urls)),
    url('api/UiCaseMaintenance/', include(Ui_CaseMaintenance.urls)),

]
