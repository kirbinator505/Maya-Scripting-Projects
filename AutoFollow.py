import maya.cmds as cmds

Constrainers = []
TConstraints = []
RConstraints = []
SConstraints = []
Names = 0
Constrained = 0
Control = 0
AttrTarget = 0
FTTarget = 0
FRTarget = 0
TransMD = 0
RotMD = 0

def setConstrainers(fieldName):
    #set the constrainers into a list
    global Constrainers
    Constrainers = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(Constrainers))
    
def setNames(inputText):
    #get the names and split them into the list
    global Names
    Names = inputText

def setConstrained(fieldName):
    global Constrained
    Constrained = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(Constrained))

def setControl(fieldName):
    global Control
    Control = cmds.ls(sl=True)
    cmds.textField(fieldName, edit=True, ip=1, tx=nameConcat(Control))

def makeConstraints():
    global TConstraints
    global RConstraints
    global SConstraints
    global Constrained
    #                           !!!default weights for constraints is 0!!!
    #for obj in Constrainers:
    TConstraints.append(cmds.parentConstraint(Constrainers, Constrained, maintainOffset=True, name="%sTranslateConstraint" % Control[0], skipRotate=['x','y','z'], w=0))

    #for obj in Constrainers:
    RConstraints.append(cmds.parentConstraint(Constrainers, Constrained, maintainOffset=True, name="%sRotateConstraint" % Control[0],skipTranslate=['x', 'y', 'z'], w=0))

    for obj in Constrainers:
        SConstraints.append(cmds.scaleConstraint(obj, Constrained, maintainOffset=True, w=0))

def makeMultiplyNodes():
    global TransMD
    global RotMD
    TransMD = cmds.shadingNode('multiplyDivide', n='%s_Translate_MD' % Control[0], au=True)
    RotMD = cmds.shadingNode('multiplyDivide', n='%s_Rotate_MD' % Control[0], au=True)

def makeAttr():
    #enum attr
    cmds.addAttr(Control, ln=cmds.textField('Attribute_Name', query=True, tx=True), at='enum', en=cmds.textField('Constrainer_Names', query=True, tx=True))
    editTarget = Control[0] + "." + cmds.textField('Attribute_Name', query=True, tx=True)
    cmds.setAttr(editTarget, edit=True, keyable=True)
    global AttrTarget
    AttrTarget = editTarget

    #follow Translate attr
    global FTTarget
    if not cmds.attributeQuery('FollowTranslate', node=Control[0], exists=True):
        cmds.addAttr(Control, ln='FollowTranslate', at='double', min=0, max=1, dv=1)
        FTTarget = '%s.FollowTranslate' % (Control[0])
        cmds.setAttr(FTTarget, e=True, keyable=True)

    # follow Rotate attr
    global FRTarget
    if not cmds.attributeQuery('FollowRotate', node=Control[0], exists=True):
        cmds.addAttr(Control, ln='FollowRotate', at='double', min=0, max=1, dv=1)
        FRTarget = '%s.FollowRotate' % (Control[0])
        cmds.setAttr(FRTarget, e=True, keyable=True)

