from django.conf import settings
from django.views.generic import TemplateView


class PrivateBetaMiddleware(object):
    """
    Add this to your ``MIDDLEWARE_CLASSES`` make all views except for
    those in the account application require that a user be logged in.
    This can be a quick and easy way to restrict views on your site,
    particularly if you remove the ability to create accounts.
    **Settings:**
    ``EARLYBIRD_ENABLE``
    Whether or not the beta middleware should be used. If set to `False`
    the PrivateBetaMiddleware middleware will be ignored and the request
    will be returned. This is useful if you want to disable early bird
    on a development machine. Default is `True`.
    """

    def __init__(self):
        self.enable_beta = settings.EARLYBIRD_ENABLE

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated() or not self.enable_beta:
            # User is logged in, no need to check anything else.
            return

        whitelisted_modules = ['django.contrib.auth.views', 'django.views.static', 'django.contrib.admin.sites']
        if '%s' % view_func.__module__ in whitelisted_modules:
            return
        else:
            return TemplateView.as_view(template_name='earlybird.html')(request)
