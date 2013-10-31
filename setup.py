__author__ = 'elip'

from setuptools import setup

COSMO_CELERY_VERSION = "0.1.1"
COSMO_CELERY_BRANCH = "master"
COSMO_CELERY = "https://github.com/CloudifySource/cosmo-celery-common/tarball/{0}".format(COSMO_CELERY_BRANCH)

setup(
    name='cosmo-plugin-python-webserver',
    version='0.1.0',
    author='elip',
    author_email='elip@gigaspaces.com',
    packages=['python_webserver_installer'],
    license='LICENSE',
    description='Plugin for starting a simple python webserver on the localhost',
    install_requires=[
        "cosmo-celery-common"
    ],
    dependency_links=["{0}#egg=cosmo-celery-common-{1}".format(COSMO_CELERY, COSMO_CELERY_VERSION)]
)
