#include <QApplication>
#include "example.h"

int main(int argc, char *argv[]) {

    QApplication app(argc, argv);
    Test *view = new Test();
    view->show();

    return app.exec();
}