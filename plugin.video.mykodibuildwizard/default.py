import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,sys
import shutil
import urllib2,urllib
import re
import extract
import time
import downloader
import plugintools
import zipfile
import ntpath

AddonID ='plugin.video.mykodibuildwizard'
USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
selfAddon = xbmcaddon.Addon(id=AddonID)
wizard1 = selfAddon.getSetting('enable_wiz1')
wizard2 = selfAddon.getSetting('enable_wiz2')
wizard3 = selfAddon.getSetting('enable_wiz3')
wizard4 = selfAddon.getSetting('enable_wiz4')
wizard5 = selfAddon.getSetting('enable_wiz5')
backupfull = selfAddon.getSetting('backup_database')
backupaddons = selfAddon.getSetting('backup_addon_data')
ADDON_DATA   =  xbmc.translatePath(os.path.join('special://','home'))
ADDON=xbmcaddon.Addon(id='plugin.video.mykodibuildwizard')
dialog = xbmcgui.Dialog()    
VERSION = "1.0.1"
PATH = "mykodibuildwizard"            
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + AddonID, 'icon.png'))
    


def CATEGORIES():
	addDir('[COLOR red][B]Backup[/B][/COLOR]','url',2,icon,icon,'')
	addDir('[COLOR red][B]Restore[/B][/COLOR]','url',3,icon,icon,'')
	if wizard1!='false':
		try:
			name=unicode(selfAddon.getSetting('name1'))
			url=unicode(selfAddon.getSetting('url1'))
			img=unicode(selfAddon.getSetting('img1'))
			fanart=unicode(selfAddon.getSetting('img1'))
			addDir('[COLOR green][B][Wizard][/B][/COLOR] ' +name,url,1,img,fanart,'')
		except: pass
	if wizard2!='false':
		try:
			name=unicode(selfAddon.getSetting('name2'))
			url=unicode(selfAddon.getSetting('url2'))
			img=unicode(selfAddon.getSetting('img2'))
			fanart=unicode(selfAddon.getSetting('img2'))
			addDir('[COLOR green][B][Wizard][/B][/COLOR] ' +name,url,1,img,fanart,'')
		except: pass
	if wizard3!='false':
		try:
			name=unicode(selfAddon.getSetting('name3'))
			url=unicode(selfAddon.getSetting('url3'))
			img=unicode(selfAddon.getSetting('img3'))
			fanart=unicode(selfAddon.getSetting('img3'))
			addDir('[COLOR green][B][Wizard][/B][/COLOR] ' +name,url,1,img,fanart,'')
		except: pass
	if wizard4!='false':
		try:
			name=unicode(selfAddon.getSetting('name4'))
			url=unicode(selfAddon.getSetting('url4'))
			img=unicode(selfAddon.getSetting('img4'))
			fanart=unicode(selfAddon.getSetting('img4'))
			addDir('[COLOR green][B][Wizard][/B][/COLOR] ' +name,url,1,img,fanart,'')
		except: pass
	if wizard5!='false':
		try:
			name=unicode(selfAddon.getSetting('name5'))
			url=unicode(selfAddon.getSetting('url5'))
			img=unicode(selfAddon.getSetting('img5'))
			fanart=unicode(selfAddon.getSetting('img5'))
			addDir('[COLOR green][B][Wizard][/B][/COLOR] ' +name,url,1,img,fanart,'')
		except: pass	
		
def ARCHIVE_CB(sourcefile, destfile, message_header, message1, message2, message3, exclude_dirs, exclude_files):
    zipobj = zipfile.ZipFile(destfile , 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(sourcefile)
    for_progress = []
    ITEM =[]
    dp = xbmcgui.DialogProgress()
    dp.create(message_header, message1, message2, message3)
    for base, dirs, files in os.walk(sourcefile):
        for file in files:
            ITEM.append(file)
    N_ITEM =len(ITEM)
    for base, dirs, files in os.walk(sourcefile):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        files[:] = [f for f in files if f not in exclude_files]
        for file in files:
            for_progress.append(file) 
            progress = len(for_progress) / float(N_ITEM) * 100  
            dp.update(int(progress),"Backing Up",'[COLOR yellow]%s[/COLOR]'%file, 'Please Wait')
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])  
    zipobj.close()
    dp.close()	