def LinkNodes():
    #connect constraint to MD
    cmds.connectAttr("%s.constraintTranslate" % TConstraints[0][0], "%s.input1" % TransMD, f=True)
    cmds.connectAttr("%s.constraintRotate" % RConstraints[0][0], "%s.input1" % RotMD, f=True)

    #connect Ctrl Attribute to MD
    cmds.connectAttr(FTTarget, "%s.input2X" % TransMD, f=True)
    cmds.connectAttr(FTTarget, "%s.input2Y" % TransMD, f=True)
    cmds.connectAttr(FTTarget, "%s.input2Z" % TransMD, f=True)
    cmds.connectAttr(FRTarget, "%s.input2X" % RotMD, f=True)
    cmds.connectAttr(FRTarget, "%s.input2Y" % RotMD, f=True)
    cmds.connectAttr(FRTarget, "%s.input2Z" % RotMD, f=True)

    #connect MD to Constrained
    cmds.connectAttr("%s.output" %TransMD, "%s.translate" % Constrained[0], f=True)
    cmds.connectAttr("%s.output" % RotMD, "%s.rotate" % Constrained[0], f=True)

    #disconnect constraint from Constrained
    cmds.disconnectAttr("%s.constraintTranslateX" % TConstraints[0][0], "%s.translateX" % Constrained[0])
    cmds.disconnectAttr("%s.constraintTranslateY" % TConstraints[0][0], "%s.translateY" % Constrained[0])
    cmds.disconnectAttr("%s.constraintTranslateZ" % TConstraints[0][0], "%s.translateZ" % Constrained[0])
    cmds.disconnectAttr("%s.constraintRotateX" % RConstraints[0][0], "%s.rotateX" % Constrained[0])
    cmds.disconnectAttr("%s.constraintRotateY" % RConstraints[0][0], "%s.rotateY" % Constrained[0])
    cmds.disconnectAttr("%s.constraintRotateZ" % RConstraints[0][0], "%s.rotateZ" % Constrained[0])

def linkAttributes():
    global AttrTarget
    global SConstraints
    global TConstraints
    global RConstraints
    i = 0
    #for every constrainer, run the code that flips through each attribute and links it to that constraint weight
    for trgt in Constrainers:
        t=0
        r=0
        s=0
        cmds.setAttr(AttrTarget, i)

        tActive = str(TConstraints[0][0]) + "." + str(Constrainers[i]) + "W" + str(i)
        rActive = str(RConstraints[0][0]) + "." + str(Constrainers[i]) + "W" + str(i)
        sActive = str(SConstraints[i][0]) + "." + str(Constrainers[i]) + "W" + str(i)

        #making driven keyframes for Translate constraints
        for const in Constrainers:
            #check if const is the active constraint, if yes, set to 1, if no, set to 0
            if str(TConstraints[0][0]) + "." + str(Constrainers[t]) + "W" + str(t) == tActive:
                cmds.setAttr(str(TConstraints[0][0]) + "." + str(Constrainers[t]) + "W" + str(t), 1)
            else:
                cmds.setAttr(str(TConstraints[0][0]) + "." + str(Constrainers[t]) + "W" + str(t), 0)
            cmds.setDrivenKeyframe(str(TConstraints[0][0]) + "." + str(Constrainers[t]) + "W" + str(t), cd=AttrTarget, itt="linear", ott="linear")
            t+=1

        # making driven keyframes for Translate constraints
        for const in Constrainers:
            # check if const is the active constraint, if yes, set to 1, if no, set to 0
            if str(RConstraints[0][0]) + "." + str(Constrainers[r]) + "W" + str(r) == rActive:
                cmds.setAttr(str(RConstraints[0][0]) + "." + str(Constrainers[r]) + "W" + str(r), 1)
            else:
                cmds.setAttr(str(RConstraints[0][0]) + "." + str(Constrainers[r]) + "W" + str(r), 0)
            cmds.setDrivenKeyframe(str(RConstraints[0][0]) + "." + str(Constrainers[r]) + "W" + str(r), cd=AttrTarget, itt="linear", ott="linear")
            r += 1

        #making driven keyframes for scale constraints
        for const in SConstraints:
            # check if const is the active constraint, if yes, set to 1, if no, set to 0
            if str(const[0]) + "." + str(Constrainers[s]) + "W" + str(s) == sActive:
                cmds.setAttr(str(const[0]) + "." + str(Constrainers[s]) + "W" + str(s), 1)
            else:
                cmds.setAttr(str(const[0]) + "." + str(Constrainers[s]) + "W" + str(s), 0)
            cmds.setDrivenKeyframe(str(SConstraints[s][0]) + "." + str(Constrainers[s]) + "W" + str(s), cd=AttrTarget, itt="linear", ott="linear")
            s+=1

        i+=1

def makeFollow():
    makeConstraints()
    makeAttr()
    makeMultiplyNodes()
    LinkNodes()
    linkAttributes()
    cmds.setAttr(AttrTarget, 0)

