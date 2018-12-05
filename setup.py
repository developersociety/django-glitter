#!/usr/bin/env python
from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.10',
    'django-mptt>=0.7',
    'django-mptt-admin>=0.3',
    'sorl-thumbnail>=12.2',
    'django-taggit>=0.21.3',
    'python-dateutil>=2.6.0',
]


setup(
    name='django-glitter',
    version='0.2.10',
    description='Glitter for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/developersociety/django-glitter',
    maintainer='The Developer Society',
    maintainer_email='studio@dev.ngo',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
    install_requires=install_requires,
)
