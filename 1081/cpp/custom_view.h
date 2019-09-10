#include <QQuickItem>

class CustomView : public QQuickItem
{
    Q_OBJECT
public:
    CustomView(QQuickItem *parent = 0);
    ~CustomView();
};