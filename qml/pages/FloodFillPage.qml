import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

RowLayout {
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.right: parent.right

    FloodImageView {
        id: imageView

        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.7
        backend: flood_image
    }
    ColumnLayout {
        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.3

        Magnifier {
            id: magnifier

            pos: imageView.backend.cursor_pos
            sourceItem: imageView
        }
        ColorSquare {
            id: colorSquare

            color: imageView.backend.presenter.color
        }
        ColorText {
            colorPresenter: imageView.backend.presenter
        }
        Text {
            Layout.fillWidth: true
            font.bold: true
            text: "Set tolerance:"
        }
        Row {
            spacing: 10

            Slider {
                id: toleranceSlider

                Layout.fillWidth: true
                from: 0
                stepSize: 1
                to: 100
                value: imageView.backend.tolerance

                onValueChanged: imageView.backend.tolerance = value
            }
            SpinBox {
                id: toleranceSpin

                from: 0
                stepSize: 1
                to: 100
                value: toleranceSlider.value
                onValueChanged: severitySlider.value = value
            }
        }
        Button{
            Layout.fillWidth: true
            text: "Reset"
            onClicked: imageView.backend.reset()
        }
    }
}
