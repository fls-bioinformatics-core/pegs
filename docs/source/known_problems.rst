**************
Known Problems
**************

The following sections detail the known problems with ``PEGS``
along with recommended solutions, where they exist.

Installation problems
=====================

* :ref:`install_problem_numpy_dtype_size`
* :ref:`install_problem_python27_virtualenv_setuptools`


Runtime problems
================

* :ref:`runtime_problem_macosx_python_not_installed_as_framework`

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

.. _runtime_problem_macosx_python_not_installed_as_framework:

"RuntimeError: Python is not installed as a framework" (Mac OS X)
-----------------------------------------------------------------

Under Mac OS X ``PEGS`` may appear to install without any issues but
then fail at runtime with an error like:

::

    RuntimeError: Python is not installed as a framework. The Mac OS X
    backend will not be able to function correctly if Python is not
    installed as a framework. See the Python documentation for more
    information on installing Python as a framework on Mac OS X. Please
    either reinstall Python as a framework, or try one of the other
    backends. If you are using (Ana)Conda please install python.app and
    replace the use of 'python' with 'pythonw'. See 'Working with
    Matplotlib on OSX' in the Matplotlib FAQ for more information.

This message is preceeded by errors coming from the ``matplotlib``
Python library.

A workaround for this problem is to use a combination of ``conda``
and ``pip``:

::

   conda create -n pegs python=3.6 matplotlib=2.2.3
   conda activate pegs
   pip install pegs-0.3.0.tgz

Essentially this uses a ``conda`` environment instead of a Python
``virtualenv``.

If you are not familiar with ``conda`` then see:

* https://docs.conda.io/projects/conda/en/latest/index.html

Instructions for installing ``conda`` on Mac OS are available
here:

* https://docs.conda.io/projects/conda/en/latest/user-guide/install/macos.html
