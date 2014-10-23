from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from registration.urls import urlpatterns


urlpatterns += patterns('',
    url(r'^login/$', auth_views.login,
        name='login', kwargs=dict(
            template_name='registration/login.html'
        )),
    url(r'^logout/$', auth_views.logout, 
        name='logout', kwargs=dict(
            template_name='registration/logout.html',
            next_page='/',
        )),
    url(r'^password/change/$', auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$', auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$', auth_views.password_reset,
        name='password_reset', kwargs=dict(
            post_reset_redirect='password_reset_done'
        )),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        name='password_reset_done'),
)
