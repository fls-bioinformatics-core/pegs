***************
Getting started
***************

The recommended way to get started with ``PEGS`` is to create a
Python virtual environment, and then install the software using
the ``pip`` utility.

For example: to create and activate a virtual environment called
``venv.pegs`` using the ``virtualenv`` utility:

::

    virtualenv venv.pegs
    source venv.pegs/bin/activate

``PEGS`` package can then be installed using ``pip``, for example:

::

    pip install pegs-0.1.0.tgz

This will make the ``pegs`` and ``mk_pegs_intervals`` utilities
available.

.. note::

   If using PEGS from a virtual environment, make sure to
   activate the environment each time before using it:

   ::

       source venv.pegs/bin/activate

   To deactive the virtual environment afterwards, do ``deactivate``.

``PEGS`` also requires the ``intersectBed`` program from ``BEDTools``, 
which needs to be installed separately and made available on ``PATH``
at runtime.

See https://bedtools.readthedocs.io/en/latest/content/installation.html
for information on how to obtain and install BEDTools.
