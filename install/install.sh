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

	mkdir -p venus-liontronbms-Master/ext/velib_python
	cp -R velib_python-master/* venus-liontronbms-Master/ext/velib_python

	echo "Add Chargery entries to serial-starter"
	echo 'ACTION=="add", ENV{ID_BUS}="usb", ENV{ID_MODEL}=="CP2102_USB_to_UART_Bridge_Controller",          ENV{VE_SERVICE}="liontronbms"' >> /etc/udev/rules.d/serial-starter.rules
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

	cp venus-liontronbms-Master/gui/qml/PageBatteryLiontronBms.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/PageBatteryChargeryLiontronBmsInfo.qml /opt/victronenergy/gui/qml
	cp venus-liontronbms-Master/gui/qml/PageMain.qml /opt/victronenergy/gui/qml

	echo "To finish, reboot the Venus OS device"
fi
