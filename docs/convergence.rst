.. extraction documentation

Convergence Analysis
====================

Find more background information on `hydro-informatics.com <https://hydro-informatics.com/convergence>`_.

Usage Example
-------------

.. important:: Requires a Telemac simulation with -s flag

    The examples require that a Telemac2d simulation ran with ``telemac2d.py steady2d.cas -s`` and that the .cas file contained the keyword
    ``PRINTING CUMULATED FLOWRATES : YES``.



Minimal
~~~~~~~

The quickest way to try ``pythomac`` is to use the example data shipped in the pythomac repository. You do not need to clone the whole repository or run a Telemac simulation; the ``example-simulation/`` folder already contains a finished run (including the ``.sortie`` output file that ``pythomac`` reads).

#. Install ``pythomac`` into your Python environment (if not yet done):

   .. code:: bash

       pip install pythomac

#. Download two items from the `pythomac repository <https://github.com/hydro-informatics/pythomac>`_ and keep them side by side:

   * the script ``example_flux_convergence.py``
   * the folder ``example-simulation/`` (with ``steady2d.cas`` and its      ``steady2d.cas_*.sortie`` output file)

   So your local layout looks like this:

   .. code:: text

       my-folder/
       ├── example_flux_convergence.py
       └── example-simulation/
           ├── steady2d.cas
           └── steady2d.cas_2024-12-06-12h52min49s.sortie

#. Run the script from ``my-folder/``:

   .. code:: bash

       python example_flux_convergence.py

   It resolves the example data relative to its own location, so no paths need   editing. The run writes ``extracted_fluxes.csv``, ``flux-convergence.png``,    ``convergence-rate.png``, and ``convergence-rate.csv`` into ``example-simulation/``.

To point the analysis at your own simulation instead, set ``simulation_dir`` to 
that simulation's folder and ``telemac_cas`` to its steering file name, for instance:

.. code:: python

    from pythomac import extract_fluxes

    simulation_dir = "/home/telemac-user/simulations/rhine/"
    cas_name = "steady2d.cas"
    extract_fluxes(simulation_dir, cas_name, plotting=False)

Full application
~~~~~~~~~~~~~~~~

.. literalinclude:: ../example_flux_convergence.py
   :language: python
   :linenos:


Script and Function docs
------------------------


Flux Analyst
~~~~~~~~~~~~~~

.. automodule:: pythomac.flux_analyst
    :members:
    :show-inheritance:

Plotting
~~~~~~~~

.. automodule:: pythomac.utils.plots
    :members:
    :show-inheritance:
