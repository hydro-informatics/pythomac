.. extraction documentation

Extraction Tools
================

Find more background information on `hydro-informatics.com <https://hydro-informatics.com/numerics/telemac/telemac2d-steady.html#verify-steady-tm2d>`_.

Usage Example
-------------

.. code:: python

    from pythomac import extract_fluxes
    
    
    simulation_dir = "/home/telemac-user/simulations/rhine/"
    cas_name = "steady2d.cas"
    extract_fluxes(simulation_dir, cas_name, plotting=False)


Script and Function docs
------------------------


Extract Fluxes
~~~~~~~~~~~~~~


.. automodule:: pythomac.extract_fluxes
    :members:
    :show-inheritance:


