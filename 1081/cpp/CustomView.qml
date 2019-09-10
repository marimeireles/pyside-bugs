import QtCharts 2.13
import QtQuick 2.13
import CustomView 1.0

CustomView {
    ChartView {
        anchors.fill: parent
        antialiasing: true
        animationOptions: ChartView.AllAnimations
        legend.visible: false

        // Replacing this PieSeries with another type of series works fine.
        PieSeries {
            id: pieSeries
            PieSlice { label: "eaten"; value: 94.9 }
            PieSlice { label: "not yet eaten"; value: 5.1 }
        }
    }
}