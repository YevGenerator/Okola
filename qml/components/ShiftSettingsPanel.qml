import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root

    property var backend
    property string cvdType: backend.cvd_type

    // Заголовок
    Text {
        Layout.fillWidth: true
        font.bold: true
        text: "Select Color Blindness Type:"
    }
    RowLayout {
        Layout.fillWidth: true

        Button {
            checkable: true
            checked: root.cvdType === "protanopia"
            text: "Protanopia"

            onClicked: backend.cvd_type = "protanopia"
        }
        Button {
            checkable: true
            checked: root.cvdType === "deuteranopia"
            text: "Deuteranopia"

            onClicked: backend.cvd_type = "deuteranopia"
        }
        Button {
            checkable: true
            checked: root.cvdType === "tritanopia"
            text: "Tritanopia"

            onClicked: backend.cvd_type = "tritanopia"
        }
    }
    Row {
        spacing: 10

        Slider {
            id: severitySlider

            Layout.fillWidth: true
            from: 0
            stepSize: 0.1
            to: 1.0
            value: backend.severity

            onValueChanged: backend.severity = value
        }
        SpinBox {
            id: severitySpin

            from: 0
            stepSize: 1
            to: 100
            value: Math.round(backend.severity * 100)

            onValueChanged: severitySlider.value = value / 100.0
        }
    }
}
