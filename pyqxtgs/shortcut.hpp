#pragma once

#include <QxtGui/QxtGlobalShortcut>

class PyGlobalShortcutHandler : public QObject
{
  Q_OBJECT
public:
  PyGlobalShortcutHandler();
  
  void enable();
  void disable();
  void setShortcut(QString shortcut);
  
signals:
  void onGlobalShortcut();
  
public slots:
  void handleGlobalShortcut();

private:
  QxtGlobalShortcut m_globalShortcut;
};
