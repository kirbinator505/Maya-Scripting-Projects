import maya.cmds as cmds

#selection = cmds.ls(sl=True)
#newAttr = cmds.addAttr(ln="testattr")
FKConstrainer = [0]
IKConstrainer = [0]
RKConstrained = [0]
Control = 0
FKConstraint = []
IKConstraint = []
RevNode = 0
AttrTarget = 0

#set selections
def setFKSelection(fieldName):
    global FKConstrainer
    FKConstrainer = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(FKConstrainer))
def setIKSelection(fieldName):
    global IKConstrainer
    IKConstrainer = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(IKConstrainer))
def setRKSelection(fieldName):
    global RKConstrained
    RKConstrained = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(RKConstrained))
def setCtrlSelection(fieldName):
    global Control
    Control = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(Control))

#concatinate the names together
def nameConcat(objs):
    newName = ""
    i=0
    for obj in objs:
        newName = newName + obj + ", "
        i += 1
    return newName

#add parent and scale constraints
def makeConstraints():
    global FKConstraint
    global IKConstraint
    f=0
    i=0
    for obj in FKConstrainer:
        FKConstraint.append(cmds.parentConstraint(obj, RKConstrained[f], maintainOffset=True))
        f+=1
    for obj in IKConstrainer:
        IKConstraint.append(cmds.parentConstraint(obj, RKConstrained[i], maintainOffset=True))
        i+=1

#add and edit attribute
def addAttribute():
    cmds.addAttr(Control, ln=cmds.textField('Attribute_Name', query=True, tx=True), at='double', min=0, max=1, dv=0)
    editTarget = Control[0] + "." + cmds.textField('Attribute_Name', query=True, tx=True)
    cmds.setAttr(editTarget, edit=True, keyable=True)
    global AttrTarget
    AttrTarget = editTarget

#link FK constraints to attribute
def linkAttributes():
    global FKConstraint
    global RKConstrained
    global IKConstraint
    f=0
    i=0
    for trgt in FKConstraint:
        cmds.connectAttr(AttrTarget,trgt[0]+"."+FKConstrainer[f]+"W0",f=True)
        f+=1
    #Create reverse node connected to attribute
    RevNode = cmds.shadingNode('reverse',au=True,n=(cmds.textField('Attribute_Name', query=True, tx=True) + "Rev"))
    cmds.connectAttr(AttrTarget, (RevNode + ".inputX"), f=True)
    #link IK Constraints to reverse node
    for trgt in IKConstraint:
        cmds.connectAttr((RevNode + ".outputX"), trgt[0]+"."+IKConstrainer[i]+"W1", f=True)
        i+=1

#Link other functions for RK
def makeRK():
    makeConstraints()
    addAttribute()
    linkAttributes()

#UI
def GenerateWindow():
    RKBuilderWindow = "RK_Builder"
    if cmds.window(RKBuilderWindow, ex = True):
        cmds.deleteUI(RKBuilderWindow, window = True)
    RKBuilderWindow = cmds.window("RK_Builder", wh = (500, 300), t = "Select effectors, effected, and control", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj=True, p=RKBuilderWindow)
    FlowLayout1 = cmds.flowLayout("Flow_Layout1", p = ColumnLayout, wr = True)
    cmds.textField('FK_Constraint', w=300, p=FlowLayout1, editable=False, ip=1, pht="Select FK Constrainer")
    cmds.button("Set_FK", l = "Set", p = FlowLayout1, c = 'setFKSelection("FK_Constraint")')
    FlowLayout2 = cmds.flowLayout("Flow_Layout2", p=ColumnLayout, wr=True)
    cmds.textField('IK_Constraint', w=300, p=FlowLayout2, editable=False, ip=1, pht="Select IK Constrainer")
    cmds.button("Set_IK", l="Set", p=FlowLayout2, c='setIKSelection("IK_Constraint")')
    FlowLayout3 = cmds.flowLayout("Flow_Layout3", p=ColumnLayout, wr=True)
    cmds.textField('RK_Constraint', w=300, p=FlowLayout3, editable=False, ip=1, pht="Select RK Constrainer")
    cmds.button("Set_RK", l="Set", p=FlowLayout3, c='setRKSelection("RK_Constraint")')
    FlowLayout4 = cmds.flowLayout("Flow_Layout4", p=ColumnLayout, wr=True)
    cmds.textField('Control_Field', w=300, p=FlowLayout4, editable=False, ip=1, pht="Select Control for Attribute")
    cmds.button("Set_Ctrl_Attr", l="Set", p=FlowLayout4, c='setCtrlSelection("Control_Field")')
    FlowLayout5 = cmds.flowLayout("Flow_Layout5", p=ColumnLayout, wr=True)
    cmds.textField('Attribute_Name', w=300, p=FlowLayout5, editable=True, ip=1, pht="Name of Attribute")
    FlowLayout6 = cmds.flowLayout("Flow_Layout6", p=ColumnLayout, wr=True)
    cmds.button("Set_Ctrl_Attr", l="Make RK", p=FlowLayout6, c='makeRK()')

    cmds.showWindow(RKBuilderWindow)
GenerateWindow()