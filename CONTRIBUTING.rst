============
Contributing
============

You can contribute in many ways:

Report Bugs
-----------

Report bugs at https://github.com/fls-bioinformatics-core/pegs/issues.

If you are reporting a bug, please include:

* Your operating system name and version, and the version of PEGS.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Write Documentation
~~~~~~~~~~~~~~~~~~~

Ephemeris could always use more documentation, whether as part of the
official Ephemeris docs, in docstrings, or even on the web in blog posts,
articles, and such.

User documentation
+++++++++++++++++++
User documentation is (partly) automated to contain the first docstring in a
module and the usage based on the parser object.

If you want to contribute to the user documentation you can edit the docstring or the parser module
or write more information in the commands .rst file. (See galaxy-wait for an example.)

When you add a new command line tool in ephemeris you can add documentation as follows:

1. Go to the source file and:

  * Add a docstring that gives general information about the module. (Examples in shed-install and run-data-managers)
  * Create a new _parser() method that returns the argument parser.

2. Create a new rst file using shed-install.rst or run-data-managers.rst as a template.
3. Reference the new rst file in commands.rst

To build your documentation to check out how it works before submitting the pull request:
1. Install sphinx in a virtual environment by running `pip install -r docs/requirements.txt` from ephemeris root
2. go to the docs directory and run `make html`

Submit Feedback
---------------

The best way to send feedback is to file an issue at
https://github.com/fls-bioinformatics-core/pegs/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.

Fix Bugs Or Implement Features
------------------------------

To contribute code to fix bugs or implement new features in PEGS:

1. Fork the ``pegs`` repository on GitHub.

   2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/pegs.git

3. Install your local copy into a Python virtualenv.
   
4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request against the ``devel`` branch
   through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. Pull requests should be made against the ``devel`` branch.
2. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring.
