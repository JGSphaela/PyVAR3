# PyVAR3

A small software for 3(or more) sweeping parameters measurements. WIP  

Clever people at Keysight decided that their software only support 2 sweeps(VAR1, VAR2).  
This is an effort to try to change that.

This program was designed to run on all platforms, but the keysight IO suite only _REALLY_ support Windows. NI MAX can be used, but it's untested(it doesn't support Keysight/Aligent instruments that I use).

## Requirements

PyVISA, PyQt6, Numpy, Matplotlib, Pandas

## Progress

Connection, data retrieve and 3-way sweep completed.

Need to solve the problem that current measuring strat is __too slow__.

Will work on GUI after program is functionally completed.
