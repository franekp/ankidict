#include "shortcut.hpp"

PyGlobalShortcutHandler::PyGlobalShortcutHandler()
    : QObject(0)
{
  connect(&m_globalShortcut, SIGNAL(activated()), SLOT(handleGlobalShortcut()));
}

void PyGlobalShortcutHandler::enable()
{
  m_globalShortcut.setEnabled(true);
}

void PyGlobalShortcutHandler::disable()
{ 
  m_globalShortcut.setEnabled(false);
}

void PyGlobalShortcutHandler::setShortcut(QString shortcut)
{
  m_globalShortcut.setShortcut(QKeySequence(shortcut));
}

void PyGlobalShortcutHandler::handleGlobalShortcut()
{
  emit onGlobalShortcut();
}


