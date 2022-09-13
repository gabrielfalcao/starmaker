StarMaker
=========

Terraform bootstrapping and management tool

Makefile Targets
----------------

``make tests``
..............

Runs all tests.


``make unit``
.............

Runs unit tests.


``make functional``
...................

Runs functional tests.


``make black``
..............

Format code with black.


``make run``
.............

Executes the main command-line script.

``make release``
................

Builds the current version and pushes to pypi.


**Setting up a new python project**
-----------------------------------

1. Clone this repo.
2. Delete the git information: ``rm -rf .git``.
3. Customize the variables in the ``Makefile``.
4. Customize the variables in the ``setup.py``.
5. Customize the ``cover-package`` variable in ``setup.cfg``.
6. Adjust the initial version in ``starmaker/version.py``.
7. Rename the folder ``starmaker`` to a valid python module name.
8. Replace the contents of this file ``README.rst`` (format documentation `here <https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_).
9. Your project is ready for development, refer to the list of makefile targets above for more information.


**Configuring open-source license**
------------------------

1. Follow the `python packaging guide for licenses <https://packaging.python.org/tutorials/packaging-projects/#creating-a-license>`_.
2. Edit the file ``LICENSE`` with a copy of the license you chose as explained in the guide above.
3. Edit ``setup.py`` with the proper `trove classifiers <https://pypi.org/classifiers/>`_ for the chosen license.


**Making a new release**
------------------------

Before making a release, make sure to configure your `pypi credentials <https://workshop-from-your-editor-to-pypi.readthedocs.io/en/latest/pypirc-credentials.html>`_....

1. Set the new version in ``version.py``.
2. Add proper version changes in ``CHANGELOG.rst``.
3. run ``make release``.


**Adding docs**
---------------

I recommend using `Sphinx <https://www.sphinx-doc.org/en/master/>`_ for documenting your project.

Sphinx is the unspoken official tool for documentation in the python
ecosystem, it supports many plugins but the `Intersphinx
<https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html>`_
plugin is among the ones I find most useful because it creates a
binary file called ``objects.inv`` that allows other Sphinx-powered
documentation to make direct reference to the documentation of
internal python APIs.
