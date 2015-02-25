try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'SearchEngine',
    'author': 'Tyler Creller',
    'url': 'https://github.com/tylercreller',
    'download_url': 'https://github.com/tylercreller.',
    'author_email': 'tylercreller@yahoo.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)