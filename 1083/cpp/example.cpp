#include "example.h"
#include <QSize>
#include <QPushButton>

GraphicsView::GraphicsView()
{   
    scene->addText("ABC");
    this->scale(20, 20);
    setScene(scene);
}

void GraphicsView::test()
{
    this->scale(0.9, 0.9);
}

void GraphicsView::sizeHint()
{
    this->setSceneRect(500, 500, 500, 500);
}

GraphicsView::~GraphicsView(){}

Test::Test()
{
    setLayout(layout);
    layout->addWidget(view);

    auto_button = new QPushButton("auto");
    connect(auto_button, &QPushButton::clicked, view, &GraphicsView::test, Qt::AutoConnection);
    layout->addWidget(auto_button);

    queued_button = new QPushButton("queued");
    connect(queued_button, &QPushButton::clicked, view, &GraphicsView::test, Qt::QueuedConnection);
    layout->addWidget(queued_button);

}

Test::~Test(){}