try:
    # Try using ez_setup to install setuptools if not already installed.
    from ez_setup import use_setuptools
    use_setuptools()
except ImportError:
    # Ignore import error and assume Python 3 which already has setuptools.
    pass

from setuptools import setup, find_packages

classifiers = ['Development Status :: 4 - Beta',
               'Operating System :: POSIX :: Linux',
               'Operating System :: MacOS :: MacOS X',
               'Operating System :: Microsoft :: Windows',
               'License :: OSI Approved :: MIT License',
               'Intended Audience :: Developers',
               'Programming Language :: Python :: 3',
               'Topic :: Software Development',
               'Topic :: System :: Hardware']

dlink = []
ireq = []


setup(name              = 'miniot_hts',
      version           = '0.8',
      author            = 'Atsushi Shibata',
      author_email      = 'shibata@m-info.co.jp',
      description       = 'A library to control Humid Temperature Sensor DHT11.',
      license           = 'MIT',
      classifiers       = classifiers,
      url               = 'https://github.com/shibats/miniot_hts/',
      dependency_links  = dlink,
      install_requires  = ireq,
      packages          = find_packages(),
      zip_safe          = False)
