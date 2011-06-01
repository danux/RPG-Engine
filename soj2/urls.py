from django.conf.urls.defaults import *
from mcnulty.urls import *

urlpatterns += patterns("registration.views",
                       url(r'^accounts/activate/(?P<activation_key>\w+)/$', 'activate', 
                           {
                            'backend': 'registration.backends.default.DefaultBackend',
                            'template_name' : 'registration/activate.html'
                            },
                           name='registration_activate_two'),
)

urlpatterns += patterns("",
                       url(r"^members/", include("aptuk.members.urls")),
                       url(r'^captcha/', include('captcha.urls')),
                       url(r"^", include("mcnulty.pages.urls")),
)