import QtQuick

Item {
    id: root

    property int size: 100
    property var sourceItem
    property int zoom: 3
    property var pos
    property real currentX: pos[0]
    property real currentY: pos[1]
    height: 100
    width: 100
    onPosChanged: magnifierCanvas.requestPaint()

    Canvas {
        id: magnifierCanvas

        height: root.height
        visible: true
        width: root.width

        onPaint: {
            let ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);
            if (!sourceItem || !sourceItem.sourceSize.width || !sourceItem.sourceSize.height)
                return;

            let sourceWidth = sourceItem.sourceSize.width;
            let sourceHeight = sourceItem.sourceSize.height;
            let zoomSize = root.size / root.zoom;

            let imgX = Math.max(0, Math.min(currentX - zoomSize / 2, sourceWidth - zoomSize));
            let imgY = Math.max(0, Math.min(currentY - zoomSize / 2, sourceHeight - zoomSize));

            ctx.drawImage(sourceItem, imgX, imgY, zoomSize, zoomSize, 0, 0, width, height);

            ctx.strokeStyle = "red";
            ctx.lineWidth = 2;
            ctx.beginPath();

            ctx.moveTo(width / 2, height / 2 - 10);
            ctx.lineTo(width / 2, height / 2 + 10);

            ctx.moveTo(width / 2 - 10, height / 2);
            ctx.lineTo(width / 2 + 10, height / 2);
            ctx.stroke();

            ctx.strokeStyle = "black";
            ctx.lineWidth = 2;
            ctx.strokeRect(0, 0, width, height);
        }
    }
}

