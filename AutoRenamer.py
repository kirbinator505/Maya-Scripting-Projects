import maya.cmds as cmds

def AutoRenamer(name):
    selection = cmds.ls(sl=True)
    occurance = name.count("#")
    split = name.split("_")
    instance = 1
    for index in range(len(selection)):
        num = "0"*(occurance-len(str(instance))) + str(instance)
        newName = split[0] + "_" + num + "_" + split[2]
        cmds.rename(selection[index], newName)
        instance += 1
def GenerateWindow():
    NamingWindow = "Naming_Window"
    if cmds.window(NamingWindow, ex = True):
        cmds.deleteUI(NamingWindow, window = True)
    NamingWindow = cmds.window("Naming_Window", wh = (500, 300), t = "Naming Window", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj = True, p = NamingWindow)
    NameField = cmds.textField("Text_Field", p = ColumnLayout, pht = "enter in format \"Name_##_NodeType\"")
    cmds.button("ReNameButton", l = "Rename", p = ColumnLayout, c = 'AutoRenamer(cmds.textField("Text_Field", query = True, tx = True))')

    cmds.showWindow(NamingWindow)

GenerateWindow()