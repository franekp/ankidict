import os
import sipconfig
from PyQt4 import pyqtconfig
 
build_file = "pyqxtgs.sbf"
config = pyqtconfig.Configuration()
pyqt_sip_flags = config.pyqt_sip_flags
 
os.system(" ".join([ \
    config.sip_bin, \
    "-c", ".", \
    "-b", build_file, \
    "-I", config.pyqt_sip_dir, \
    pyqt_sip_flags, \
    "shortcut.sip" \
]))
 
installs = []
installs.append(["shortcut.sip", os.path.join(config.default_sip_dir, "pyqxtgs")])
installs.append(["shortcut.py", config.default_mod_dir])
 
makefile = pyqtconfig.QtGuiModuleMakefile(
    configuration=config,
    build_file=build_file,
    installs=installs
)
 
makefile.extra_libs = ["pyqxtgs"]
makefile.extra_lib_dirs = [".."]
 
makefile.generate()
 
content = {
    "pyqxtgs_sip_dir":    config.default_sip_dir,
    "pyqxtgs_sip_flags":  pyqt_sip_flags
}
sipconfig.create_config_module("pyqxtgs.py", "pyqxtgs.py.in", content) 
