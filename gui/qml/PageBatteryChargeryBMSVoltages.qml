import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils

MbPage {
	id: root

	property string bindPrefix
	property BatteryDetails details: BatteryDetails { bindPrefix: root.bindPrefix }
	title: service.description + " | Cell Voltages"

	model: VisualItemModel {

		MbItemRow {
			description: qsTr("Status (BalL/BalH/Mos)")
			values: [
				MbTextBlock { item { bind: service.path("/Info/BalanceLow"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/BalanceHigh"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Mosfet"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
                        description: qsTr("Zellenanzahl")
                        values: [
                                MbTextBlock { item { bind: service.path("/Info/NumberOfCells"); } width: 70; height: 25 }
                        ]
                }

		MbItemRow {
			description: qsTr("Zellen (1/2)")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Cell1"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell2"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Zellen (4/5")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Cell3"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell4"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Normal Kapazität")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/BatteryNominalAH"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Data Timestamp")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/UpdateTimestamp"); } width: 215; height: 25 }
			]
		}

	}
}
