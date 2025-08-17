"""
URL configuration for conduit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

import django_components
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# Register custom components
from conduit.components import nav as _nav  # noqa: F401
from hsds.components import contact_form as _contact_form  # noqa: F401
from hsds.components import address_form as _address_form  # noqa: F401
from hsds.components import location_form as _location_form  # noqa: F401
from hsds.components import organization_form as _organization_form  # noqa: F401
from hsds.components import phone_form as _phone_form  # noqa: F401
from hsds.components import schedule_form as _schedule_form  # noqa: F401
from hsds.components import service_form as _service_form  # noqa: F401
from hsds.urls import api_router

django_components.autodiscover()


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("pulse/", include("pulse.urls")),
    path("management/", TemplateView.as_view(template_name="management/dashboard.html"), name="management-dashboard"),
    path("api/v1/", include(api_router.urls)),
    path("api/", include("resources.urls")),
    path("", include("hsds.urls")),
    path("", include("django_components.urls")),
]
