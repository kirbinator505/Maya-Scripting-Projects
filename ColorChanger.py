import maya.cmds as cmds
colorNum = 0
def SetColor (num):
    selectionList = cmds.ls(sl=True)
    #make stuff below work with iterables
    for i in selectionList:
        selectionTarget = cmds.listRelatives(i, shapes = True)[0]
        cmds.setAttr(selectionTarget + '.overrideEnabled', True)
        cmds.setAttr(selectionTarget + '.overrideRGBColors', 0)
        cmds.setAttr(selectionTarget + '.overrideColor', num) #max 31 replace the number with entered value

def GenerateWindow():
    ColorWindow = "Color_Window"
    if cmds.window(ColorWindow, ex = True):
        cmds.deleteUI(ColorWindow, window = True)
    ColorWindow = cmds.window("Color_Window", wh = (500, 300), t = "enter value between 0 and 31", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj = True, p = ColorWindow)
    NumVar = cmds.intField("Int_Field", min = 0, max = 31, p = ColumnLayout)
    cmds.button("RecolorButton", l = "Color", p = ColumnLayout, c = 'SetColor(cmds.intField("Int_Field", query = True, v = True))')

    cmds.showWindow(ColorWindow)
GenerateWindow()