import urllib,urllib2,re,xbmcplugin,xbmcgui,urlresolver,sys,xbmc,xbmcaddon,os,urlparse,random
from t0mm0.common.addon import Addon
from metahandler import metahandlers
from resources.lib.libraries import cache
from resources.lib.libraries import client
from resources.lib.libraries import cloudflare
import threading
from BeautifulSoup import BeautifulSoup as bs

addon_id = 'plugin.video.docuhub'
selfAddon = xbmcaddon.Addon(id=addon_id)
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
metaset = selfAddon.getSetting('enable_meta')
addon = Addon(addon_id, sys.argv)
HOME         =  xbmc.translatePath('special://home/')
dialog = xbmcgui.Dialog()
def CATEGORIES():
	addDir2('DocuLovers','http://documentarylovers.com/film/genre/',15,icon,fanart)

	addDir2('TopDocumentary','http://topdocumentaryfilms.com/all/',2,icon,fanart)
	addDir2('DocuHeaven','http://documentaryheaven.com/',5,icon,fanart)
	addDir2('DocuAddict','http://documentaryaddict.com/',8,icon,fanart)
	# addDir2('DocuTube','http://www.documentarytube.com/',11,icon4,fanartfeature)
def DOCULOVERSMENU(name,url):
	try:link = open_url(url)
	except:link = cloudflare.request(url, mobile=True)
	addDir2('Search','http://documentarylovers.com/?s=',16,icon,fanart)	
	addDir2('Latest Movies','http://documentarylovers.com/film/',13,icon,fanart)
	addDir2('Top Rated','http://documentarylovers.com/film/?r_sortby=highest_rated&r_orderby=desc',13,icon,fanart)
	addDir2('Most Rated','http://documentarylovers.com/film/?r_sortby=most_rated&r_orderby=desc',13,icon,fanart)
	match=re.compile('href="(.+?)" title=".+?" class="genrelinks">(.+?)</a>').findall(link)
	for url,name in match:
		name = cleanHex(name)
		name = re.sub('&quot;',' ',name)
		name = re.sub('&amp;','&',name)
		url = "http://documentarylovers.com" + url
		addDir2('[GENRE] ' + name,url,13,icon,fanart)

def DOCULOVERSSEARCH(url):

    keyboard = xbmc.Keyboard('', 'Search Documentary', False)
    keyboard.doModal()
    if keyboard.isConfirmed():
        query = keyboard.getText()
	url =  url + query
	DOCULOVERS(name,url)
def DOCULOVERS(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)

        match=re.compile('class="post-thumbnail".+?ref="(.+?)" title="(.+?)".+?ata-original="(.+?)"', re.DOTALL).findall(link)
        matchnext = re.compile('<link\s*rel="next" href="(.+?)"').findall(link)
        for url,name,img in match:
				name = cleanHex(name)
				name = re.sub('&quot;',' ',name)
				name = re.sub('&amp;','&',name)

				addLink(name,url,14,img,fanart)	
        for url in matchnext:
				addDir2('NEXT >>>',url,13,icon,fanart)	
def Doculoversplay(url,name,iconimage):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('id="playVideo" data-video="(.+?)" data-src="(.+?)">').findall(link)		
        for datavideo,url in match:
			if "youtube" in datavideo: url = "https://www.youtube.com/watch?v=" + url
			try:
				resolved=urlresolver.resolve(url)
				addon.resolve_url(resolved)
			except: 
				stream_url = urlresolver.HostedMediaFile(url).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
				xbmc.Player ().play(stream_url,liz,False)					
				
