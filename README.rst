Django Glitter
==============

Glitter is a front-end content management framework for Django.

Installation
~~~~~~~~~~~~

.. code-block:: sh

  pip install django-glitter


Contributing
~~~~~~~~~~~~

1. Fork it!
2. Create your feature branch: ``git checkout -b my-new-feature``
3. Commit your changes: ``git commit -am 'Add some feature'``
4. Push to the branch: ``git push origin my-new-feature``
5. Submit a pull request :D


Run Development Tests
~~~~~~~~~~~~~~~~~~~~~
To facilitate testing we use tox_, which you can install with:

.. code-block:: sh

  pip install tox

Currently we test on Python versions 2.7, 3.3, 3.4 & 3.5 and Django versions
1.8, 1.9 & 1.10.

To use the same test suite, make sure you have the above mentioned Python
interpreters installed, some platforms, like Ubuntu, won't have all versions
available in their default package repository and you may need to add 'custom'
repositories like Felix Krull's deadsnakes_. Depending on your development
platform you may need to add development tools and each of the python versions
development headers.

Assuming you have all the supported python versions installed and forked the
repository to `django-glitter` running the tests is a matter of:
  
.. code-block:: sh

  cd django-glitter
  tox


Credits
~~~~~~~

Concept and project launch by Team Blanc

License
~~~~~~~

Glitter is licensed under BSD-3


.. _tox: https://testrun.org/tox/latest/
.. _deadsnakes: https://launchpad.net/~fkrull/+archive/ubuntu/deadsnakes