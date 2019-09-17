#include <QWidget>
#include <QGraphicsView>
#include <QHBoxLayout>
#include <QPushButton>

class GraphicsView : public QGraphicsView
{
    Q_OBJECT
public:
    GraphicsView();
    ~GraphicsView();
    void test();
    void sizeHint();
    
    QWidget *window = new QWidget;
    QGraphicsScene *scene = new QGraphicsScene;
};

class Test : public QWidget
    // Q_OBJECT
{
public:
    Test();
    ~Test();
    
    QHBoxLayout *layout = new QHBoxLayout;
    QPushButton *auto_button;
    QPushButton *queued_button;
    GraphicsView *view = new GraphicsView;
};