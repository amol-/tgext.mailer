from tg import config
from .message import Attachment, Message


def plugme(configurator, options=None):
    if options is None:  # pragma: no cover
        options = {}

    from tg import hooks
    from .plugmailer import SetupMailer, RequestMailerAppWrapper

    if hasattr(configurator, 'register_wrapper'):
        # TG2.3
        hooks.register('before_config', SetupMailer(options))
        configurator.register_wrapper(RequestMailerAppWrapper)
    else:
        # TG2.4+
        hooks.register('before_wsgi_middlewares', SetupMailer(options))
        configurator.register_application_wrapper(RequestMailerAppWrapper)
    
    return dict(appid='tgext.mailer')


def get_mailer(request):
    if request is None:
        return config['tg.app_globals']._mailer
    else:
        return request._mailer


__all__ = ['Attachment', 'Message', 'get_mailer', 'plugme']
