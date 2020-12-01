 # License
 - MIT License
 - Use this project at your own risk
# Thanks a lot

Inspired by @Tobi177 : [https://github.com/Tobi177/venus-chargerybms].
He created a driver for a chargery BMS and made it available and thus provided a very good example of how to create such a driver
Many Thanks!

# Description

This driver connects Venus OS to a Liontron BMS (xiaoxiang bms). 

![preview1](https://github.com/capptn/venus-liontronbms/blob/Master/img/example1.png)
![preview2](https://github.com/capptn/venus-liontronbms/blob/Master/img/example2.png)
![preview3](https://github.com/capptn/venus-liontronbms/blob/Master/img/example3.png)

The Liontronbms Driver can act as the Main Batterymonitor of your Victron Venus OS System.


![](https://github.com/capptn/venus-liontronbms/blob/Master/img/example4.png | width=100)
![](https://github.com/capptn/venus-liontronbms/blob/Master/img/example5.png | width=100)
<img src="https://your-image-url.type" width="100" height="100">

# Requirements

- Venus OS, GX Device or Raspberry Pi
- ESP32 as bridge beetwen USB->Serial->Bluetooth with this software: [coming soon]

# Installation on Venus OS
- Download the install.sh under /install/install.sh
- Access Venus os via SSH with root: [https://www.victronenergy.com/live/ccgx:root_access]
- connect the ESP32
- reboot

# Notes
- The driver must be reinstalled after a firmware upgrade
