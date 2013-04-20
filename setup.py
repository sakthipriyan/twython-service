from setuptools import setup
from setuptools import find_packages

__author__ = 'Sakthi Priyan H <sakthipriyans@gmail.com>'
__version__ = '0.0.1'

setup(
    # Basic package information.
    name='twython_service',
    version=__version__,
    packages=find_packages(),

    # Packaging options.
    include_package_data=True,

    # Package dependencies.
    install_requires=['twython>=2.5.4'],

    # Metadata for PyPI.
    author='Sakthi Priyan H',
    author_email='sakthipriyans@gmail.com',
    license='Apache License, Version 2.0',
    url='https://github.com/spriyan/twython-service',
    keywords='twitter api tweet twython service',
    description='Twython Service adds another level of abstraction while posting tweets via Twython.',
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License v2',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
        'Topic :: Internet'
    ]
)