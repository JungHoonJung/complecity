Basic structure
================

.. contents:: Contents :
  :local:
  :depth: 2

Before we start
-----------------

You just did one step to the documentation.
For the first time, you need to learn about the syntax of rst(reStructuredText) syntax.
It is similar to Markdown, but a little bit different.
Here is a quick-start_ guide for this.

.. _quick-start: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html








Managing file with ``TOCtree``
------------------------------


If you create a new project, inside of the root folder will be only ``README.md``.
you can start your documentation project very fast through command ``sphinx-quickstart`` (For detail usage and options, See sphinx-quickstart_).
It will make a configuration and homepage with a simple format.
Now, assume that your system like below.

.. _ex1:
Example 1 (initializing) :
    your system :
        .. code-block::

            project/
                docs/
                    conf.py
                    index.rst
                    make.bat
                    Makefile

                README.md


.. _sphinx-quickstart: https://www.sphinx-doc.org/en/master/man/sphinx-quickstart.html

Each single file will be a page of your documentation.
So, you need to decide the tree-structure between the pages so-called '``TOCtree`` (Table Of Contents tree)'.
Every file in your documentation folder must be at ``TOCtree``.
If not, the ``sphinx``, the HTML compiler, won't compile that file with warning message.

.. _ex2:
Example 2 (``TOCtree``) :
    ``index.rst`` :
        .. code-block::

            .. toctree::
                :maxdepth: 2
                :caption: Contents:

                file1
                file2
                file3...



As you see above, there is specific syntax for making ``TOCtree`` for each page.
The *Directive* is its name (See :doc:`Directive` for more detail.).
``TOCtree`` will be compiled recursively, it means every file can contain ``TOCtree`` which file.

.. warning::
  If you set a file refer to file which already refers first one, ``sphinx`` will return recursion error.


When you write down the file name in ``TOCtree``, there needs only filename, not extension(i.e. .exe, .rst, .md, etc).
Moreover, you should use relative path for specifying the correct file.

.. _TOCtree: https://www.sphinx-doc.org/en/1.5/markup/toctree.html

.. _ex3:
Example 3 (recursively implemented) :
    your system :
        .. code-block::

            project/
                docs/
                    section1/
                        main.rst
                    section2/
                        main.rst
                    conf.py
                    section1.rst
                    section2.rst
                    index.rst
                    make.bat
                    Makefile

                README.md

    ``TOCtree`` :
        ``index.rst`` :
            .. code-block::

                .. toctree::
                    :maxdepth: 2
                    :caption: Contents:

                    section1
                    section2


        ``section1.rst`` :
            .. code-block::

                .. toctree::

                    section1/main

        ``section2.rst`` :
            .. code-block::

                .. toctree::

                    section2/main

    Schematic :
        .. code-block::

            'TOCtree' :
                index.rst
                    section1.rst
                        section1/main.rst
                    section2.rst
                        section2/main.rst

.. seealso::
    If you want to know ``TOCtree`` more, See TOCtree_documentation_.


.. _TOCtree_documentation: https://www.sphinx-doc.org/en/1.5/markup/toctree.html



Cross-referencing
------------------

When we read the Wikipedia, there are many hyperlinks to another pages or specific location of same page.
it is called *Cross-referencing* that will be explained into this section.

For example, You can go to :ref:`Basic structure` (header of this page), even :doc:`../index`.

Usage :
    .. code-block::

      :ref:`(header you want to go)`  Or link_

.. note::
    If you want to go another page, use ``:doc:`` rather than ``:ref:``
