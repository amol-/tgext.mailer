from tg import config
from tg.support.converters import asbool

import logging
log = logging.getLogger('tgext.mailer')

from tgext.mailer.mailer import Mailer, DebugMailer, DummyMailer


class SetupMailer(object):
    def __init__(self, options):
        self.options = options

    def _create_standard_mailer(self, config):
        return Mailer.from_settings(config, prefix='mail.')

    def _create_dummy_mailer(self, config):
        return DummyMailer()

    def _create_debug_mailer(self, config):
        import os
        path = os.path.join(os.getcwd(), 'mail')
        return DebugMailer(path)

    def __call__(self, app):
        try:
            # If specified on plugtime, force the specified one
            # useful for tests or scripts.
            using_debugmailer = self.options['debugmailer']
        except KeyError:
            # Otherwise use the option provided in configuration file.
            using_debugmailer = config.get('mail.debugmailer', False)

        if using_debugmailer == 'dummy':
            mailer_factory = self._create_dummy_mailer
        elif asbool(using_debugmailer):
            mailer_factory = self._create_debug_mailer
        else:
            mailer_factory = self._create_standard_mailer

        config['tg.app_globals']._mailer_factory = mailer_factory

        global_mailer = mailer_factory(config)
        config['tg.app_globals']._mailer = global_mailer

        log.info('Configured %s', global_mailer.__class__.__name__)
        return app


class RequestMailerAppWrapper(object):
    def __init__(self, dispatcher, config):
        self.dispatcher = dispatcher

    def __call__(self, controller, environ, context):
        context.request._mailer = context.app_globals._mailer_factory(context.config)
        return self.dispatcher(controller, environ, context)
