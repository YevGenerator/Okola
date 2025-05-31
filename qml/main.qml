import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "components"
import "pages"

ApplicationWindow {
    height: 600
    title: "Image Color Picker"
    visible: true
    width: 1000

    FilePicker {
        id: picker

        anchors.left: parent.left
        anchors.top: parent.top

        onSourceChanged: {
            image_provider.load_image(source);
        }
    }

    ColumnLayout {
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: picker.bottom

        Tabs {
            id: tabs

            Layout.fillWidth: true
            anchors.top: parent.top
        }
        StackLayout {
            Layout.fillHeight: true
            currentIndex: tabs.index

            OriginalPage {
                id: originalPage
            }

            FloodFillPage{
                id: floodFillPage
            }
            ColorShiftPage{
                id: shiftPage
            }
            ColorDaltonizePage{
                id: daltonizePage
            }
        }
    }
}
