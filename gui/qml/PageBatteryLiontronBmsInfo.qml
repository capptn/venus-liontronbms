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
			description: qsTr("Zellen Balancer")
			values: [
				MbTextBlock { item { bind: service.path("/Info/Balance1"); } width: 40; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Balance2"); } width: 40; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Balance3"); } width: 40; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Balance4"); } width: 40; height: 25 }
			]
		}

		MbItemRow {
                        description: qsTr("Zellenanzahl")
                        values: [
                                MbTextBlock { item { bind: service.path("/Info/NumberOfCells"); } width: 70; height: 25 }
                        ]
                }

		MbItemRow {
                        description: qsTr("Ladezyklen")
                        values: [
                                MbTextBlock { item { bind: service.path("/Info/Cycles"); } width: 70; height: 25 }
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
			description: qsTr("Zellen (3/4)")
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
                        description: qsTr("Fehler Meldung")
                        values: [
                                MbTextBlock { item { bind: service.path("/Info/ProtectionState"); } width: 215; height: 25 }
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
