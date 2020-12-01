#!/usr/bin/env python

import argparse
import gobject
import platform
import argparse
import logging
import sys
import os
import time
import datetime
import serial
import math
import struct
import decimal

# setup timezone
os.environ['TZ'] = 'Europe/Berlin'

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
    # filename='log.txt')

# connect and register to dbus
driver = {
	'name'        : "LIONTRON BMS",
	'servicename' : "liontron",
	'instance'    : 1,
	'id'          : 0x01,
	'version'     : 1.0,
	'serial'      : "LIONGBMS",
	'connection'  : "com.victronenergy.battery.ttyLIONBMS01"
}


parser = argparse.ArgumentParser(description = 'LIONTRON BMS driver')
parser.add_argument('--version', action='version', version='%(prog)s v' + str(driver['version']) + ' (' + driver['serial'] + ')')
parser.add_argument('--debug', action="store_true", help='enable debug logging')
parser.add_argument('--test', action="store_true", help='test some stored examples network packets')
parser.add_argument('--victron', action="store_true", help='enable Victron DBUS support for VenusOS')
requiredArguments = parser.add_argument_group('required arguments')
requiredArguments.add_argument('-d', '--device', help='serial device for data (eg /dev/ttyUSB0)', required=True)
args = parser.parse_args()

serial_port = serial.Serial(args.device, 115200, timeout=1)
serial_port.flushInput()
logging.info(serial_port.name)


# victron stuff should be used
if args.victron:

	# Victron packages
	sys.path.insert(1, os.path.join(os.path.dirname(__file__), './ext/velib_python'))
	from vedbus import VeDbusService


	from dbus.mainloop.glib import DBusGMainLoop
	DBusGMainLoop(set_as_default=True)

	dbusservice = VeDbusService(driver['connection'])

	# Create the management objects, as specified in the ccgx dbus-api document
	dbusservice.add_path('/Mgmt/ProcessName', __file__)
	dbusservice.add_path('/Mgmt/ProcessVersion', 'Unknown and Python ' + platform.python_version())
	dbusservice.add_path('/Mgmt/Connection', driver['connection'])

	# Create the mandatory objects
	dbusservice.add_path('/DeviceInstance',  driver['instance'])
	dbusservice.add_path('/ProductId',       driver['id'])
	dbusservice.add_path('/ProductName',     driver['name'])
	dbusservice.add_path('/FirmwareVersion', driver['version'])
	dbusservice.add_path('/HardwareVersion', driver['version'])
	dbusservice.add_path('/Serial',          driver['serial'])
	dbusservice.add_path('/Connected',       1)

	# Create device list
	dbusservice.add_path('/Devices/0/DeviceInstance',  driver['instance'])
	dbusservice.add_path('/Devices/0/FirmwareVersion', driver['version'])
	dbusservice.add_path('/Devices/0/ProductId',       driver['id'])
	dbusservice.add_path('/Devices/0/ProductName',     driver['name'])
	dbusservice.add_path('/Devices/0/ServiceName',     driver['servicename'])
	dbusservice.add_path('/Devices/0/VregLink',        "(API)")

	# Create the chargery bms paths
	dbusservice.add_path('/Info/Soc',                      -1)
	dbusservice.add_path('/Info/CurrentMode',              -1)
	dbusservice.add_path('/Info/Current',                  -1)
	dbusservice.add_path('/Info/Temp/Sensor1',             -1)
	dbusservice.add_path('/Info/Temp/Sensor2',             -1)
	dbusservice.add_path('/Info/ChargeEndVoltage',         -1)
	dbusservice.add_path('/Info/UpdateTimestamp',          -1)
	dbusservice.add_path('/Info/BalanceHigh',              -1)
	dbusservice.add_path('/Info/BalanceLow',               -1)
	dbusservice.add_path('/Info/Mosfet',                   -1)
	dbusservice.add_path('/Info/NumberOfCells',            -1)
	dbusservice.add_path('/Info/Cycles',                   -1)
	dbusservice.add_path('/Info/ProtectionState',          -1)
	dbusservice.add_path('/Dc/0/Voltage',                  -1)
	dbusservice.add_path('/Dc/0/Current',                  -1)
	dbusservice.add_path('/Dc/0/Power',                    -1)
	dbusservice.add_path('/Dc/0/Temperature',              -1)
	dbusservice.add_path('/Soc',                           -1)
	dbusservice.add_path('/Voltages/Cell1',                -1)
	dbusservice.add_path('/Voltages/Cell2',                -1)
	dbusservice.add_path('/Voltages/Cell3',                -1)
	dbusservice.add_path('/Voltages/Cell4',                -1)
	dbusservice.add_path('/Voltages/Sum',                  -1)
	dbusservice.add_path('/Voltages/Diff',                 -1)
	dbusservice.add_path('/Voltages/Max',                  -1)
	dbusservice.add_path('/Voltages/Min',                  -1)
	dbusservice.add_path('/Voltages/BatteryCapacityWH',    -1)
	dbusservice.add_path('/Voltages/BatteryCapacityAH',    -1)
	dbusservice.add_path('/Voltages/BatteryNominalAH',     -1)
	dbusservice.add_path('/Voltages/UpdateTimestamp',      -1)



	# Create the real values paths
	dbusservice.add_path('/Raw/Info/Soc',                      -1)
	dbusservice.add_path('/Raw/Info/CurrentMode',              -1)
	dbusservice.add_path('/Raw/Info/Current',                  -1)
	dbusservice.add_path('/Raw/Info/Temp/Sensor1',             -1)
	dbusservice.add_path('/Raw/Info/Temp/Sensor2',             -1)
	dbusservice.add_path('/Raw/Info/ChargeEndVoltage',         -1)
	dbusservice.add_path('/Raw/Info/UpdateTimestamp',          -1)
	dbusservice.add_path('/Raw/Voltages/Cell1',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell2',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell3',                -1)
	dbusservice.add_path('/Raw/Voltages/Cell4',                -1)
	dbusservice.add_path('/Raw/Voltages/Sum',                  -1)
	dbusservice.add_path('/Raw/Voltages/Diff',                 -1)
	dbusservice.add_path('/Raw/Voltages/Max',                  -1)
	dbusservice.add_path('/Raw/Voltages/Min',                  -1)
	dbusservice.add_path('/Raw/Voltages/BatteryCapacityWH',    -1)
	dbusservice.add_path('/Raw/Voltages/BatteryCapacityAH',    -1)
	dbusservice.add_path('/Raw/Voltages/BatteryNominalAH',     -1)
	dbusservice.add_path('/Raw/Voltages/UpdateTimestamp',      -1)



