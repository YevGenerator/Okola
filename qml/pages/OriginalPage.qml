import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import "../components"

RowLayout {
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    anchors.right: parent.right

    ImageView {
        id: imageView

        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.7
        backend: original_image
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
    }
}
