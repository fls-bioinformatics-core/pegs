***************
Getting started
***************

Running ``PEGS`` requires:

* The ``PEGS`` Python package, and
* The ``bedtools`` program from ``BEDTools2``

Installing PEGS from PyPI using virtualenv and pip
==================================================

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

    pip install pegs

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
   encounter any errors when installing or running the software.

.. note::

   If installing PEGS on Mac OS X it is possible that you will
   get an error at runtime relating to Python not being installed
   as a framework; in this case please try reinstalling PEGS using
   the workaround in :doc:`known problems section <known_problems>`.

Installing PEGS using Conda
===========================

Another approach for installing ``PEGS`` to use
`Conda <http://conda.pydata.org/docs/>`__ (most easily obtained via
the `Miniconda Python distribution <http://conda.pydata.org/miniconda.html>`__).

Once you have Conda installed you can create a new Conda environment
with ``PEGS`` installed using the following command:

::

   conda create -c bioconda -c conda-forge -n pegs pegs

Alternatively you can install ``PEGS`` into an existing Conda
environment using:

::

   conda install -c bioconda -c conda-forge pegs

.. warning::

   We recommend installing ``PEGS`` into a new Conda environment to
   avoid issues with incompatible packages, which has been observed
   for example when trying to install directly into the base Conda
   distribtion.

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
