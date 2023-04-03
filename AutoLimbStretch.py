import maya.cmds as cmds

TCtrl = 0
IKBJ = 0
IKBC = 0
IKMJ = 0
IKTJ = 0
IKTC = 0
LimbSide = ""
SpaceDir = False

#set selections
def SetTCtrl(fieldName):
    global TCtrl
    TCtrl = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=TCtrl)
def SetIKBJ(fieldName):
    global IKBJ
    IKBJ = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=IKBJ)
def SetIKBC(fieldName):
    global IKBC
    IKBC = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=IKBC)
def SetIKMJ(fieldName):
    global IKMJ
    IKMJ = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=IKMJ)
def SetIKTJ(fieldName):
    global IKTJ
    IKTJ = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=IKTJ)
def SetIKTC(fieldName):
    global IKTC
    IKTC = cmds.ls(sl=True)[0]
    cmds.textField(fieldName, edit=True, ip=1, tx=IKTC)
def SetLimbSide(fieldName):
    global LimbSide
    LimbSide = cmds.textField(fieldName, query=True, tx=True)
    print(LimbSide)
def SetPosOrNeg(set, fieldName):
    global SpaceDir
    SpaceDir = set
    if set is True:
        cmds.textField(fieldName, edit=True, ip=1, tx="-")
    else:
        cmds.textField(fieldName, edit=True, ip=1, tx="+")

