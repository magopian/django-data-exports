Django-data-exports
===================

Django-data-exports is a model data exports app for Django. It allows you to easily
create exports for your models.

Adding this app to your project will let you create exports for your models,
and customize the data that will be exported by specifying which columns to include,
and which format to use.

Typical use case: display a few columns from one of your models as a HTML table to
be easily copy/pasted to a spreadsheet.

* Author: Mathieu Agopian and `contributors`_
* Licence: BSD
* Compatibility: Django 1.3+ (class-based-views required)
* Requirements: django-inspect-model
* Documentation: http://django-data-exports.readthedocs.org/en/latest/

.. _contributors: https://github.com/magopian/django-data-exports/contributors


Contributing
------------

Get the code:

::

    git clone https://github.com/magopian/django-data-exports.git
    cd django-data-export
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .

Install the development requirements:

::

    pip install -r test_requirements.txt

Run the tests:

::

    DJANGO_SETTINGS_MODULE=data_exports.test_settings make test
