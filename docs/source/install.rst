***************
Getting started
***************

Running ``PEGS`` requires:

* The ``PEGS`` Python package, and
* The ``bedtools`` program from ``BEDTools2``

Installing PEGS
===============

The recommended way to get started with ``PEGS`` is to create a
Python virtual environment, and then install the software using
the ``pip`` utility.

For example: to create and activate a virtual environment called
``venv.pegs`` using the ``virtualenv`` utility:

::

    virtualenv venv.pegs
    source venv.pegs/bin/activate

The ``PEGS`` package can then be installed using ``pip``, for
example:

::

    pip install pegs-0.1.0.tgz

which will make the ``pegs`` and ``mk_pegs_intervals`` utilities
available.

.. note::

   If using PEGS from a virtual environment, make sure to
   activate the environment each time before using it:

   ::

       source venv.pegs/bin/activate

   To deactive the virtual environment afterwards, do ``deactivate``.

.. note::

   PEGS is compatible with both Python2 and Python3; please
   check :doc:`known problems section <known_problems>` if you
   encounter any errors when installing the software.

Installing BEDTOOLS
===================

``PEGS`` uses the ``bedtools intersect`` function from the ``BEDTools2``
package.

This needs to be installed separately and then made available on
your ``PATH`` at runtime.

See https://bedtools.readthedocs.io/en/latest/content/installation.html
for information on how to obtain and install BEDTools2.
