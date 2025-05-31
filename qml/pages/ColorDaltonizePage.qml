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
        backend: daltonize_image
    }
    ColumnLayout {
        Layout.fillHeight: true
        Layout.preferredWidth: parent.width * 0.3

        RowLayout {
            anchors.fill: parent

            Column {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.top: parent.top

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
                    id: colorTextPanel

                    colorPresenter: imageView.backend.presenter
                }
            }
            Column {
                Layout.preferredWidth: parent.width * 0.5
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                anchors.top: parent.top

                Magnifier {
                    id: magnifier2

                    pos: imageView.backend.cursor_pos

                    sourceItem: Image {
                        cache: false
                        fillMode: Image.PreserveAspectFit
                        source: original_image.provider_source
                    }
                }
                ColorSquare {
                    id: colorSquareOriginal

                    color: original_image.presenter.color
                }
                ColorText {
                    id: colorTextPanelOriginal

                    colorPresenter: original_image.presenter
                }
            }
        }
        ShiftSettingsPanel {
            anchors.top: colorTextPanel.bottom
            backend: daltonize_image
        }
    }
}
