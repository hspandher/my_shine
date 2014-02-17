from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'my_shine.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'mini_shine.views.home'),
    url(r'register/', 'mini_shine.views.register'),
    url(r'^candidate/(\d{1,10})/add-work-experience/$', 'mini_shine.views.add_work_experience')
)
