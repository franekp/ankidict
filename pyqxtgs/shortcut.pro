TEMPLATE = lib
TARGET = pyqxtgs
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets
CONFIG += qxt
QXT = core gui
HEADERS += shortcut.hpp
SOURCES += shortcut.cpp

