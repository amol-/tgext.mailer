import unittest
from .base import app_with_mailer
from tg import config
from tgext.mailer import get_mailer


class TestGetMailer(unittest.TestCase):
    def test_arg_is_missing(self):
        app = app_with_mailer()
        resp = app.get('/test')

        mailer = get_mailer(None)
        self.assertEqual(mailer, config['tg.app_globals']._mailer)
        self.assertNotEqual(mailer, resp.req._mailer)

    def test_arg_is_request(self):
        app = app_with_mailer()
        resp = app.get('/test')

        result = get_mailer(resp.req)
        self.assertEqual(result, resp.req._mailer)
        self.assertNotEqual(result, config['tg.app_globals']._mailer)

    def test_different_requests_got_different_mailers(self):
        app = app_with_mailer()

        resp1 = app.get('/test')
        mailer1 = get_mailer(resp1.req)

        resp2 = app.get('/test')
        mailer2 = get_mailer(resp2.req)

        self.assertNotEqual(mailer1, mailer2)


class TestConfigurationOptions(unittest.TestCase):
    def test_with_default_prefix(self):
        settings = {'mail.default_sender': 'sender'}

        app = app_with_mailer(None, settings)

        mailer = get_mailer(None)
        self.assertEqual(mailer.default_sender, 'sender')

