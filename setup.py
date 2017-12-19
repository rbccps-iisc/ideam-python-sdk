from distutils.core import setup
import os
install_requires = ['chardet', 'multidict>=3.0.0',
                    'async_timeout>=1.2.0', 'yarl>=0.11', 'aiohttp>=2.3.0']


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

setup(
  name='ideam',
  packages=['ideam'],
  version='0.0.1',
  long_description='\n\n'.join((read('README.rst'), read('CHANGES.rst'))),
  description='Python SDK for IoT Data Exchange & Analytics Middleware',
  author='Harish Anand',
  author_email='smartcity@rbccps.org',
  url='https://github.com/rbccps-iisc/ideam-python-sdk',
  download_url='https://github.com/rbccps-iisc/ideam-python-sdk/archive/0.0.1.tar.gz',
  keywords=['IoT', 'smartcity', 'ideam'],
  license="ISC",
  python_requires='>=3.5.4',
  install_requires=install_requires,
  classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Topic :: Internet",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: ISC License (ISCL)",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS",
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)