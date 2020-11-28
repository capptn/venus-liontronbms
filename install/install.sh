#!/bin/bash

read -p "Install Chargery BMS on Venus OS at your own risk? [Y to proceed]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
	echo "Download driver and library"

	wget https://github.com/capptn/venus-liontronbms/archive/Master.zip
	unzip Master.zip
	rm Master.zip

	wget https://github.com/victronenergy/velib_python/archive/master.zip
	unzip master.zip
	rm master.zip

	mkdir -p venus-liontron-Master/ext/velib_python
	cp -R velib_python-master/* venus-liontronbms-Master/ext/velib_python

	echo "Add Chargery entries to serial-starter"
	sed -i  's/ENV{VE_SERVICE}="rs485:default"/ENV{VE_SERVICE}="rs485:default:chargerybms"/g' /etc/udev/rules.d/serial-starter.rules
	sed -i  '/service.*imt.*dbus-imt-si-rs485tc/a service liontronbms     liontronbms' /etc/venus/serial-starter.conf

	echo "Install Chargery driver"
	mkdir -p /var/log/liontronbms
	mkdir -p /opt/victronenergy/liontronbms
	cp -R venus-liontronbms-Master/ext /opt/victronenergy/liontronbms
	cp -R venus-liontronbms-Master/driver/* /opt/victronenergy/liontronbms

	chmod +x /opt/victronenergy/liontronbms/start-liontronbms.sh
	chmod +x /opt/victronenergy/liontronbms/liontronbms.py
	chmod +x /opt/victronenergy/liontronbms/service/run
	chmod +x /opt/victronenergy/liontronbms/service/log/run

	ln -s /opt/victronenergy/liontronbms/service /service/liontronbms

	echo "Copy gui files"

	cp venus-liontronbms-Master/gui/qml/MbItemRowTOBO.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/MbTextDescriptionTOBO.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/PageBatteryChargeryBMS.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/PageBatteryChargeryBMSVoltages.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/PageMain.qml /opt/victronenergy/gui/qml

	read -p "Setup new gui overview? [Y to proceed]" -n 1 -r
	echo    # (optional) move to a new line
	if [[ $REPLY =~ ^[Yy]$ ]]
	then
		echo "Setup new overview"
		cp venus-liontronbms-Master/gui/qml/OverviewTiles.qml /opt/victronenergy/gui/qml
	fi

	echo "To finish, reboot the Venus OS device"
fi
