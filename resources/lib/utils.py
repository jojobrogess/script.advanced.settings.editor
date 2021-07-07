import xbmc,xbmcvfs
import xbmcgui
import xbmcaddon

__addon_id__ = 'script.advanced.settings.editor'
__Addon = xbmcaddon.Addon(__addon_id__)

def data_dir():
    return __Addon.getAddonInfo('profile')

def addon_dir():
    return __Addon.getAddonInfo('path')

def log(message, loglevel=xbmc.LOGDEBUG):
    xbmc.log(__addon_id__ + "-" + __Addon.getAddonInfo('version') + ": " + message, level=loglevel)

def showNotification(message):      
    xbmcgui.Dialog().notification(getString(30000), message, time=4000, icon=xbmcvfs.translatePath(__Addon.getAddonInfo('path') + "/icon.png"))

def setSetting(name,value):
    __Addon.setSetting(name,value)

def getSetting(name):
    return __Addon.getSetting(name)
    
def getString(string_id):
    return __Addon.getLocalizedString(string_id)

