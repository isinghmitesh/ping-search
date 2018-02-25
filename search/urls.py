from django.conf.urls import url
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^product/$', views.search, name='search'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^surprise/$', views.surprise, name='surprize'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy'),
    url(r'^base/$', views.base, name='base'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="search/robots.txt", content_type="text/plain"),
        name="robots_file")

]


