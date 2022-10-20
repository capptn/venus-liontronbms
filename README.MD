 # License
 - MIT License
 - Use this project at your own risk
# Thanks a lot

Inspired by @Tobi177 : [https://github.com/Tobi177/venus-chargerybms].
He created a driver for a chargery BMS and made it available and thus provided a very good example of how to create such a driver
Many Thanks!

# Description

This driver connects Venus OS to a Liontron BMS (xiaoxiang bms). 

<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example1.png" height="200">
<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example3.png" height="200">
<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example2.png" height="200">


The Liontronbms driver can act as the main batterymonitor of your victron system.

<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example4.png" height="200">
<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example5.png" height="200">

!! Attention !!, you have to open and change the battery. All changes you make are at your own risk

<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/example6.png" height="500">

!! Attention, the wiring shown in the picture is only for the test setup.
If the system is an island system on battery operation, attention must be paid to the isolation of the FTDI adapter. Otherwise equalizing currents will flow which are not measured by the bms.

If the GX device is supplied by the same battery that is to be monitored, it is sufficient to only connect the rx and tx lines. An isolated FTDI can also be used.

<img src="https://github.com/capptn/venus-liontronbms/blob/Master/img/conn_example.png" height="500">

# Requirements

- Venus OS, GX Device or Raspberry Pi
- FTDI-USB Adapter (with CP2102 Chip)

# Installation on Venus OS
- Access Venus os via SSH with root: [https://www.victronenergy.com/live/ccgx:root_access]
- Download the install.sh under /install/install.sh
- run it with `sh install.sh`
- reboot
- connect the Battery and FTDI

# Using the driver for other purposes

To get a JSON-formatted report, use the `--json` option.

The `--delay <number>` will set a repeat interval of `number` seconds. A negative value for `number` will cause liontronbms.py to exit normally after creating a single report.

# Usage via Bluetooth serial

This might be simpler than using serial wiring. To do so:
- install Python ble-serial: https://github.com/Jakeler/ble-serial
  - usally this is just `pip install ble.serial` 
- run ble-serial like so:

````
mah@oe-sox:~/src/venus-liontronbms/driver$ ble-serial -i hci0 -d A4:C1:38:9A:A7:24
03:01:27.961 | INFO | linux_pty.py: Port endpoint created on /tmp/ttyBLE -> /dev/pts/5
03:01:27.961 | INFO | ble_interface.py: Receiver set up
/home/mah/.local/lib/python3.10/site-packages/ble_serial/bluetooth/ble_interface.py:28: FutureWarning: This method will be removed future version, pass the callback to the BleakClient constructor instead.
  self.dev.set_disconnected_callback(self.handle_disconnect)
03:01:28.363 | INFO | ble_interface.py: Trying to connect with A4:C1:38:9A:A7:24: 032240133
03:01:29.427 | INFO | ble_interface.py: Device A4:C1:38:9A:A7:24 connected
03:01:29.427 | INFO | ble_interface.py: Found write characteristic 0000ff02-0000-1000-8000-00805f9b34fb (H. 20)
03:01:29.427 | INFO | ble_interface.py: Found notify characteristic 0000ff01-0000-1000-8000-00805f9b34fb (H. 16)
03:01:29.765 | INFO | main.py: Running main loop!
````

This will create a pseudo-serial device connected to the battery at /dev/ttyBLE which can be used by liontronbms.py like so:


````
mah@oe-sox:~/src/venus-liontronbms/driver$ python liontronbms.py -d /tmp/ttyBLE  --json --interval -1
2022-10-20 03:49:16 INFO     /tmp/ttyBLE
2022-10-20 03:49:16 INFO     ask for basic Data
2022-10-20 03:49:17 INFO     parse packet 3
2022-10-20 03:49:17 INFO      leer um 15.614678899082568
2022-10-20 03:49:17 INFO     ask for Cell Data
2022-10-20 03:49:17 INFO     parse packet 4
2022-10-20 03:49:17 INFO     3.176
2022-10-20 03:49:17 INFO     ask for bms info
2022-10-20 03:49:18 INFO     parse packet 5
2022-10-20 03:49:18 INFO     serial number 032240133
{
    "bms": {
        "charged_end_voltage": {
            "value": -1,
            "text": ""
        },
        "current_mode": {
            "value": -1,
            "text": ""
        },
        "current": {
            "value": -1.09,
            "text": "-1.09A"
        },
        "temperature": {
            "sensor_t1": {
                "value": 20.8,
                "text": "20.80\u00b0C"
            },
            "sensor_t2": {
                "value": -405.9,
                "text": "-405.90\u00b0C"
            }
        },
        "soc": {
            "value": 37.0,
            "text": "37%"
        },
        "eta": {
            "value": 15.614678899082568,
            "text": " leer um Thu 20.10.2022 19:26:10"
        },
        "timestamp": {
            "value": 1666230557.1611423,
            "text": "Thu 20.10.2022 03:49:17"
        },
        "balance_1": {
            "value": -1,
            "text": "0"
        },
        "balance_2": {
            "value": -1,
            "text": "0"
        },
        "balance_3": {
            "value": -1,
            "text": "0"
        },
        "balance_4": {
            "value": -1,
            "text": "0"
        },
        "mosfet": {
            "value": -1,
            "text": ""
        },
        "number_of_cells": {
            "value": 4,
            "text": "4"
        },
        "cycles": {
            "value": -1,
            "text": 1
        },
        "protection_state": {
            "value": -1,
            "text": "Kein Fehler"
        }
    },
    "voltages": {
        "cell1_voltage": {
            "value": 3.176,
            "text": "3.176V"
        },
        "cell2_voltage": {
            "value": 3.177,
            "text": "3.177V"
        },
        "cell3_voltage": {
            "value": 3.176,
            "text": "3.176V"
        },
        "cell4_voltage": {
            "value": 3.177,
            "text": "3.177V"
        },
        "agg_voltages": {
            "sum": {
                "value": 12.7,
                "text": "12.70V"
            },
            "max": {
                "value": -1,
                "text": ""
            },
            "min": {
                "value": -1,
                "text": ""
            },
            "diff": {
                "value": -1,
                "text": ""
            }
        },
        "battery_capacity_wh": {
            "value": 216.154,
            "text": "216Wh"
        },
        "battery_capacity_ah": {
            "value": 17.02,
            "text": "17Ah"
        },
        "battery_nominal_ah": {
            "value": 46.13,
            "text": "46Ah"
        },
        "timestamp": {
            "value": 1666230557.6626542,
            "text": "Thu 20.10.2022 03:49:17"
        }
    }
}
```` 

# Notes
- The driver must be reinstalled after a firmware upgrade