def BackupWiz():
	if backupfull!='false':
		search_entered =''
		keyboard = xbmc.Keyboard(search_entered, 'Name your Build Backup')
		keyboard.doModal()
		if keyboard.isConfirmed():
			search_entered = keyboard.getText().replace(' ','_')

		if len(search_entered)>1:		
			backupdir=unicode(selfAddon.getSetting('remote_path'))
			to_backup = xbmc.translatePath(os.path.join('special://','home'))
			backup_zip = xbmc.translatePath(os.path.join(backupdir,search_entered+'_build.zip'))
			backup_path = xbmc.translatePath(os.path.join(backupdir,'backup'))    
			dp = xbmcgui.DialogProgress()
			dp.create("BACKUP/RESTORE","Backing Up",'', 'Please Wait')
			dialog.ok("BACKUP/RESTORE", "Click OK to Start your backup", '','')
			exclude_dirs_full =  ['cache','packages']
			exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
			message_header = "Backing up your Build"
			message1 = "Archiving..."
			message2 = ""
			message3 = "Please Wait"
			ARCHIVE_CB(to_backup, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)
	elif backupaddons!='false':
		search_entered =''
		keyboard = xbmc.Keyboard(search_entered, 'Name your Backup')
		keyboard.doModal()
		if keyboard.isConfirmed():
			search_entered = keyboard.getText().replace(' ','_')

		if len(search_entered)>1:		
			backupdir=unicode(selfAddon.getSetting('remote_path'))
			to_backup = xbmc.translatePath(os.path.join('special://','home'))
			backup_zip = xbmc.translatePath(os.path.join(backupdir,search_entered+'_addons_data.zip'))
			backup_path = xbmc.translatePath(os.path.join(backupdir,'backup'))    
			dp = xbmcgui.DialogProgress()
			dp.create("BACKUP/RESTORE","Backing Up",'', 'Please Wait')
			dialog.ok("BACKUP/RESTORE", "Click OK to Start your backup", '','')
			exclude_dirs_full =  ['addons','cache']
			exclude_files_full = ["xbmc.log","xbmc.old.log","kodi.log","kodi.old.log",'.DS_Store','.setup_complete','XBMCHelper.conf']
			message_header = "Backing up Addons Data"
			message1 = "Archiving..."
			message2 = ""
			message3 = "Please Wait"
			ARCHIVE_CB(to_backup, backup_zip, message_header, message1, message2, message3, exclude_dirs_full, exclude_files_full)	

def RestoreWiz():
	
	backupdir=unicode(selfAddon.getSetting('remote_restore_path'))
	import time
	dp = xbmcgui.DialogProgress()
	lib=xbmc.translatePath(os.path.join(backupdir,'addon_data.zip'))
	dp.create("Restoring File","In Progress...",'', 'Please Wait')
	dp.update(0,"", "Extracting Zip Please Wait")
	extract.all(backupdir,ADDON_DATA,dp)
	time.sleep(1)

	 
	 
def OPEN_URL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link
    
    
def wizard(name,url,description):
    path = xbmc.translatePath(os.path.join('special://home/addons','packages'))
    dp = xbmcgui.DialogProgress()
    dp.create("My Wizard","Downloading ",'', 'Please Wait')
    lib=os.path.join(path, name+'.zip')
    try:
       os.remove(lib)
    except:
       pass
    downloader.download(url, lib, dp)
    addonfolder = xbmc.translatePath(os.path.join('special://','home'))
    time.sleep(2)
    dp.update(0,"", "Extracting Zip Please Wait")
    print '======================================='
    print addonfolder
    print '======================================='
    extract.all(lib,addonfolder,dp)
    dialog = xbmcgui.Dialog()
    dialog.ok("DOWNLOAD COMPLETE", 'Unfortunately the only way to get the new changes to stick is', 'to force close kodi. Click ok to force Kodi to close,', 'DO NOT use the quit/exit options in Kodi., If the Force close does not close for some reason please Restart Device or kill task manaully')
    killxbmc()
        
      
        
