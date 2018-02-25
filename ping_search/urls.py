
from django.conf.urls import include, url
from django.contrib import admin
import debug_toolbar
urlpatterns = [

    url(r'^admin/', admin.site.urls),
    url(r'^__debug__/', include(debug_toolbar.urls)),
    url(r'^', include('search.urls')),
]