def nameConcat(objs):
    newName = ""
    i=0
    for obj in objs:
        newName = newName + obj + ", "
        i += 1
    return newName

def Clear():
    global Constrainers
    global TConstraints
    global RConstraints
    global SConstraints
    global Control
    global Names
    global Constrained
    global AttrTarget
    Constrainers = []
    TConstraints = []
    RConstraints = []
    SConstraints = []
    Names = []
    Constrained = 0
    Control = 0
    AttrTarget = 0
    cmds.textField('Constrainers', edit=True, ip=1, tx="")
    cmds.textField('Constrainers', edit=True, ip=1, pht="Select Constrainers")
    cmds.textField('Constrainer_Names', edit=True, ip=1, tx="")
    cmds.textField('Constrainer_Names', edit=True, ip=1, pht="Name of Constrainers for Enum")
    cmds.textField('Constrained', edit=True, ip=1, tx="")
    cmds.textField('Constrained', edit=True, ip=1, pht="Select Constrained Parent Group")
    cmds.textField('Control_Field', edit=True, ip=1, tx="")
    cmds.textField('Control_Field', edit=True, ip=1, pht="Select Control for Attribute")
    cmds.textField('Attribute_Name', edit=True, ip=1, tx="")
    cmds.textField('Attribute_Name', edit=True, ip=1, pht="Name of Attribute")

def GenerateWindow():
    FollowBuilderWindow = "Follow_Builder"
    if cmds.window(FollowBuilderWindow, ex = True):
        cmds.deleteUI(FollowBuilderWindow, window = True)
    FollowBuilderWindow = cmds.window("Follow_Builder", wh = (500, 300), t = "Select effectors, effected, and control", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj=True, p=FollowBuilderWindow)

    FlowLayout1 = cmds.flowLayout("Flow_Layout1", p = ColumnLayout, wr = True)
    cmds.textField('Constrainers', w=300, p=FlowLayout1, editable=False, ip=1, pht="Select Constrainers")
    cmds.button("Set_Constrainers", l = "Set", p = FlowLayout1, c = 'setConstrainers("Constrainers")')

    FlowLayout2 = cmds.flowLayout("Flow_Layout2", p=ColumnLayout, wr=True)
    cmds.textField('Constrainer_Names', w=300, p=FlowLayout2, editable=True, ip=1, pht="Name of Constrainers for Enum, seperate with :")
    #cmds.button("Set_Names", l="Set", p=FlowLayout2, c='setNames(cmds.textField("Constrainer_Names", query = True, tx = True))')

    FlowLayout3 = cmds.flowLayout("Flow_Layout3", p=ColumnLayout, wr=True)
    cmds.textField('Constrained', w=300, p=FlowLayout3, editable=False, ip=1, pht="Select Constrained Parent Group")
    cmds.button("Set_Constrained", l="Set", p=FlowLayout3, c='setConstrained("Constrained")')

    FlowLayout4 = cmds.flowLayout("Flow_Layout4", p=ColumnLayout, wr=True)
    cmds.textField('Control_Field', w=300, p=FlowLayout4, editable=False, ip=1, pht="Select Control for Attribute")
    cmds.button("Set_Ctrl_Attr", l="Set", p=FlowLayout4, c='setControl("Control_Field")')

    FlowLayout5 = cmds.flowLayout("Flow_Layout5", p=ColumnLayout, wr=True)
    cmds.textField('Attribute_Name', w=300, p=FlowLayout5, editable=True, ip=1, pht="Name of Attribute")

    FlowLayout6 = cmds.flowLayout("Flow_Layout6", p=ColumnLayout, wr=True)
    cmds.button("Make_Follow", l="Make Follow", p=FlowLayout6, c='makeFollow()')

    FlowLayout7 = cmds.flowLayout("Flow_Layout7", p=ColumnLayout, wr=True)
    cmds.button("Clear_Bttn", l="Clear", p=FlowLayout7, c='Clear()')

    cmds.showWindow(FollowBuilderWindow)
GenerateWindow()