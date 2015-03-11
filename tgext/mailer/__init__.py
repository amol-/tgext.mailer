from tg import config
from .message import Attachment, Message


def plugme(configurator, options=None):
    if options is None:  # pragma: no cover
        options = {}

    from tg.configuration import milestones
    from .plugmailer import SetupMailer, RequestMailerAppWrapper

    milestones.environment_loaded.register(SetupMailer(configurator, options))
    configurator.register_wrapper(RequestMailerAppWrapper)
    
    return dict(appid='tgext.mailer')


def get_mailer(request):
    if request is None:
        return config['tg.app_globals']._mailer
    else:
        return request._mailer


__all__ = ['Attachment', 'Message', 'get_mailer', 'plugme']
