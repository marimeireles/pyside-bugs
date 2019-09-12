#include <QApplication>
#include <QQmlApplicationEngine>
#include "custom_view.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    qmlRegisterType<CustomView>("CustomView", 1, 0, "CustomView");
    QQmlApplicationEngine engine;
    engine.load(QUrl("main.qml"));

    if (engine.rootObjects().empty() )
    {
        return -1;
    }

    return app.exec();
}