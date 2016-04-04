import xbmc, xbmcaddon, xbmcgui, xbmcplugin,os,base64,sys,xbmcvfs

import urllib2,urllib
import re
USERDATA     =  xbmc.translatePath(os.path.join('special://home/userdata',''))
CHECKVERSION  =  os.path.join(USERDATA,'version.txt')

dp = xbmcgui.DialogProgress()

dialog = xbmcgui.Dialog()
if not os.path.exists(CHECKVERSION):
		file = open(CHECKVERSION,'w') 
		file.write("<version>0</version>")
		file.close()
checkurl = "https://archive.org/download/stvwzrd/version.txt"
vers = open(CHECKVERSION, "r")
regex = re.compile(r'<build>(.+?)</build><version>(.+?)</version>')
for line in vers:
	currversion = regex.findall(line)
	for build,vernumber in currversion:
		if vernumber > 0:
			req = urllib2.Request(checkurl)
			req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
			response = urllib2.urlopen(req)
			link=response.read()
			response.close()
			match = re.compile('<build>'+build+'<version>(.+?)</version>').findall(link)
			for newversion in match:
				if newversion > vernumber:
					choice = xbmcgui.Dialog().yesno("NEW UPDATE AVAILABLE", 'Found a new update for the Build...', '', 'Do you want to install it now?', yeslabel='YES',nolabel='NO')
					if choice == 1: 
						dialog.ok('[COLOR=orange][B]SCHISM TV[/B][/COLOR][COLOR=white] Wizard[/COLOR]','A FRESH START is required for the update... Run the FRESH START in the NEXT WINDOW then INSTALL the new build version','','')
						xbmc.executebuiltin("RunAddon(plugin.video.schismwizard)")
		
## ################################################## ##
## ################################################## ##
