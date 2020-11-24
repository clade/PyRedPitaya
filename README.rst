Overview
========

This package provides a library to access the `Red Pitaya <http://redpitaya.com/>`_ registers. This library consist of a C library (libmonitor.c) and a ctypes interface on the Python side. 

An object oriented interface to the different application (scope, generator, PID, AMS, ...) is provided. This interface is implemented using Python properties (see usage below) and can quickly be extended to your own application. 

An rpyc server is used in order to communicate with your computer. The interface is the same on the computer as the one on the board.

Installation
============

The process to install PyRedPitaya on the board requires the installation of Python first. See `this link <https://github.com/clade/RedPitaya/tree/master/python>`_.


To install PyRedPitaya on the computer download the package and run the command:: 

  python setup.py install

or use easy_install::

  easy_install PyRedPitaya


Usage
=====

You need to have Python installed on you Red Pitaya. 

Interactive Python
------------------

Logging onto the redpitaya using ssh, one can start the ipython shell and run :

.. code ::

    from PyRedPitaya.board import RedPitaya

    redpitaya = RedPitaya()

    print redpitaya.ams.temp # Read property
    redpitaya.hk.led = 0b10101010 # Write property


Remote access
-------------

You need to install the PyRedPitaya package on your PC as well as Rpyc: 

.. code::

    rpyc_server

On the computer (replace REDPITAYA_IP by the string containing the IP address) : 

.. code::

    from rpyc import connect
    from PyRedPitaya.pc import RedPitaya

    conn = connect(REDPITAYA_IP, port=18861)
    redpitaya = RedPitaya(conn)

    print(redpitaya.read(0x40000000)) # Direct access

    print(redpitaya.ams.temp) # Read property

    from time import sleep
    import matplotlib.pyplot as plt

    redpitaya.scope.setup(data_decimation=8, trigger_source=1)
    sleep(100E-3)
    plt.plot(redpitaya.scope.times, redpitaya.scope.data_ch1)
    plt.show()

