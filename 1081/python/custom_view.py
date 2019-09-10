from PySide2.QtQuick import QQuickItem


class CustomView(QQuickItem):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)