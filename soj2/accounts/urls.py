from django.conf.urls.defaults import *

from registration.views import register, activate

urlpatterns = patterns("",
                       url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'members/forgotten_password.html', 'email_template_name':'members/password_reset_email.html', 'post_reset_redirect' : '/members/password-reset/done/'}, name="password-reset"),
                       url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name' : 'members/forgotten_password_done.html',}, name="password-reset-done"),
                       url(r'^password-reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',{ 'template_name': 'members/password_reset_confirm.html', 'post_reset_redirect' : '/members/password-reset/confirm/done/'}, name="password-reset-confirm"),
                       url(r'^password-reset/confirm/done/$','django.contrib.auth.views.password_reset_complete',{ 'template_name': 'members/password_reset_confirm_done.html' }, name="password-reset-confirm-done"),
                       url(r'^login/$', 'django.contrib.auth.views.login', {'template_name' : 'members/login.html'}, name="login"),
                       url(r'^logout/$', 'mcnulty.pages.views.logout_view', name="logout"),
                       url(r'^permission-denied/$', 'django.views.generic.simple.direct_to_template', {'template': 'permission_denied.html'}, name="permission-denied"),
                       url(r'^register/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/register-done.html'}, name='register-done'),
                       url(r'^activate/done/$', 'django.views.generic.simple.direct_to_template', {'template': 'accounts/activate-done.html'}, name='activate-done'),
)

urlpatterns += patterns("registration.views",
               url(r'^activate/(?P<activation_key>\w+)/$', activate, {
                      'success_url' : 'accounts:activate-done',
                    'backend': 'soj2.accounts.backend.Soj2Backend',
                    'template_name' : 'accounts/activate.html',},
                   name='activate'),
               url(r'^register/$', register, {
                      'success_url' : 'accounts:register-done',
                      'backend': 'soj2.accounts.backend.Soj2Backend', 
                      'template_name' : 'accounts/register.html'},
                  name='register'),)