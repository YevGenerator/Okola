import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Button {
    id: browseButton
    text: "Browse..."

    property string source: ""

    FileDialog {
        id: fileDialog
        title: "Select an image"
        nameFilters: ["Images (*.png *.jpg *.jpeg *.bmp)"]
        onAccepted: {
            let url = selectedFile.toString()
            if (url.startsWith("file://"))
                url = url.substring(8)
            browseButton.source = url
        }
    }

    onClicked: fileDialog.open()
}