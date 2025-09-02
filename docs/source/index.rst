.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Classes:

  Classes <classes>

.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Modules:

  modules <modules>

.. toctree::
  :hidden:
  :maxdepth: 2
  :caption: Recipes:

  first_example <example_analysis>

Overview
========

| GitHub: https://www.github.com/matteobecchi/graph_time_series

| Maintainer: `matteobecchi <https://github.com/matteobecchi/>`_

The ``graph-time-series`` python package offers a collection of tools to compute
graph-related quantities on graphs and, in particular, on time-series of graphs.
It is based on the ``networkx`` package for the graph implementation.

Installation
============

Clone this repository on your machine and run::

    $ pip install -e .

Developer Setup
---------------

#. Install `just`_.
#. In a new virtual environment run::

    $ just dev

#. Run code checks::

    $ just check

.. _`just`: https://github.com/casey/just

Examples
========

There will be examples throughout the documentation and available in
the ``examples/`` directory of this repository.

How To Cite
===========

TBD

Acknowledgements
================

I developed this code when working in the Pavan group,
https://www.gmpavanlab.polito.it/, whose members often provide very valuable
feedback, which I gratefully acknowledge.

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
