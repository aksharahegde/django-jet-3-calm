================================
Django JET Calm (for Django-4)
================================

Rebooted version of https://github.com/geex-arts/django-jet#readme

**Modern template for Django-4 admin interface with improved functionality**

**MAJOR UPGRADE**
  * Latest jQuery and jQuery-UI
  * Multiselect dropdown in list filter

.. image:: https://raw.githubusercontent.com/geex-arts/jet/static/logo.png

Django JET has two kinds of licenses: open-source (AGPLv3) and commercial. Please note that using AGPLv3
code in your programs make them AGPL compatible too. So if you don't want to comply with that we can provide you a commercial
license (visit Home page). The commercial license is designed for using Django JET in commercial products
and applications without the provisions of the AGPLv3.

* Documentation: http://jet.readthedocs.org/ (Old official version)
* libi.io http://libi.io/library/1683/django-jet (Old official version)
* PyPI: https://pypi.python.org/pypi/django-jet (Old official version)

Why Django JET?
===============

* New fresh look
* Responsive mobile interface
* Useful admin home page
* Minimal template overriding
* Easy integration
* Themes support
* Autocompletion
* Handy controls

Screenshots
===========

.. image:: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen1_720.png
    :alt: Screenshot #1
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen1.png
    
.. image:: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen2_720.png
    :alt: Screenshot #2
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen2.png
    
.. image:: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen3_720.png
    :alt: Screenshot #3
    :align: center
    :target: https://raw.githubusercontent.com/geex-arts/django-jet/static/screen3.png

Installation
============

* Download and install the Django 4 version of Django JET:

.. code:: python

    pip install git+https://github.com/aksharahegde/django-jet-3-calm.git#<version>
    # or
    pip install git+https://github.com/aksharahegde/django-jet-3-calm.git@<branch_name>

* Add 'jet' application to the INSTALLED_APPS setting of your Django project settings.py file (note it should be before 'django.contrib.admin'):

.. code:: python

    INSTALLED_APPS = (
        ...
        'jet',
        'django.contrib.admin',
    )
        
* Make sure ``django.template.context_processors.request`` context processor is enabled in settings.py:

.. code:: python

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    ...
                    'django.template.context_processors.request',
                    ...
                ],
            },
        },
    ]

* Add URL-pattern to the urlpatterns of your Django project urls.py file (they are needed for related–lookups and autocompletes):

.. code:: python

    urlpatterns [
        '',
        path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
        path('admin/', include(admin.site.urls)),
        ...
    ]

* Create database tables:

.. code:: python

    python manage.py migrate jet
    # or 
    python manage.py syncdb
        
* Collect static if you are in production environment:

.. code:: python

        python manage.py collectstatic
        
* Clear your browser cache

Dashboard installation
======================

.. note:: Dashboard is located into a separate application. So after a typical JET installation it won't be active.
          To enable dashboard application follow these steps:

* Add 'jet.dashboard' application to the INSTALLED_APPS setting of your Django project settings.py file (note it should be before 'jet'):

.. code:: python

    INSTALLED_APPS = (
        ...
        'jet.dashboard',
        'jet',
        'django.contrib.admin',
        ...
    )

* Add URL-pattern to the urlpatterns of your Django project urls.py file (they are needed for related–lookups and autocompletes):

.. code:: python

    urlpatterns [
        '',
        path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
        path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
        path('admin/', include(admin.site.urls)),
        ...
    ]

.. warning::
    From Django 3.0 the default value of the ``X_FRAME_OPTIONS`` setting was changed from ``SAMEORIGIN`` to ``DENY``. This       can cause errors for popups such as for the ``Field Lookup Popup``. To solve this you should add the following to your       Django project settings.py file:
    
.. code:: python
        
        X_FRAME_OPTIONS = 'SAMEORIGIN'
        

* **For Google Analytics widgets only** install python package:

.. code::

    pip install google-api-python-client==1.4.1

* Create database tables:

.. code:: python

    python manage.py migrate dashboard
    # or
    python manage.py syncdb

* Collect static if you are in production environment:

.. code:: python

        python manage.py collectstatic




![Alt](https://repobeats.axiom.co/api/embed/07083dcb52203db7d4a60a26ca66001a3cdde9de.svg "Repobeats analytics image")
