import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TabBar {
    id: tabs
    property alias index: tabs.currentIndex
    Layout.fillWidth: true

    TabButton {
        text: "Оригінал"
    }
    TabButton {
        text: "Розмальовка"
    }
    TabButton {
        text: "Симуляція зсуву"
    }
    TabButton{
        text: "Корекція"
    }
}
