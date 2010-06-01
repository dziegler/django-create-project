from django.conf.urls.defaults import *
from django.contrib import admin
from django import template

template.add_to_builtins('django.templatetags.i18n')

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(user_admin.urls)),
)

try:
    from localsettings import *
    from django.conf import settings
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                    {'document_root': settings.MEDIA_ROOT}),
    )
except ImportError:
    pass
