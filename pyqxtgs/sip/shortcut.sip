%Module pyqxtgs
%Import QtCore/QtCoremod.sip
%Import QtGui/QtGuimod.sip
%If (Qt_4_2_0 -)
 
class PyGlobalShortcutHandler : public QObject {
%TypeHeaderCode
#include "../shortcut.hpp"
%End
public:
  PyGlobalShortcutHandler();
  void enable();
  void disable();
  void setShortcut(QString shortcut);
  
signals:
  void onGlobalShortcut();
  
public slots:
  void handleGlobalShortcut();
}; 
%End 
