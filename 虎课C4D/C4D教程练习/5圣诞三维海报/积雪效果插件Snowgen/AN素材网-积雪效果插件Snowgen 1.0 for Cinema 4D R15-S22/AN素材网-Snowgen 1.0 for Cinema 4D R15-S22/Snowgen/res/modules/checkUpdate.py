import          c4d, os, urllib2, re, webbrowser, random
from os  import path, mkdir
from c4d import gui, plugins

#checkupdate version 1.0


def symbolcache(name, version, folder = "Updated Plugins"):
    '''
Parameters: 
    - name:    Must be the __file__ variable
    - version: A version number. Can be either float or string.
    - folder:  An arbitrary name for the folder in which text file will store.

    '''

    if type(version) is not str: version = str(version)

    pluginFile = os.path.basename(name)
    pluginName = os.path.splitext(pluginFile)[0]
    
    name = pluginName


    prefPath  = c4d.storage.GeGetC4DPath(c4d.C4D_PATH_PREFS)       #Prefs Directory
    smblPath  = path.join(prefPath, "symbolcache").decode("utf-8") #Symbolcache File

    folderPath = path.join(prefPath, folder).decode("utf-8")
    textFile   = path.join(folderPath, name).decode("utf-8")


    def updateFiles():
        with open(smblPath.decode("utf-8"), 'w') as txt: txt.write("  ")    #Clear symbolcache
        with open(textFile.decode("utf-8"), 'w') as txt: txt.write(version) #Update txt
        c4d.RestartMe() #Restart Cinema 4D.


    if path.exists(folderPath) == False: mkdir(folderPath)


    if path.exists(textFile):                                #Check if plugin txt is/was installed.
        with open(textFile.decode("utf-8"), 'r') as txt:     #Read txt
            if float(txt.read()) != float(version):          #Check if txt is older than current
                updateFiles()

    elif path.exists(textFile) == False: 
        updateFiles()





def NewVersion(version, url, pattern = "", ):

    '''
Parameters: 
    - version: A version number. Can be either float or string.
    - url:     Web-page, on which version number figurates.
    - pattern: Text from the web-page, in which version number figurates.

    '''

    if pattern == "": pattern = '<strong>Latest version is(.+?)</strong>'

    result = re.compile(pattern)
    f = os.path.join(os.path.dirname(c4d.storage.GeGetStartupApplication()), "resource", "ssl", "cacert.pem")

    htmlsource = urllib2.urlopen(url, cafile=f)

    htmltext = htmlsource.read()

    latest = re.findall(result, htmltext)[0]

    if float(latest) > float(version): return [True,latest]

    if float(latest) <= float(version): return [False,latest]








def RegisterCheckPlugin(id, version, url, pattern = "", name = "", ):

    '''
Parameters: 
    - id:      A unique plugin ID. You must obtain this from PluginCafe.com
    - version: A version number. Can be either float or string.
    - url:     Web-page, on which version number figurates.
    - pattern: Text from the web-page, in which version number figurates.
    - name:    Must be the __file__ variable

    '''

    if pattern == "": pattern = '<strong>Latest version is(.+?)</strong>'

    pluginFile = os.path.basename(name)
    pluginName = os.path.splitext(pluginFile)[0]
    
    name = pluginName

    class CheckForUpdates(c4d.plugins.CommandData):


        def Execute(self, doc):

            latest = NewVersion(version, url, pattern)[1]

            versionComp = "You are using version " + str(version) + "\nThe  latest  version  is" + str(latest)

            if NewVersion(version, url, pattern)[0]: 
                title  = "New Version Is Available"

                output = versionComp  + "\nPlease check your email to get the update"

            if not NewVersion(version, url, pattern)[0]: 
                title = "New Version Is Not Available"
                output =  versionComp
            
            class Dialog(gui.GeDialog):

                def CreateLayout(self):

                    self.SetTitle("Check For Updates: " + name)
                    
                    self.AddStaticText(       id = 1002, flags = c4d.BFH_CENTER,    initw = 400, inith = 15, name = '', borderstyle = c4d.BORDER_NONE)
                    self.AddMultiLineEditText(id = 1000, flags = c4d.BFH_CENTER, initw = 400, inith = 50, style = c4d.DR_MULTILINE_READONLY)
                    
                    self.AddButton(1001, c4d.BFH_CENTER, 200,15, 'More Info')
                    
                    return True

                def InitValues(self) :

                    self.SetString(1000, output)
                    self.SetString(1002, title)

                    return True


                def Command(self, id, msg):

                    if (id == 1001):
                        webbrowser.open(url,2)
                        self.Close()

                    return True


            Dialog().Open(c4d.DLG_TYPE_MODAL)

            return True

    try:    bmp = c4d.bitmaps.InitResourceBitmap(450000220)
    except: bmp = c4d.bitmaps.InitResourceBitmap(c4d.RESOURCEIMAGE_BOOLGROUP)

    plugins.RegisterCommandPlugin(id     = id, 
                                  str    = "Check For Updates",
                                  info   = c4d.PLUGINFLAG_COMMAND_HOTKEY,
                                  dat    = CheckForUpdates(),
                                  help   = "Check For Update",
                                  icon   = bmp,)



def UpdateAtStartUp(version, url, command, ):
    value = random.randint(1,5)
    if value == 1:
        if NewVersion(version, url,)[0]:

            c4d.CallCommand(command) # Check For Updates