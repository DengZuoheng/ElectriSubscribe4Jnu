from django.conf.urls import patterns, include, url
from django.contrib import admin
from subscriber import views
import trigger.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'server.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.form),
    url(r'^index/$',views.form),
    url(r'^form/$',views.form),
    url(r'^form/err/(\d+)$',views.form),
    url(r'^SubcribeAction/$',views.subcribe_action),
    url(r'^success/',views.success),
)
