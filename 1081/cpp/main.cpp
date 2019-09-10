#include <QApplication>
#include <QQmlApplicationEngine>
#include "custom_view.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    printf("thats all I have to do in a linux\n");
    qmlRegisterType<CustomView>("CustomView", 1, 0, "CustomView"); //why is this guydoing this
    QQmlApplicationEngine engine;
    engine.load(QUrl("main.qml"));

    if (!engine.rootObjects().empty() )
    {
        return -1;
    }

    return app.exec();
}