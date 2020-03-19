**************
Known Problems
**************

The following sections detail the known problems with ``PEGS``
along with recommended solutions, where they exist.

Installation problems
=====================

* :ref:`install_problem_numpy_dtype_size`
* :ref:`install_problem_python27_virtualenv_setuptools`

.. _install_problem_numpy_dtype_size:

"numpy.dtype size changed"
--------------------------

Errors about ``numpy.dtype size changed, may indicate binary incompatibility``:
it's recommended to reinstall the ``scipy`` package using the
``--no-binary`` option of ``pip``, i.e.:

::

    pip uninstall scipy
    pip install --no-binary scipy scipy==1.1.0

See https://stackoverflow.com/a/25753627/579925 for more details.

.. _install_problem_python27_virtualenv_setuptools:

"ERROR: Package 'setuptools' requires a different Python: 2.7.12 not in '>=3.5'"
--------------------------------------------------------------------------------

This error has been observed when using Python 2.7 and installing
``PEGS`` using ``virtualenv`` as described in the
:doc:`installation documentation <install>`:

::

   ERROR: Package 'setuptools' requires a different Python: 2.7.12 not in '>=3.5'

This appears to be a problem with the ``virtualenv`` initialisation
pulling in a version of the ``setuptools`` package which is not
compatible with Python 2.7.

In this case it's recommended to try the following procedure to set up
the Python virtual environment:

::

    virtualenv --no-setuptools -p python2.7 venv.pegs
    source venv.pegs/bin/activate
    pip install setuptools

which should then have the correct version of ``setuptools``.

``PEGS`` can then be installed using e.g.:

::

   pip install pegs-0.1.0.tgz

as before.
