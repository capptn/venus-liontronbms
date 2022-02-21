import QtQuick 1.1
import com.victron.velib 1.0

MbPage {
	id: root

	property variant service
	property string bindPrefix

	property VBusItem hasSettings: VBusItem { bind: service.path("/Settings/HasSettings") }
	property VBusItem productId: VBusItem { bind: service.path("/ProductId") }
	property VBusItem socItem: VBusItem { bind: service.path("/Info/Soc") }
	property VBusItem voltItem: VBusItem { bind: service.path("/Voltages/Sum") }
	property VBusItem currentItem: VBusItem { bind: service.path("/Info/Current") }

	title: service.description
	summary: [socItem.text, voltItem.text, currentItem.text ]

	model: VisualItemModel {

		MbItemRow {
			id: battvol
			description: qsTr("Batterie Spannung")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Sum"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Ladezustand")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/BatteryCapacityWH"); } height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/BatteryCapacityAH"); }  width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Soc"); } width: 70; height: 25 }
			]
		}
		
		MbItemRow {
			description: qsTr("")
			values: [
				MbTextBlock { item { bind: service.path("/Info/Eta"); } width:70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Temperatur-Sensoren (1/2)")
			values: [
				MbTextBlock { item { bind: service.path("/Info/Temp/Sensor1"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Temp/Sensor2"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Letzte Verbindung")
			values: [
				MbTextBlock { item { bind: service.path("/Info/UpdateTimestamp"); } width: 215; height: 25 }
			]
		}


		MbSubMenu {
			description: qsTr("Informationen")
			subpage: Component {
				PageBatteryLiontronBmsInfo {
					bindPrefix: service.path("")
				}
			}
		}

		MbSubMenu {
			description: qsTr("Device")
			subpage: Component {
				PageDeviceInfo {
					title: qsTr("Device")
					bindPrefix: service.path("")
				}
			}
		}

	}
}
