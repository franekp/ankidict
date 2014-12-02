import millandict_addon as addon

conf = addon.Config()
conf.enable_global_shortcut = True
conf.enable_debug_menu = True

millan = addon.MillanDict(conf)
