import unittest
from .base import app_with_mailer
from tgext.mailer import get_mailer


class TestIncludemeDebug(unittest.TestCase):
    def test_includeme(self):
        from tgext.mailer.mailer import DummyMailer

        app = app_with_mailer({'debugmailer': 'dummy'})
        self.assertEqual(get_mailer(None).__class__, DummyMailer)