#Make nodes, attributes, enter Connections and data
def MakeStretch():
    global TCtrl
    global IKBJ
    global IKTJ
    global LimbSide
    global SpaceDir
    Limb = LimbSide.split("_")[1]
    #Make Attributes
    #make GlobalScale Attribute if not already made, set it to variable either way
    MasterScale=0
    if cmds.attributeQuery('MasterScale', n=TCtrl, ex=True):
        print("Already Exists")
        MasterScale = '%s.MasterScale' %TCtrl
    else:
        print("Make New Attr")
        MasterScale = '%s.MasterScale' % TCtrl
        cmds.addAttr(TCtrl, ln='MasterScale',at='float', min=1, dv=1)
        cmds.setAttr(MasterScale, edit=True, keyable=True)
        cmds.connectAttr(MasterScale, "%s.scaleX" % TCtrl)
        cmds.connectAttr(MasterScale, "%s.scaleY" % TCtrl)
        cmds.connectAttr(MasterScale, "%s.scaleZ" % TCtrl)
        cmds.setAttr("%s.scaleX" % TCtrl, l=True, k=False, cb=False)
        cmds.setAttr("%s.scaleY" % TCtrl, l=True, k=False, cb=False)
        cmds.setAttr("%s.scaleZ" % TCtrl, l=True, k=False, cb=False)
    #make Ik Ctrl attributes
    cmds.addAttr(IKTC, ln='Stretch', at='double', min=0, max=1, dv=0)
    StretchAttr = IKTC + ".Stretch"
    cmds.setAttr(StretchAttr, edit=True, keyable=True)
    cmds.addAttr(IKTC, ln='MaxStretch', at='float', min=1, max=10, dv=2)
    StretchMaxAttr = IKTC + ".MaxStretch"
    cmds.setAttr(StretchMaxAttr, edit=True, keyable=True)
    cmds.addAttr(IKTC, ln='%sLength' % Limb, at='float', min=-9.9, max=20, dv=0)
    ArmLengthAttr = IKTC + ".%sLength" % Limb
    cmds.setAttr(ArmLengthAttr, edit=True, keyable=True)
    cmds.addAttr(IKTC, ln='Upper%sLength' % Limb, at='float', min=-9.9, max=20, dv=0)
    UpperArmLengthAttr = IKTC + ".Upper%sLength" % Limb
    cmds.setAttr(UpperArmLengthAttr, edit=True, keyable=True)
    cmds.addAttr(IKTC, ln='Lower%sLength' % Limb, at='float', min=-9.9, max=20, dv=0)
    LowerArmLengthAttr = IKTC + ".Lower%sLength" % Limb
    cmds.setAttr(LowerArmLengthAttr, edit=True, keyable=True)

    #make and move Locators
    Dist_01_Loc = cmds.spaceLocator(a=True, n=LimbSide + "_IK_Dist_01_Loc")[0]
    Dist_02_Loc = cmds.spaceLocator(a=True, n=LimbSide + "_IK_Dist_02_Loc")[0]
    cmds.xform(Dist_01_Loc, ws=True, t=Get_Xform(IKBJ))
    cmds.xform(Dist_02_Loc, ws=True, t=Get_Xform(IKTJ))

    #Make Nodes
    IK_Length_MD = cmds.shadingNode('multiplyDivide', n='%s_IK_Length_MD' %LimbSide, au=True)
    IK_Joint_Ref_MD = cmds.shadingNode('multiplyDivide', n='%s_IK_Joint_Ref_MD' % LimbSide, au=True)
    Stretch_Global_Scale_MD = cmds.shadingNode('multiplyDivide', n='%s_Stretch_Global_Scale_MD' % LimbSide, au=True)
    Stretch_Switch_MD = cmds.shadingNode('multiplyDivide', n='%s_Stretch_Switch_MD' % LimbSide, au=True)
    IK_Stretch_Scalar = cmds.shadingNode('multiplyDivide', n='%s_IK_Stretch_Scalar' % LimbSide, au=True)
    IK_Joint_Length_MD = cmds.shadingNode('multiplyDivide', n='%s_IK_Joint_Length_MD' % LimbSide, au=True)
    IK_Length_Combined_PMA = cmds.shadingNode('plusMinusAverage', n='%s_IK_Length_Combined_PMA' % LimbSide, au=True)
    Upper_Length_PMA = cmds.shadingNode('plusMinusAverage', n='%s_Upper_Length_PMA' % LimbSide, au=True)
    Lower_Length_PMA = cmds.shadingNode('plusMinusAverage', n='%s_Lower_Length_PMA' % LimbSide, au=True)
    Length_Denominator = cmds.shadingNode('plusMinusAverage', n='%s_Length_Denominator' % LimbSide, au=True)
    IK_Stretch_Clamp = cmds.shadingNode('clamp', n='%s_IK_Stretch_Clamp' % LimbSide, au=True)
    IK_Distance = cmds.shadingNode('distanceBetween', n='%s_IK_Distance' % LimbSide, au=True)

    #Edit Nodes
    cmds.setAttr("%s.input1D[0]" % Upper_Length_PMA, cmds.getAttr("%s.translateX" %IKMJ))
    cmds.setAttr("%s.input1D[0]" % Lower_Length_PMA, cmds.getAttr("%s.translateX" % IKTJ))
    cmds.setAttr("%s.operation" % IK_Stretch_Scalar, 2)
    cmds.setAttr("%s.operation" % IK_Length_MD, 2)
    cmds.setAttr("%s.operation" % Stretch_Global_Scale_MD, 2)
    cmds.setAttr("%s.input1X" % IK_Joint_Ref_MD, cmds.getAttr("%s.translateX" %IKMJ))
    cmds.setAttr("%s.input1Y" % IK_Joint_Ref_MD, cmds.getAttr("%s.translateX" % IKTJ))
    cmds.setAttr("%s.input2X" % IK_Length_MD, 10)
    cmds.setAttr("%s.input2Y" % IK_Length_MD, 10)
    cmds.setAttr("%s.input2Z" % IK_Length_MD, 10)
    cmds.setAttr("%s.minR" % IK_Stretch_Clamp, 1)

    #Make Connections
    cmds.connectAttr(ArmLengthAttr, "%s.input1X" % IK_Length_MD, f=True)
    cmds.connectAttr(UpperArmLengthAttr, "%s.input1Y" % IK_Length_MD, f=True)
    cmds.connectAttr(LowerArmLengthAttr, "%s.input1Z" % IK_Length_MD, f=True)
    cmds.connectAttr(StretchAttr, "%s.input2X" % Stretch_Switch_MD, f=True)
    cmds.connectAttr(StretchMaxAttr, "%s.maxR" % IK_Stretch_Clamp, f=True)
    cmds.connectAttr("%s.outputX" % IK_Length_MD, "%s.input2D[0].input2Dx" % IK_Length_Combined_PMA, f=True)
    cmds.connectAttr("%s.outputX" % IK_Length_MD, "%s.input2D[0].input2Dy" % IK_Length_Combined_PMA, f=True)
    cmds.connectAttr("%s.outputY" % IK_Length_MD, "%s.input2D[1].input2Dx" % IK_Length_Combined_PMA, f=True)
    cmds.connectAttr("%s.outputZ" % IK_Length_MD, "%s.input2D[1].input2Dy" % IK_Length_Combined_PMA, f=True)
    cmds.connectAttr("%s.output2Dx" % IK_Length_Combined_PMA, "%s.input2X" % IK_Joint_Ref_MD, f=True)
    cmds.connectAttr("%s.output2Dy" % IK_Length_Combined_PMA, "%s.input2Y" % IK_Joint_Ref_MD, f=True)
    cmds.connectAttr("%s.outputX" % IK_Joint_Ref_MD, "%s.input1D[1]" % Upper_Length_PMA, f=True)
    cmds.connectAttr("%s.outputY" % IK_Joint_Ref_MD, "%s.input1D[1]" % Lower_Length_PMA, f=True)
    cmds.connectAttr("%s.output1D" % Upper_Length_PMA, "%s.input1D[0]" % Length_Denominator, f=True)
    cmds.connectAttr("%s.output1D" % Lower_Length_PMA, "%s.input1D[1]" % Length_Denominator, f=True)
    cmds.connectAttr("%s.output1D" % Length_Denominator, "%s.input2X" % IK_Stretch_Scalar, f=True)
    cmds.connectAttr("%s.output1D" % Upper_Length_PMA, "%s.input1X" % IK_Joint_Length_MD, f=True)
    cmds.connectAttr("%s.output1D" % Lower_Length_PMA, "%s.input1Y" % IK_Joint_Length_MD, f=True)
    cmds.connectAttr("%s.worldMatrix[0]" % Dist_01_Loc, "%s.inMatrix1" % IK_Distance, f=True)
    cmds.connectAttr("%s.worldMatrix[0]" % Dist_02_Loc, "%s.inMatrix2" % IK_Distance, f=True)
    cmds.connectAttr("%s.distance" % IK_Distance, "%s.input1X" % Stretch_Global_Scale_MD, f=True)
    cmds.connectAttr(MasterScale, "%s.input2X" % Stretch_Global_Scale_MD, f=True)
    cmds.connectAttr("%s.outputX" % Stretch_Global_Scale_MD, "%s.input1X" % Stretch_Switch_MD, f=True)
    cmds.connectAttr(StretchAttr, "%s.input2X" % Stretch_Switch_MD, f=True)
    cmds.connectAttr("%s.outputX" % Stretch_Switch_MD, "%s.input1X" % IK_Stretch_Scalar, f=True)
    cmds.connectAttr("%s.outputX" % IK_Stretch_Scalar, "%s.inputR" % IK_Stretch_Clamp, f=True)
    cmds.connectAttr("%s.outputR" % IK_Stretch_Clamp, "%s.input2X" % IK_Joint_Length_MD, f=True)
    cmds.connectAttr("%s.outputR" % IK_Stretch_Clamp, "%s.input2Y" % IK_Joint_Length_MD, f=True)
    cmds.connectAttr("%s.outputX" % IK_Joint_Length_MD, "%s.translateX" % IKMJ, f=True)
    cmds.connectAttr("%s.outputY" % IK_Joint_Length_MD, "%s.translateX" % IKTJ, f=True)

    if SpaceDir is True:
        IK_Rev_MD = cmds.shadingNode('multiplyDivide', n='%s_IK_Rev_MD' % LimbSide, au=True)
        cmds.setAttr("%s.input2X" % IK_Rev_MD, -1)
        cmds.connectAttr("%s.outputX" % IK_Stretch_Scalar, "%s.input1X" % IK_Rev_MD, f=True)
        cmds.connectAttr("%s.outputX" % IK_Rev_MD, "%s.inputR" % IK_Stretch_Clamp, f=True)

    #parent Constraints
    cmds.parentConstraint(IKBC, Dist_01_Loc, mo=True)
    cmds.parentConstraint(IKTC, Dist_02_Loc, mo=True)

