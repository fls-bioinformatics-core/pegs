**************
Known Problems
**************

"numpy.dtype size changed"
==========================

Errors about ``numpy.dtype size changed, may indicate binary incompatibility``:
it's recommended to reinstall the ``scipy`` package using the
``--no-binary`` option of ``pip``, i.e.:

::

    pip uninstall scipy
    pip install --no-binary scipy scipy==1.1.0

See https://stackoverflow.com/a/25753627/579925 for more details.
