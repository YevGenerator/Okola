import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Image {
    id: img

    property var backend
    property int refreshKey: 0

    signal cursorPositionChanged(real x, real y)

    cache: false
    fillMode: Image.PreserveAspectFit
    focus: true
    source: backend.provider_source

    Keys.onPressed: {
        if (event.key === Qt.Key_Q) {
            backend.presenter.speak();
            event.accepted = true;
        }
    }
    onHeightChanged: {
        img.backend.on_size_changed(img.width, img.height);
    }
    onWidthChanged: {
        img.backend.on_size_changed(img.width, img.height);
    }

    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onPositionChanged:{
            img.backend.on_cursor_pos(mouse.x, mouse.y)
            img.backend.color_update()
            cursorPositionChanged(img.backend.cursor_pos[0], img.backend.cursor_pos[1])
            img.focus=true
        }
    }
}
