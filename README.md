MillanDict
==========

Macmillan dictionary source for Anki

Turn off Global Shortcuts with `turn_on_global_shortcut_routine=False`

PyQxt GlobalShortcut (pyqxtgs) wrapper
--------------------------------------

Requirements:
* `PyQt4-devel` or similar
* `SIP`
* maby I have sth forgotten

Compilation:
`
cd pyqxtgs
qmake-qt4
make

cd sip
python configure.py
`

Now open `pyqxtgs/sip/Makefile` and add `-I/usr/include/QxtCore -I/usr/include/QxtGui` to `CPPFLAGS`

Then:
`
make
`

Copy `pyqxtgs.so` to Anki plugin directory.
Copy `libpyqxtgs.so*` to directory where the dynamic linker will be looking for.
It can be eg. `/usr/lib`. You will probably have to run `ldconfig` to update dynamic linker library database.

