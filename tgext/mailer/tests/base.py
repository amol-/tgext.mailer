from tg.configuration import AppConfig
from tg.configuration import milestones
from tg.configuration import config
from tg import TGController, expose
from tgext.mailer import plugme
from webtest import TestApp


def configurator_with_mailer(options=None):
    if options is None:
        options = {}

    # Clear all previous mailer options
    for option in list(config.keys()):
        if option.startswith('mail.'):
            config.pop(option)

    milestones._reset_all()

    class RootController(TGController):
        @expose()
        def test(self):
            return 'HI!'

    app_cfg = AppConfig(minimal=True, root_controller=RootController())
    plugme(app_cfg, options)
    return app_cfg


def app_with_mailer(options=None, app_config=None):
    if app_config is None:
        app_config = {}

    app_cfg = configurator_with_mailer(options)
    app = app_cfg.make_wsgi_app(**app_config)
    return TestApp(app)