PACKET_LENGTH_MINIMUM            = 10

BMS_STATUS = {
	'bms' : {
		'charged_end_voltage' : {
			'value' : -1.000,
			'text' : ""
		},
		'current_mode'        : {
			'value' : -1,
			'text'  : ""
		},
		'current' : {
			'value' : -1,
			'text' : ""
		},
		'temperature' : {
			'sensor_t1' : {
				'value' : -1.00,
				'text'  : ""
			},
			'sensor_t2' : {
				'value' : -1.00,
				'text'  : ""
			}
		},
		'soc' : {
			'value' : -1,
			'text'  : ""
		},
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		},
		'balance_high' : {
                        'value' : -1,
                        'text'  : ""
                },
		'balance_low' : {
                        'value' : -1,
                        'text'  : ""
                },
		'mosfet' : {
                        'value' : -1,
                        'text'  : ""
                },
		'number_of_cells' : {
                        'value' : -1,
                        'text'  : ""
                },
		'cycles' : {
                        'value' : -1,
                        'text'  : ""
                },
		'protection_state' : {
                        'value' : -1,
                        'text'  : ""
                }
	},
	'voltages' : {
		'cell1_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell2_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell3_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'cell4_voltage' : {
			'value' : -1,
			'text'  : ""
		},
		'agg_voltages' : {
			'sum' : {
				'value' : -1,
				'text'  : ""
			},
			'max' : {
				'value' : -1,
				'text'  : ""
			},
			'min' : {
				'value' : -1,
				'text'  : ""
			},
			'diff' : {
				'value' : -1,
				'text'  : ""
			}
		},
		'battery_capacity_wh' : {
			'value' : -1,
			'text'  : ""
		},
		'battery_capacity_ah' : {
			'value' : -1,
			'text'  : ""
		},
		'battery_nominal_ah' : {
                        'value' : -1,
                        'text'  : ""
                },
		'timestamp' : {
			'value' : -1,
			'text'  : ""
		}
	}
}

