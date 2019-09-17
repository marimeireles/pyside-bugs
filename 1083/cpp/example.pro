QMAKE_CXXFLAGS += -stdlib=libc++
QMAKE_CXXFLAGS += -std=c++11
QMAKE_CXXFLAGS += -mmacosx-version-min=10.7
QMAKE_LFLAGS += -mmacosx-version-min=10.7

TEMPLATE = app
TARGET = 1083
INCLUDEPATH += .

HEADERS += example.h
SOURCES += example.cpp main.cpp


QT += widgets