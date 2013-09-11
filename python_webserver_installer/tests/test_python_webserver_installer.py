import unittest

__author__ = 'elip'

from python_webserver_installer.tasks import start


class WebserverInstallerTestCase(unittest.TestCase):

    def test_start(self):
        start('_test_id')

