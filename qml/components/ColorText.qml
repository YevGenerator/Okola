import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ColumnLayout {
    id: root
    property var colorPresenter

    Label {
        font.pixelSize: 14
        text: "RGB: " + root.colorPresenter.rgb.join(", ")
    }
    Label {
        font.pixelSize: 14
        text: "HEX: " + root.colorPresenter.hex
    }
    Label {
        font.pixelSize: 14
        text: "HSV: " + root.colorPresenter.hsv.join(", ")
    }
    Label {
        font.pixelSize: 14
        text: "LAB: " + root.colorPresenter.lab.join(", ")
    }
    Label {
        font.pixelSize: 14
        text: "Name: " + root.colorPresenter.name
    }
}
