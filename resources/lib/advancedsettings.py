import xbmc,xbmcvfs
from xml.dom import minidom
import utils as utils

class AdvancedSettings:
    as_file = xbmc.translatePath('special://home/userdata/advancedsettings.xml')
    doc = None
    
    def __init__(self):

        #read in the file, or make a blank one if it doesn't exist            
        if(xbmcvfs.exists(self.as_file)):
            self.doc = minidom.parse(self.as_file)
        else:
            self.doc.minidom.Document()
            topNode = self.doc.createElement('advancedsettings')
            self.doc.appendchild(topNode)

    def listNodes(self,aNode = None):
        result = []
        
        if(aNode == None):
            #use the root node
            result = self.__parseNodes(self.doc.documentElement)
        else:
            result = self.__parseNodes(self.doc.getElementsByTagName(aNode)[0])
            
        return result
                

    def getNode(self,parent,node):
        if(parent == ''):
            parent = None

        #get the top level node
        nodeList = self.listNodes(parent)
        foundNode = None
        
        for aNode in nodeList:
            if(aNode.name == node):
                foundNode = aNode

        return foundNode

    def renameNode(self,node,newName):
        #get the child
        childNode = self.doc.documentElement.getElementsByTagName(node.name)[0]

        childNode.tagName = newName

        self._writeFile()

    def updateValue(self,node,newValue):
    
        #get the child
        childNode = self.doc.documentElement.getElementsByTagName(node.name)[0]

        #set a new value, or create one if blank
        if(len(childNode.childNodes) > 0):
            childNode.firstChild.nodeValue = newValue
        else:
            valueNode = self.doc.createTextNode(newValue)
            childNode.appendChild(valueNode)

        self._writeFile()

    def deleteNode(self,node):
        #get the xml node from the dom
        childNode = self.doc.documentElement.getElementsByTagName(node.name)[0]

        #remove this node from the parent
        parentNode = childNode.parentNode
        parentNode.removeChild(childNode)

        self._writeFile()

    def addNode(self,parent,child):
        parentNode = None

        if(parent == 'advancedsettings'):
            #hack in case we're already at the top
            parentNode = self.doc.documentElement
        else:
            #get the parent from the dom
            parentNode = self.doc.documentElement.getElementsByTagName(parent)[0]

        #remove any text children from this node (if they exist)
        if(len(parentNode.childNodes) == 1 and parentNode.firstChild.nodeType == self.doc.TEXT_NODE):
            parentNode.removeChild(parentNode.firstChild)

        childNode = self.doc.createElement(child.name)

        #only add value if there is on
        if(child.value != ''):
            value = self.doc.createTextNode(child.value)
            childNode.appendChild(value)

        #add the child
        parentNode.appendChild(childNode)

        self._writeFile()
        

    def _writeFile(self):
        file = xbmcvfs.File(self.as_file,'w')
        file.write(str(self.doc.toxml()))
        file.close()

    def __parseNodes(self,nodeList):
        result = []

        for node in nodeList.childNodes:
            if(node.nodeType == self.doc.ELEMENT_NODE):
                aSetting = SettingNode(node.nodeName)

                if(len(node.childNodes) > 0 and node.firstChild.nodeType != self.doc.TEXT_NODE):
                    aSetting.hasChildren = True
                
                if(len(node.childNodes) > 0 and node.firstChild.nodeType == self.doc.TEXT_NODE):
                    aSetting.value = node.childNodes[0].nodeValue
                        
                aSetting.parent = node.parentNode.nodeName
                
                result.append(aSetting)
        return result

class SettingNode:
    name = ''
    value = ''
    hasChildren = False
    parent = ''
    
    def __init__(self,name):
        self.name = name
