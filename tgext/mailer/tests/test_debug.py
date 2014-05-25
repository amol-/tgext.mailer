import unittest
from .base import app_with_mailer
from tgext.mailer import get_mailer


class TestIncludemeDebug(unittest.TestCase):
    def test_includeme(self):
        from tgext.mailer.mailer import DebugMailer

        app = app_with_mailer({'debugmailer': True})
        self.assertEqual(get_mailer(None).__class__, DebugMailer)
