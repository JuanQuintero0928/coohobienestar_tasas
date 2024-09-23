"""
URL configuration for coohobienestar_tasas project.

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
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, logout_then_login
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import Dashboard
from django.conf.urls import handler404
from django.shortcuts import render

# def custom_404(request, exception):
#     return render(request, '404.html', status=404)

# handler404 = 'coohobienestar_tasas.urls.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('', login_required(Dashboard.as_view()), name='dashboard'),
    path('informacion/', include(('dashboard.urls','informacion'))),  #Plantilla Principal de la base
    path('informacion/', include(('asociado.urls','asociado'))),
    path('parametro/', include(('parametro.urls','parametro'))),
    path('proceso/', include(('historico.urls','proceso'))),
    path('reportes/', include(('reporte.urls','reportes'))),

]
