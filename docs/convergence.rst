.. extraction documentation

Convergence Analysis
====================

Find more background information on `hydro-informatics.com <https://hydro-informatics.com/numerics/telemac/convergence.html>`_.

Usage Example
-------------

Minimal
~~~~~~~
.. code:: python

    from pythomac import extract_fluxes
    
    
    simulation_dir = "/home/telemac-user/simulations/rhine/"
    cas_name = "steady2d.cas"
    extract_fluxes(simulation_dir, cas_name, plotting=False)

Full application
~~~~~~~~~~~~~~~~

.. literalinclude:: .example_flux_convergence.py
   :language: python
   :linenos:


Script and Function docs
------------------------


Flux Analyst
~~~~~~~~~~~~~~

.. automodule:: pythomac.extract_fluxes
    :members:
    :show-inheritance:


.. automodule:: pythomac.calculate_convergence
    :members:
    :show-inheritance:

.. automodule:: pythomac.get_convergence_time
    :members:
    :show-inheritance:

Plotting
~~~~~~~~

.. automodule:: pythomac.utils.plots
    :members:
    :show-inheritance:
