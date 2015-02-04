__version__ = '0.1.0-alpha+01'
default_app_config = 'wagtailbakery.apps.WagtailBakeryAppConfig'

from django import get_version
if '1.7' > get_version():
    from . import signal_handlers
    signal_handlers.register_signal_handlers()