# example network packets form the chargery community protocol manual v1.25
BMS_TEST_PACKETS = {
	1 : bytearray.fromhex('2424570F0E240100E6008100845B27'),
	2 : bytearray.fromhex('2424570F0E240100E4008100845B25'),
	3 : bytearray.fromhex('2424570F0E240100E1008300845B24'),
	4 : bytearray.fromhex('2424562D0CFD0D040D040D020D030D040D060D010D080D020D050CFE0D060CFB0D0F0CFC76FED50263140E0095'),
    5 : bytearray.fromhex('2424582801E4000100030003000300020003000000000001000100010000000500020003000300CC'),
	6 : bytearray.fromhex('2424570F0E240100E4008300845B27'),
	7 : bytearray.fromhex('24245814012a000900040007000b000b00070010')
}


# define special unicode characters here
SPECIAL_DISPLAY_SYMBOLS = {
	'degree' : u'\u00b0',
	'ohm'    : u'\u03A9'
}


def reset_status_values():

	BMS_STATUS['bms']['charged_end_voltage']['value'] = -1
	BMS_STATUS['bms']['charged_end_voltage']['text']  = ""
	BMS_STATUS['bms']['current_mode']['value'] = -1
	BMS_STATUS['bms']['current_mode']['text']  = ""
	BMS_STATUS['bms']['current']['value'] = -1
	BMS_STATUS['bms']['current']['text']  = ""
	BMS_STATUS['bms']['temperature']['sensor_t1']['value'] = -1
	BMS_STATUS['bms']['temperature']['sensor_t1']['text']  = ""
	BMS_STATUS['bms']['temperature']['sensor_t2']['value'] = -1
	BMS_STATUS['bms']['temperature']['sensor_t2']['text']  = ""
	BMS_STATUS['bms']['soc']['value'] = -1
	BMS_STATUS['bms']['soc']['text']  = ""
	BMS_STATUS['bms']['timestamp']['value'] = -1
	BMS_STATUS['bms']['timestamp']['text']  = ""
	BMS_STATUS['bms']['balance_high']['value'] = -1
        BMS_STATUS['bms']['balance_high']['text']  = ""
        BMS_STATUS['bms']['balance_low']['value'] = -1
        BMS_STATUS['bms']['balance_low']['text']  = ""
        BMS_STATUS['bms']['mosfet']['value'] = -1
        BMS_STATUS['bms']['mosfet']['text']  = ""
        BMS_STATUS['bms']['number_of_cells']['value'] = -1
        BMS_STATUS['bms']['number_of_cells']['text']  = ""


def reset_voltages_values():
	BMS_STATUS['voltages']['cell1_voltage']['value'] = -1
	BMS_STATUS['voltages']['cell1_voltage']['text']  = ""
	BMS_STATUS['voltages']['cell2_voltage']['value'] = -1
	BMS_STATUS['voltages']['cell2_voltage']['text']  = ""
	BMS_STATUS['voltages']['cell3_voltage']['value'] = -1
	BMS_STATUS['voltages']['cell3_voltage']['text']  = ""
	BMS_STATUS['voltages']['cell4_voltage']['value'] = -1
	BMS_STATUS['voltages']['cell4_voltage']['text']  = ""
	BMS_STATUS['voltages']['agg_voltages']['sum']['value'] = -1
	BMS_STATUS['voltages']['agg_voltages']['sum']['text']  = ""
	BMS_STATUS['voltages']['agg_voltages']['max']['value'] = -1
	BMS_STATUS['voltages']['agg_voltages']['max']['text']  = ""
	BMS_STATUS['voltages']['agg_voltages']['min']['value'] = -1
	BMS_STATUS['voltages']['agg_voltages']['min']['text']  = ""
	BMS_STATUS['voltages']['agg_voltages']['diff']['value'] = -1
	BMS_STATUS['voltages']['agg_voltages']['diff']['text']  = ""
	BMS_STATUS['voltages']['battery_capacity_wh']['value'] = -1
	BMS_STATUS['voltages']['battery_capacity_wh']['text']  = ""
	BMS_STATUS['voltages']['battery_capacity_ah']['value'] = -1
	BMS_STATUS['voltages']['battery_capacity_ah']['text']  = ""
	BMS_STATUS['voltages']['timestamp']['value'] = -1
	BMS_STATUS['voltages']['timestamp']['text']  = ""

def get_voltage_value(val1):
	return float(val1.strip())

def get_remainWh(v, ah):
        return int(v * ah)