def TOPDOCUMENTARIES(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        soup=bs(link)
        tag=soup.find('nav',{'class':'module clear'})
        match=re.compile('<a href="([^"]+)">(.*?)</a></li>').findall(str(tag))
        for url,name in match:
				name = cleanHex(name)
				name = re.sub('&quot;',' ',name)

				addDir2(name,url,3,icon,fanart)
				
def TOPDOCUMENTARIESLINK(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
          	
        match=re.compile('<span class="excerptpic"><a href="(.+?)" title="(.+?)"><im.+?src="(.+?)" class="').findall(link)
        matchnext=re.compile('<link rel="next" href="(.+?)".+?>').findall(link)

        for url,name,img in match:
				name = cleanHex(name)
				name = re.sub('&quot;',' ',name)
				addLink(name,url,4,img,img)
        for url in matchnext:

				addDir2('NEXT >>>',url,3,icon,fanart)
def PLAYTOPDOCUMENTARIES(url,name,iconimage):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<meta itemprop="embedUrl" content="(.+?)".+?>').findall(link)		
        for url in match:
			try:
				resolved=urlresolver.resolve(url)
				addon.resolve_url(resolved)
			except: 
				stream_url = urlresolver.HostedMediaFile(url).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
				xbmc.Player ().play(stream_url,liz,False)


def DOCUHEAVEN(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<li class="cat-item cat-item.+?"><a href="(.+?)".+?>(.+?)</a>').findall(link)
        for url,name in match:	
			name = cleanHex(name)
			name = re.sub('&quot;',' ',name)
			name = re.sub('&amp;',' ',name)
			url = 'http://documentaryheaven.com' + url
			addDir2(name,url,6,icon,fanart)

def DOCUHEAVENLINK(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<a href="(.+?)" title="(.+?)">\s*<im.+?src="(.+?)"').findall(link)
        matchnext=re.compile('<link rel="next" href="(.+?)"').findall(link)		
			
        for url,name,img in match:	
			name = cleanHex(name)
			name = re.sub('&quot;',' ',name)
			addLink(name,url,7,img,img)
        for url in matchnext:	
			
			addDir2('NEXT >>>',url,6,icon,fanart)
def DOCUHEAVENPLAY(url,name,iconimage):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<ifram.+?src="(.+?)" frameborder=').findall(link)		
        for url in match:
			try:
				resolved=urlresolver.resolve(url)
				addon.resolve_url(resolved)
			except: 
				stream_url = urlresolver.HostedMediaFile(url).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
				xbmc.Player ().play(stream_url,liz,False)		

def DOCUADDICT(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<a title=".+?" href="(.+?)">\s*<i class=.+?span itemprop="genre">(.+?)</span>').findall(link)
        for url,name in match:	
			name = cleanHex(name)
			name = re.sub('&quot;',' ',name)
			name = re.sub('&amp;',' ',name)
			addDir2(name,url,9,icon,fanart)
def DOCUADDICTLINK(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<a title="(.+?)" href="(.+?)">\s*<img class="lazy" alt=".+?" src="(.+?)" />').findall(link)
        matchnext=re.compile('<li class="next">\s*<a rel="next" href="(.+?)">').findall(link)
		
        for name,url,img in match:	
			name = cleanHex(name)
			name = re.sub('&quot;',' ',name)
			name = re.sub('&amp;',' ',name)
			addLink(name,url,10,img,img)

        for url in matchnext:	
			url = "http://documentaryaddict.com/" + url
			addDir2('NEXT >>>',url,9,icon,fanart)	

def DOCUADDICTPLAY(url,name,iconimage):
        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('src="(.+?)" frameborder="').findall(link)		
        for url in match:
			try:
				resolved=urlresolver.resolve(url)
				addon.resolve_url(resolved)
			except: 
				stream_url = urlresolver.HostedMediaFile(url).resolve()
				liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage=iconimage)
				xbmc.Player ().play(stream_url,liz,False)	
				
def DOCUTUBE(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        soup=bs(link)
        tag=soup.find('div',{'class':'panel-body alt categories'})
        match=re.compile('<a href="(.+?)" title=".+?">(.+?)</a>').findall(str(tag))
        for url,name in match:
				url = "http://www.documentarytube.com" + url
				addDir2(name,url,12,icon,fanart)
def DOCUTUBELINK(name,url):

        try:link = open_url(url)
        except:link = cloudflare.request(url, mobile=True)
        match=re.compile('<div class="image-thumb"><a href="(.+?)" class="image-thumb-inner"><img src="(.+?)" alt="(.+?)">').findall(link)
        matchnext=re.compile('<li class="next">\s*<a rel="next" href="(.+?)">').findall(link)
        for url,img,name in match:	
			addLink(name,url,10,img,img)
	

    
def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

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

def addDir2(name,url,mode,iconimage,fanart,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, 'plot': description } )
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
def addLink(name,url,mode,iconimage,description=''):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&description="+str(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        liz.setProperty("IsPlayable","true")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
        return ok
def addDir(name,url,mode,iconimage,itemcount,isFolder=False):
        try:
          if not 'COLOR' in name:
            splitName=name.partition('(')
            simplename=""
            simpleyear=""
            if len(splitName)>0:
                simplename=splitName[0]
                simpleyear=splitName[2].partition(')')
            if len(simpleyear)>0:
                simpleyear=simpleyear[0]
            mg = metahandlers.MetaData()
            meta = mg.get_meta('movie', name=simplename ,year=simpleyear)
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage=meta['cover_url'], thumbnailImage=meta['cover_url'])
            liz.setInfo( type="Video", infoLabels= meta )
            liz.setProperty("IsPlayable","true")
            contextMenuItems = []
            contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
            liz.addContextMenuItems(contextMenuItems, replaceItems=False)
            if not meta['backdrop_url'] == '': liz.setProperty('fanart_image', meta['backdrop_url'])
            else: liz.setProperty('fanart_image', fanart)
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder,totalItems=itemcount)
            return ok
        except:
            u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
            ok=True
            liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
            liz.setInfo( type="Video", infoLabels={ "Title": name } )
            liz.setProperty('fanart_image', fanart)
            liz.setProperty("IsPlayable","true")
            ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isFolder)
            return ok

def open_url(url):
        # url=url.replace(' ','%20')
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

def setView(content, viewType):
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)
    if selfAddon.getSetting('auto-view')=='true':
        xbmc.executebuiltin("Container.SetViewMode(%s)" % selfAddon.getSetting(viewType) )

params=get_params(); url=None; name=None; mode=None; site=None; iconimage=None
try: site=urllib.unquote_plus(params["site"])
except: pass
try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
print "Site: "+str(site); print "Mode: "+str(mode); print "URL: "+str(url); print "Name: "+str(name)
print params


if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==2: TOPDOCUMENTARIES(name,url)
elif mode==3: TOPDOCUMENTARIESLINK(name,url)
elif mode==4: PLAYTOPDOCUMENTARIES(url,name,iconimage)
elif mode==5: DOCUHEAVEN(name,url)
elif mode==6: DOCUHEAVENLINK(name,url)
elif mode==7: DOCUHEAVENPLAY(url,name,iconimage)
elif mode==8: DOCUADDICT(name,url)
elif mode==9: DOCUADDICTLINK(name,url)
elif mode==10: DOCUADDICTPLAY(url,name,iconimage)
elif mode==11: DOCUTUBE(name,url)
elif mode==12: DOCUTUBELINK(name,url)
elif mode==13: DOCULOVERS(name,url)
elif mode==14: Doculoversplay(url,name,iconimage)
elif mode==15: DOCULOVERSMENU(name,url)
elif mode==16: DOCULOVERSSEARCH(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

