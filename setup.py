#!/usr/bin/env python
from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.9',
    'django-mptt>=0.7,<0.9',
    'django-mptt-admin>=0.3',
    'sorl-thumbnail>=12.2',
]


setup(
    name='django-glitter',
    version='0.1.13',
    description='Glitter for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/django-glitter',
    maintainer='Blanc Ltd',
    maintainer_email='studio@blanc.ltd.uk',
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
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='BSD',
    install_requires=install_requires,
)
