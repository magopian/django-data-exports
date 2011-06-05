# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

import data_exports


setup(
    name='django-data-exports',
    version=data_exports.__version__,
    author=u'Mathieu agopian',
    author_email='mathieu.agopian@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/magopian/django-data-exports',
    license='BSD licence, see LICENCE file',
    description='Model data exports for Django',
    long_description=open('README.rst').read(),
    install_requires=[
        'Django>=1.3',
        'django-inspect-model',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    zip_safe=False,
)
