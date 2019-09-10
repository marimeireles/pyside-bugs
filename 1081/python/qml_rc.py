# -*- coding: utf-8 -*-

# Resource object code
#
# Created: Tue Sep 10 15:41:52 2019
#      by: The Resource Compiler for PySide2 (Qt v5.13.1)
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x00\x8e\
i\
mport QtQuick 2.\
13\x0aimport QtQuic\
k.Controls 2.13\x0a\
\x0aApplicationWind\
ow {\x0a    visible\
: true\x0a\x0a    Cust\
omView {\x0a       \
 anchors.fill: p\
arent\x0a    }\x0a}\
\x00\x00\x01\xe3\
i\
mport QtCharts 2\
.13\x0aimport QtQui\
ck 2.13\x0aimport C\
ustomView 1.0\x0a\x0aC\
ustomView {\x0a    \
ChartView {\x0a    \
    anchors.fill\
: parent\x0a       \
 antialiasing: t\
rue\x0a        anim\
ationOptions: Ch\
artView.AllAnima\
tions\x0a        le\
gend.visible: fa\
lse\x0a\x0a        // \
Replacing this P\
ieSeries with an\
other type of se\
ries works fine.\
\x0a        PieSeri\
es {\x0a           \
 id: pieSeries\x0a \
           PieSl\
ice { label: \x22ea\
ten\x22; value: 94.\
9 }\x0a            \
PieSlice { label\
: \x22not yet eaten\
\x22; value: 5.1 }\x0a\
        }\x0a    }\x0a\
}\x0a\
"

qt_resource_name = b"\
\x00\x08\
\x08\x01Z\x5c\
\x00m\
\x00a\x00i\x00n\x00.\x00q\x00m\x00l\
\x00\x0e\
\x06\xa0\x83\x1c\
\x00C\
\x00u\x00s\x00t\x00o\x00m\x00V\x00i\x00e\x00w\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x02\x00\x00\x00\x01\
\x00\x00\x00\x16\x00\x00\x00\x00\x00\x01\x00\x00\x00\x92\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
