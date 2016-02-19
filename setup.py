#!/usr/bin/env python
from setuptools import find_packages, setup


install_requires = [
    'Django>=1.8,<1.9',
    'django-mptt>=0.7,<0.8',
    'django-mptt-admin>=0.3,<0.4',
    'sorl-thumbnail>=12.2',
]


setup(
    name='django-glitter',
    version='0.1',
    description='Glitter for Django',
    long_description=open('README.rst').read(),
    url='https://github.com/blancltd/django-glitter',
    maintainer='Blanc LTD',
    maintainer_email='studio@blanc.ltd.uk',
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='Proprietary',
    install_requires=install_requires,
)