def parse_packet(packet):
	BMS_STATUS['bms']['temperature']['sensor_t1']['value'] = 21.20
	BMS_STATUS['bms']['temperature']['sensor_t1']['text'] = "21.20" + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"
	print(packet)
	lines = packet.splitlines()
	if len(lines) >= 18:
		cell1_voltage = lines[13].split(": ")
		print("NEW DATA")
		if len(cell1_voltage) >= 2:
			if cell1_voltage[0] == "Cell 1":
				print(cell1_voltage[1]);
				reset_voltages_values()
				BMS_STATUS['voltages']['cell1_voltage']['value'] = get_voltage_value(cell1_voltage[1])
				BMS_STATUS['voltages']['cell1_voltage']['text'] = "{:.3f}".format(float(cell1_voltage[1])) + "V"
				if args.victron:
					dbusservice["/Voltages/Cell1"] = BMS_STATUS['voltages']['cell1_voltage']['text']
					dbusservice["/Raw/Voltages/Cell1"] = BMS_STATUS['voltages']['cell1_voltage']['value']
				current_date = datetime.datetime.now()
				BMS_STATUS['voltages']['timestamp']['value'] = time.time()
				BMS_STATUS['voltages']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
				if args.victron:
					dbusservice["/Voltages/UpdateTimestamp"] = BMS_STATUS['voltages']['timestamp']['text']
					dbusservice["/Raw/Voltages/UpdateTimestamp"] = BMS_STATUS['voltages']['timestamp']['value']
			cell2_voltage = lines[14].split(": ")
			if cell2_voltage[0] == "Cell 2":
				BMS_STATUS['voltages']['cell2_voltage']['value'] = get_voltage_value(cell2_voltage[1])
                                BMS_STATUS['voltages']['cell2_voltage']['text'] = "{:.3f}".format(float(cell2_voltage[1])) + "V"
                                if args.victron:
                                        dbusservice["/Voltages/Cell2"] = BMS_STATUS['voltages']['cell2_voltage']['text']
                                        dbusservice["/Raw/Voltages/Cell2"] = BMS_STATUS['voltages']['cell2_voltage']['value']
			cell3_voltage = lines[15].split(": ")
                        if cell3_voltage[0] == "Cell 3":
                                BMS_STATUS['voltages']['cell3_voltage']['value'] = get_voltage_value(cell3_voltage[1])
                                BMS_STATUS['voltages']['cell3_voltage']['text'] = "{:.3f}".format(float(cell3_voltage[1])) + "V"
                                if args.victron:
                                        dbusservice["/Voltages/Cell3"] = BMS_STATUS['voltages']['cell3_voltage']['text']
                                        dbusservice["/Raw/Voltages/Cell3"] = BMS_STATUS['voltages']['cell3_voltage']['value']
			cell4_voltage = lines[16].split(": ")
                        if cell4_voltage[0] == "Cell 4":
                                BMS_STATUS['voltages']['cell4_voltage']['value'] = get_voltage_value(cell4_voltage[1])
                                BMS_STATUS['voltages']['cell4_voltage']['text'] = "{:.3f}".format(float(cell4_voltage[1])) + "V"
                                if args.victron:
                                        dbusservice["/Voltages/Cell4"] = BMS_STATUS['voltages']['cell4_voltage']['text']
                                        dbusservice["/Raw/Voltages/Cell4"] = BMS_STATUS['voltages']['cell4_voltage']['value']
			voltageSum = lines[0].split(": ")
			if len(voltageSum) >= 2 and voltageSum[0] == "Total voltage":
				BMS_STATUS['voltages']['agg_voltages']['sum']['value']  = round(float(voltageSum[1]), 2);
				BMS_STATUS['voltages']['agg_voltages']['sum']['text']   = "{:.2f}".format(BMS_STATUS['voltages']['agg_voltages']['sum']['value']) + "V"
				if args.victron:
					dbusservice["/Voltages/Sum"]      = BMS_STATUS['voltages']['agg_voltages']['sum']['text']
					dbusservice["/Raw/Voltages/Sum"]  = BMS_STATUS['voltages']['agg_voltages']['sum']['value']
					dbusservice["/Dc/0/Voltage"]  = BMS_STATUS['voltages']['agg_voltages']['sum']['value']
			soc = lines[5].split(": ")
			if len(soc) >= 2 and soc[0] == "CapacityRemainPercent":
				# soc value
				print("receive SOC from ESP")
				reset_status_values()
				BMS_STATUS['bms']['soc']['value'] = float(soc[1])
				BMS_STATUS['bms']['soc']['text'] = soc[1] + "%"
				if args.victron:
					dbusservice["/Info/Soc"] = BMS_STATUS['bms']['soc']['text']
					dbusservice["/Raw/Info/Soc"] = BMS_STATUS['bms']['soc']['value']
					dbusservice["/Soc"] = BMS_STATUS['bms']['soc']['value']
				# update timestamp
				current_date = datetime.datetime.now()
				BMS_STATUS['bms']['timestamp']['value'] = time.time()
				BMS_STATUS['bms']['timestamp']['text']  = current_date.strftime('%a %d.%m.%Y %H:%M:%S')
				if args.victron:
					dbusservice["/Info/UpdateTimestamp"] = BMS_STATUS['bms']['timestamp']['text']
					dbusservice["/Raw/Info/UpdateTimestamp"] = BMS_STATUS['bms']['timestamp']['value']
                        temp1 = lines[6].split(": ")
                        if len(temp1) >= 2 and  temp1[0] == "Temp1":
				BMS_STATUS['bms']['temperature']['sensor_t1']['value'] = float(temp1[1])
				BMS_STATUS['bms']['temperature']['sensor_t1']['text'] = "{:.2f}".format(float(temp1[1])) + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"
				if args.victron:
					dbusservice["/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['text']
					dbusservice["/Raw/Info/Temp/Sensor1"] = BMS_STATUS['bms']['temperature']['sensor_t1']['value']
					dbusservice["/Dc/0/Temperature"] = BMS_STATUS['bms']['temperature']['sensor_t1']['value']
			temp2 = lines[7].split(": ")
                        if len(temp2) >= 2 and temp2[0] == "Temp2":
                                BMS_STATUS['bms']['temperature']['sensor_t2']['value'] = float(temp2[1])
                                BMS_STATUS['bms']['temperature']['sensor_t2']['text'] = temp2[1] + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"
                                if args.victron:
                                        dbusservice["/Info/Temp/Sensor2"] = "{:.2f}".format(float(temp2[1])) + SPECIAL_DISPLAY_SYMBOLS['degree'] + "C"
                                        dbusservice["/Raw/Info/Temp/Sensor2"] = BMS_STATUS['bms']['temperature']['sensor_t2']['value']
                        remainAh = lines[2].split(": ")
                        if len(remainAh) >= 2 and remainAh[0] == "CapacityRemainAh":
                                # Remainding AH value
                               	BMS_STATUS['voltages']['battery_capacity_ah']['value'] = float(remainAh[1])
				BMS_STATUS['voltages']['battery_capacity_ah']['text'] = "{:.0f}".format(float(remainAh[1])) + "Ah"
				if args.victron:
					dbusservice["/Voltages/BatteryCapacityAH"] = BMS_STATUS['voltages']['battery_capacity_ah']['text']
					dbusservice["/Raw/Voltages/BatteryCapacityAH"] = BMS_STATUS['voltages']['battery_capacity_ah']['value']
			nominalAh = lines[3].split(": ")
			if len(nominalAh) >= 2 and nominalAh[0] == "CapacityNominalAh":
                                # Remainding AH value
                                BMS_STATUS['voltages']['battery_nominal_ah']['value'] = float(nominalAh[1])
                                BMS_STATUS['voltages']['battery_nominal_ah']['text'] = "{:.0f}".format(float(nominalAh[1])) + "Ah"
                                if args.victron:
                                        dbusservice["/Voltages/BatteryNominalAH"] = BMS_STATUS['voltages']['battery_nominal_ah']['text']
                                        dbusservice["/Raw/Voltages/BatteryNominalAH"] = BMS_STATUS['voltages']['battery_nominal_ah']['value']
			if len(remainAh) >= 2 and len(voltageSum) >= 2 and remainAh[0] == "CapacityRemainAh" and voltageSum[0] == "Total voltage":
				remainWh = get_remainWh(float(voltageSum[1]), float(remainAh[1]))
				BMS_STATUS['voltages']['battery_capacity_wh']['value'] = remainWh
				BMS_STATUS['voltages']['battery_capacity_wh']['text'] = "{:.0f}".format(BMS_STATUS['voltages']['battery_capacity_wh']['value']) + "Wh"
				if args.victron:
					dbusservice["/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['text']
					dbusservice["/Raw/Voltages/BatteryCapacityWH"] = BMS_STATUS['voltages']['battery_capacity_wh']['value']
			amps = lines[1].split(": ")
                        if len(amps) >= 2 and amps[0] == "Amps":
				BMS_STATUS['bms']['current']['value'] = float(amps[1])
				BMS_STATUS['bms']['current']['text'] = str(BMS_STATUS['bms']['current']['value']) + "A"
				if args.victron:
					dbusservice["/Info/Current"]     = BMS_STATUS['bms']['current']['text']
					dbusservice["/Raw/Info/Current"]     = BMS_STATUS['bms']['current']['value']
					dbusservice["/Dc/0/Current"]     = BMS_STATUS['bms']['current']['value']
				watt = BMS_STATUS['bms']['current']['value'] * BMS_STATUS['voltages']['agg_voltages']['sum']['value']
				if args.victron:
					dbusservice["/Dc/0/Power"]     = watt
			balanceLow = lines[8].split(": ")
                        if len(balanceLow) >= 2 and balanceLow[0] == "Balance Code Low":
                                BMS_STATUS['bms']['balance_low']['text'] = balanceLow[1]
                                if args.victron:
                                        dbusservice["/Info/BalanceLow"]     = BMS_STATUS['bms']['balance_low']['text']
			balanceHigh = lines[9].split(": ")
                        if len(balanceHigh) >= 2 and balanceHigh[0] == "Balance Code High":
                                BMS_STATUS['bms']['balance_high']['text'] = balanceHigh[1]
                                if args.victron:
                                        dbusservice["/Info/BalanceHigh"]     = BMS_STATUS['bms']['balance_high']['text']
			mosfet = lines[10].split(": ")
                        if len(mosfet) >= 2 and mosfet[0] == "Mosfet Status":
                                BMS_STATUS['bms']['mosfet']['text'] = mosfet[1]
                                if args.victron:
                                        dbusservice["/Info/Mosfet"]     = BMS_STATUS['bms']['mosfet']['text']
			numberOfCells = lines[12].split(": ")
                        if len(numberOfCells) >= 2 and numberOfCells[0] == "Number of cells":
                                BMS_STATUS['bms']['number_of_cells']['text'] = numberOfCells[1]
                                if args.victron:
                                        dbusservice["/Info/NumberOfCells"]     = BMS_STATUS['bms']['number_of_cells']['text']
			cycles = lines[4].split(": ")
                        if len(cycles) >= 2 and cycles[0] == "Cycles":
                                BMS_STATUS['bms']['cycles']['text'] = int(float(cycles[1]))
                                if args.victron:
                                        dbusservice["/Info/Cycles"]     = BMS_STATUS['bms']['cycles']['text']
			protectioncode = lines[11].split(": ")
                        if len(protectioncode) >= 2 and protectioncode[0] == "Protection Code":
				protectionbyte = int(protectioncode[1], 16)
				print(protectionbyte);
				protectiontext = "---"
				if protectionbyte == 0:
					protectiontext = "Kein Fehler"
				if protectionbyte != 0:
					protectiontext = "Fehler vorhanden!"
				print(protectiontext);
                                BMS_STATUS['bms']['protection_state']['text'] = protectiontext
                                if args.victron:
                                        dbusservice["/Info/ProtectionState"]     = BMS_STATUS['bms']['protection_state']['text']


def handle_serial_data(test_packet = ''):
	try:
		serial_packet = ""
		if (serial_port.in_waiting > 0):
			logging.debug("Data Waiting [" + str(serial_port.in_waiting) + " bytes]")
		if (serial_port.in_waiting >= (PACKET_LENGTH_MINIMUM * 2)):
			data_buffer_array = serial_port.read(serial_port.in_waiting)
			logging.debug("Data Received [" + str(len(data_buffer_array)) + " bytes]")
			for data_buffer in data_buffer_array:
				serial_packet += data_buffer

			if (len(serial_packet) > 0):
				parse_packet(serial_packet)

			data_buffer_array = ""
			serial_packet = ""

		if args.victron:
			gobject.timeout_add(1000, handle_serial_data)

	except KeyboardInterrupt:
		if not args.victron:
			raise

if args.victron:
	gobject.timeout_add(1000, handle_serial_data)
	mainloop = gobject.MainLoop()
	mainloop.run()
else:
	while True:
		handle_serial_data()
		time.sleep(1)