def Get_Xform(obj):

    pos = cmds.xform(obj, q=True, worldSpace=True, translation=True)
    return pos

def GenerateWindow():
    global TCtrl
    global IKBJ
    global IKBC
    global IKMJ
    global IKTJ
    global IKTC
    global LimbSide
    LimbStretchWindow = "Limb_Stretch_Wind"
    if cmds.window(LimbStretchWindow, ex = True):
        cmds.deleteUI(LimbStretchWindow, window = True)
    LimbStretchWindow = cmds.window("Limb_Stretch_Wind", wh = (500, 300), t = "Automatic Limb Stretch Builder", s = True)
    ColumnLayout = cmds.columnLayout("Column_Layout", adj=True, p=LimbStretchWindow)

    FlowLayout1 = cmds.flowLayout("Flow_Layout1", p = ColumnLayout, wr = True)
    cmds.textField('Transform_Ctrl', w=300, p=FlowLayout1, editable=False, ip=1, pht="Select Transform Control")
    cmds.button("Set_TCtrl", l = "Set", p = FlowLayout1, c = 'SetTCtrl("Transform_Ctrl")')

    FlowLayout2 = cmds.flowLayout("Flow_Layout2", p=ColumnLayout, wr=True)
    cmds.textField('IK_Base_Jnt', w=300, p=FlowLayout2, editable=False, ip=1, pht="IK System Base Joint (Shoulder or Hip)")
    cmds.button("Set_IK_B_J", l="Set", p=FlowLayout2, c='SetIKBJ("IK_Base_Jnt")')

    FlowLayout3 = cmds.flowLayout("Flow_Layout3", p=ColumnLayout, wr=True)
    cmds.textField('IK_Base_Ctrl', w=300, p=FlowLayout3, editable=False, ip=1, pht="IK System Base Control (Shoulder or Hip)")
    cmds.button("Set_IK_B_C", l="Set", p=FlowLayout3, c='SetIKBC("IK_Base_Ctrl")')

    FlowLayout4 = cmds.flowLayout("Flow_Layout4", p=ColumnLayout, wr=True)
    cmds.textField('IK_Mid_Jnt', w=300, p=FlowLayout4, editable=False, ip=1, pht="IK System Mid Joint (Elbow or Knee)")
    cmds.button("Set_IK_M_J", l="Set", p=FlowLayout4, c='SetIKMJ("IK_Mid_Jnt")')

    FlowLayout5 = cmds.flowLayout("Flow_Layout5", p=ColumnLayout, wr=True)
    cmds.textField('IK_Tip_Jnt', w=300, p=FlowLayout5, editable=False, ip=1, pht="IK System Tip Joint (Wrist or Ankle)")
    cmds.button("Set_IK_T_J", l="Set", p=FlowLayout5, c='SetIKTJ("IK_Tip_Jnt")')

    FlowLayout6 = cmds.flowLayout("Flow_Layout6", p=ColumnLayout, wr=True)
    cmds.textField('IK_Tip_Ctrl', w=300, p=FlowLayout6, editable=False, ip=1, pht="IK System Tip Ctrl (Wrist or Ankle)")
    cmds.button("Set_IK_T_C", l="Set", p=FlowLayout6, c='SetIKTC("IK_Tip_Ctrl")')

    FlowLayout7 = cmds.flowLayout("Flow_Layout7", p=ColumnLayout, wr=True)
    cmds.textField('Limb_Side', w=300, p=FlowLayout7, editable=True, ip=1, pht="Side and Limb (eg: L_Arm)")
    cmds.button("Set_Limb_Side", l="Set", p=FlowLayout7, c='SetLimbSide("Limb_Side")')

    FlowLayout8 = cmds.flowLayout("Flow_Layout8", p=ColumnLayout, wr=True)
    cmds.textField('World_Space', w=200, p=FlowLayout8, editable=False, ip=1, pht="Limb Dist Positive or Negative")
    cmds.button("Set_World_Space_Pos", l="+", p=FlowLayout8, c='SetPosOrNeg(False, "World_Space_Disp")')
    cmds.button("Set_World_Space_Neg", l="-", p=FlowLayout8, c='SetPosOrNeg(True, "World_Space_Disp")')
    cmds.textField('World_Space_Disp', w=20, p=FlowLayout8, editable=False, ip=1)

    FlowLayout9 = cmds.flowLayout("Flow_Layout9", p=ColumnLayout, wr=True)
    cmds.button("Make_Limb_Stretch", l="Make Limb Stretch", p=FlowLayout9, c='MakeStretch()')

    cmds.showWindow(LimbStretchWindow)
GenerateWindow()