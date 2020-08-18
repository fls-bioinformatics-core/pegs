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

    pip install pegs-0.3.0.tgz

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

``PEGS`` uses the ``bedtools`` program from the ``BEDTools2``
package to generate the overlaps for the enrichment calculations.

If ``bedtools`` is not available when ``PEGS`` is run then ``PEGS``
will attempt to download and install it in the user's home area,
under:

::

   ${HOME}/.pegs/bin/

Subsequently runs of ``PEGS`` will use this version of ``bedtools``
if no other versions can be found.

Alternatively ``bedtools`` can to be installed separately and then
made available on the user's ``PATH`` at runtime.

For example for a Linux system:

::

   wget https://github.com/arq5x/bedtools2/releases/download/v2.29.2/bedtools.static.binary
   mv bedtools.static.binary bedtools
   chmod a+x bedtools

See https://bedtools.readthedocs.io/en/latest/content/installation.html
for more information on how to install BEDTools2.