def killxbmc():
    choice = xbmcgui.Dialog().yesno('Force Close Kodi', 'You are about to close Kodi', 'Would you like to continue?', nolabel='No, Cancel',yeslabel='Yes, Close')
    if choice == 0:
        return
    elif choice == 1:
        pass
    myplatform = platform()
    print "Platform: " + str(myplatform)
    if myplatform == 'osx': # OSX
        print "############   try osx force close  #################"
        try: os.system('killall -9 XBMC')
        except: pass
        try: os.system('killall -9 Kodi')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'linux': #Linux
        print "############   try linux force close  #################"
        try: os.system('killall XBMC')
        except: pass
        try: os.system('killall Kodi')
        except: pass
        try: os.system('killall -9 xbmc.bin')
        except: pass
        try: os.system('killall -9 kodi.bin')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.",'')
    elif myplatform == 'android': # Android  
        print "############   try android force close  #################"
        try: os.system('adb shell am force-stop org.xbmc.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.kodi')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc.xbmc')
        except: pass
        try: os.system('adb shell am force-stop org.xbmc')
        except: pass        
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "Your system has been detected as Android, you ", "[COLOR=yellow][B]MUST[/COLOR][/B] force close XBMC/Kodi. [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Either close using Task Manager (If unsure pull the plug).")
    elif myplatform == 'windows': # Windows
        print "############   try windows force close  #################"
        try:
            os.system('@ECHO off')
            os.system('tskill XBMC.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('tskill Kodi.exe')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im Kodi.exe /f')
        except: pass
        try:
            os.system('@ECHO off')
            os.system('TASKKILL /im XBMC.exe /f')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit cleanly via the menu.","Use task manager and NOT ALT F4")
    else: #ATV
        print "############   try atv force close  #################"
        try: os.system('killall AppleTV')
        except: pass
        print "############   try raspbmc force close  #################" #OSMC / Raspbmc
        try: os.system('sudo initctl stop kodi')
        except: pass
        try: os.system('sudo initctl stop xbmc')
        except: pass
        dialog.ok("[COLOR=red][B]WARNING  !!![/COLOR][/B]", "If you\'re seeing this message it means the force close", "was unsuccessful. Please force close XBMC/Kodi [COLOR=lime]DO NOT[/COLOR] exit via the menu.","Your platform could not be detected so just pull the power cable.")    

def platform():
    if xbmc.getCondVisibility('system.platform.android'):
        return 'android'
    elif xbmc.getCondVisibility('system.platform.linux'):
        return 'linux'
    elif xbmc.getCondVisibility('system.platform.windows'):
        return 'windows'
    elif xbmc.getCondVisibility('system.platform.osx'):
        return 'osx'
    elif xbmc.getCondVisibility('system.platform.atv2'):
        return 'atv2'
    elif xbmc.getCondVisibility('system.platform.ios'):
        return 'ios'


def addDir(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addDir2(name,mode,iconimage,fanart):
        u=sys.argv[0]+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok       
       
        
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
        
                      
params=get_params()
url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
        
        
print str(PATH)+': '+str(VERSION)
print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "IconImage: "+str(iconimage)


def setView(content, viewType):
    # set content type so library shows more views and info
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    
        xbmc.executebuiltin("Container.SetViewMode(50)")
        
        
if mode==None or url==None or len(url)<1:
        CATEGORIES()
       
elif mode==1:
        wizard(name,url,description)
        
elif mode==2:
        BackupWiz()
elif mode==3:
        RestoreWiz()        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

