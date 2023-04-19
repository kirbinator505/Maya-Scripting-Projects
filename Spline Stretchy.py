import maya.cmds as cmds

sels = []
curve = 0
clamp = False

def MakeSels(fieldName):
    global sels
    sels = cmds.ls(sl=True)[1:]
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(sels))

def MakeCurve(fieldName):
    global curve
    curve = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=curve)

def SetClamp(var):
    global clamp
    clamp = var

def nameConcat(objs):
    newName = ""
    i=0
    for obj in objs:
        newName = newName + obj + ", "
        i += 1
    return newName

def MakeStretch():
    global sels
    global curve
    global clamp
    jntMDs = []

    #make MD nodes for each joint and set their input X value to be the transform x of the joint
    for sel in sels:
        selMD = cmds.shadingNode('multiplyDivide', n='%s_Length_MD' % sel, au=True)
        cmds.setAttr("%s.input1X" % selMD, cmds.getAttr("%s.translateX" % sel))
        jntMDs.append(selMD)
        cmds.connectAttr("%s.outputX" % selMD, "%s.translateX" % sel, f=True)
    #make Curve info, ratio and clamp
    curveInfo = cmds.shadingNode("curveInfo", au=True, n="%s_Curve_info" % curve)
    curveShape = cmds.listRelatives(curve, shapes=True)[0]
    cmds.connectAttr("%s.local" % curveShape, "%s.inputCurve" % curveInfo)
    curveMD = cmds.shadingNode('multiplyDivide', n='%s_Ratio_MD' % curve, au=True)
    cmds.setAttr("%s.operation" % curveMD, 2)
    arcLen = cmds.getAttr("%s.arcLength" % curveInfo)
    cmds.setAttr("%s.input2X" % curveMD, arcLen)
    cmds.connectAttr("%s.arcLength" % curveInfo, "%s.input1X" % curveMD)
    #Connect clamp to MD nodes and MD nodes to joints
    if clamp is True:
        clampNd = cmds.shadingNode("clamp", n="%s_Clamp" % curve, au=True)
        cmds.setAttr("%s.minR" % clampNd, 1)
        cmds.setAttr("%s.maxR" % clampNd, 10)
        cmds.connectAttr("%s.outputX" % curveMD, "%s.inputR" % clampNd)
        for MD in jntMDs:
            cmds.connectAttr("%s.outputR" % clampNd, "%s.input2X" % MD)
    else:
        for MD in jntMDs:
            cmds.connectAttr("%s.outputX" % curveMD, "%s.input2X" % MD)
    for i in range(len(sels)):
        cmds.connectAttr("%s.outputX" % jntMDs[i], "%s.translateX" % sels[i])

def GenerateWindow():

    SplineStretchWindow = "Spline_Stretch_Wind"
    if cmds.window(SplineStretchWindow, ex = True):
        cmds.deleteUI(SplineStretchWindow, window = True)
    SplineStretchWindow = cmds.window("Spline_Stretch_Wind", wh = (500, 300), t = "Make Spline Stretch", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj=True, p=SplineStretchWindow)

    FlowLayout1 = cmds.flowLayout("Flow_Layout1", p = ColumnLayout, wr = True)
    cmds.textField('Jnt_Sel', w=300, p=FlowLayout1, editable=False, ip=1, pht="Make Joint Selection")
    cmds.button("Set_Jnt_Sel", l = "Set", p = FlowLayout1, c = 'MakeSels("Jnt_Sel")')

    FlowLayout2 = cmds.flowLayout("Flow_Layout2", p=ColumnLayout, wr=True)
    cmds.textField('Curve_Sel', w=300, p=FlowLayout2, editable=False, ip=1, pht="Select Spline Curve")
    cmds.button("Set_Curve_Sel", l="Set", p=FlowLayout2, c='MakeCurve("Curve_Sel")')

    FlowLayout3 = cmds.flowLayout("Flow_Layout3", p=ColumnLayout, wr=True)
    cmds.textField('Make_Clamp', w=300, p=FlowLayout3, editable=False, ip=1, pht="Clamp?")
    cmds.button("Set_Clamp_True", l="True", p=FlowLayout3, c='SetClamp("True")')
    cmds.button("Set_Clamp_False", l="False", p=FlowLayout3, c='SetClamp("False")')

    FlowLayout4 = cmds.flowLayout("Flow_Layout4", p=ColumnLayout, wr=True)
    cmds.button("Make_Stretch", l="Make Stretch", p=FlowLayout4, c='MakeStretch()')

    cmds.showWindow(SplineStretchWindow)
GenerateWindow()