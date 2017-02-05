from setuptools import setup, find_packages
import sys, os

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
except IOError:
    README = ''

version = "0.2.0"

test_requirements = [
  'nose',
  'webtest',
]

setup(name='tgext.mailer',
      version=version,
      description="TurboGears extension for sending emails with transaction manager integration",
      long_description=README,
      classifiers=[
        "Environment :: Web Environment",
        "Framework :: TurboGears"
      ],
      keywords='turbogears2.extension',
      author='Alessandro Molina',
      author_email='amol@turbogears.org',
      url='https://github.com/amol-/tgext.mailer',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tgext.mailer.tests']),
      namespace_packages = ['tgext'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "TurboGears2 >= 2.3.2",
          "repoze.sendmail == 4.3",
      ],
      extras_require={
           # Used by Travis and Coverage due to setup.py nosetests
           # causing a coredump when used with coverage
           'testing': test_requirements,
      },
      test_suite='nose.collector',
      tests_require=test_requirements,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
