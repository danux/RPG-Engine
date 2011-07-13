from django.conf.urls.defaults import *

from registration.views import register, activate


urlpatterns = patterns("",
        url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'accounts/login.html'}, name="login"),
        url(r'^register/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/register-done.html'}, name='register-done'),
        url(r'^activate/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/activate-done.html'}, name='activate-done'),
        url(r'^change-password/done/$', 'django.contrib.auth.views.password_change_done', {'template_name' : 'accounts/change-password-done.html'}, name="change-password-done"),
        url(r'^change-password/$', 'django.contrib.auth.views.password_change', {'template_name' : 'accounts/change-password.html', 'post_change_redirect' : 'done/'}, name="change-password"),
        url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', {'template_name' : 'accounts/password-reset.html', 'post_reset_redirect' : 'done/', 'email_template_name' : 'accounts/emails/password-reset.txt'}, name="password-reset"),
        url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name' : 'accounts/password-reset-done.html'}, name="password-reset-done"),
        url(r'^password-reset-confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name' : 'accounts/password-reset-confirm.html', 'post_reset_redirect' : '/accounts/password-reset-complete/'}, name="password-reset-confirm"),
        url(r'^password-reset-complete/$', 'django.contrib.auth.views.password_reset_complete', {'template_name' : 'accounts/password-reset-complete.html'}, name="password-reset-complete"),
)

urlpatterns += patterns("registration.views",
        url(r'^activate/(?P<activation_key>\w+)/$', activate, {
                'success_url' : 'accounts:activate-done',
                'backend': 'rpgengine.accounts.backend.RPGEngineBackend',
                'template_name' : 'accounts/activate.html',},
                name='activate'),
        url(r'^register/$', register, {
                 'success_url' : 'accounts:register-done',
                 'backend': 'rpgengine.accounts.backend.RPGEngineBackend', 
                 'template_name' : 'accounts/register.html'},
                 name='register'),)

urlpatterns += patterns("rpgengine.accounts.views",
                        url(r'^$', 
                            'my_account',
                            name="my-account"),
                        url(r'^update-profile/$', 
                            'update_profile',
                            name="update-profile"),)
                        