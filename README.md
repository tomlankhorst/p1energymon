P1 Energy Monitor
=================
This is the ** Meeuwenstraat Energy Monitor **. A small Python application that reads serial data sent through the P1 port of a DSMR (Dutch Smart Meter Requirements) smart meter. It is designed to be effective and reduce writes to SD cards or other storage to increase the lifetime of a Raspberry Pi. 
Installation
------------
- Set the parameters in energymon.py
- Copy the init.d file to /etc/init.d
- Edit the file, ensure paths are correct
- chmod +x the file to enable execution
- `sudo update-rc.d energymon defaults`
