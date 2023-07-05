import math
import adsk.core
import adsk.fusion
import traceback


def create_col(
    app: adsk.core.Application,
    center: adsk.core.Point3D,
    sktDiameter: float,
    colHeight: float):

    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    # Get the root component of the active design
    rootComp = design.rootComponent

    # Get extrude features
    extrudes = rootComp.features.extrudeFeatures

    # Create sketch  
    sketches = rootComp.sketches   
    sketch = sketches.add(rootComp.xYConstructionPlane)
    sketchCircles = sketch.sketchCurves.sketchCircles
    circle = sketchCircles.addByCenterRadius(center, sktDiameter*0.5)

    # Get the profile defined by the circle
    prof = sketch.profiles.item(0)


    # Extrude Sample 1: A simple way of creating typical extrusions (extrusion that goes from the profile plane the specified distance).
    # Define a distance extent of 5 cm
    distance = adsk.core.ValueInput.createByReal(colHeight)
    extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)    
    # Get the extrusion body
    return extrude1

def create_col_join(
    app: adsk.core.Application,
    center: adsk.core.Point3D,
    sktDiameter: float,
    colHeight: float):

    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)

    # Get the root component of the active design
    rootComp = design.rootComponent

    # Get extrude features
    extrudes = rootComp.features.extrudeFeatures

    # Create sketch  
    sketches = rootComp.sketches   
    sketch = sketches.add(rootComp.xYConstructionPlane)
    sketchCircles = sketch.sketchCurves.sketchCircles
    circle = sketchCircles.addByCenterRadius(center, sktDiameter*0.5)

    # Get the profile defined by the circle
    prof = sketch.profiles.item(0)


    # Extrude Sample 1: A simple way of creating typical extrusions (extrusion that goes from the profile plane the specified distance).
    # Define a distance extent of 5 cm
    distance = adsk.core.ValueInput.createByReal(colHeight)
    extrude1 = extrudes.addSimple(prof, distance, adsk.fusion.FeatureOperations.JoinFeatureOperation)    
    # Get the extrusion body
    return extrude1
        

def split_remove(
    app: adsk.core.Application,
    cutter,
    cuttee
):
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    root_comp = design.rootComponent
    features = root_comp.features
        
    # 假设要进行分割的线圈特征和拉伸体是 coil_feature 和 extrude_body
    # cutter = coilFeat_1.bodies.item(0)  # 获取要分割的线圈特征对象
    # cuttee = colFeat_1.bodies.item(0)  # 获取要分割的拉伸体对象
        
    faces = cutter.faces
    # cutting_face = faces.item(5)  # 选择一个外部表面作为切割面


    split_bodies = features.splitBodyFeatures

    split_input = split_bodies.createInput(cuttee, cutter, False)
    split_feature = split_bodies.add(split_input)
        
    split_bodies = split_feature.bodies
    
        
    if split_bodies.count == 2:
        # 获取第一个分割后的体
        split_body_1 = split_bodies.item(0)

        # 获取第二个分割后的体
        split_body_2 = split_bodies.item(1)
            
        # 进行相关操作

    removeFeatures = features.removeFeatures
    body = split_body_1
    # Create remove feature
    removeFeat = removeFeatures.add(body)
        
    # Create an occurrence
    occs = root_comp.occurrences
    occ = occs.addNewComponent(adsk.core.Matrix3D.create())
        
    # Create remove feature
    removeFeat2 = removeFeatures.add(occ)


def create_coil(coilRevolutions, tk, hei, diam, flag):

    app: adsk.core.Application = adsk.core.Application.get()
    des: adsk.fusion.Design = app.activeProduct
    root: adsk.fusion.Component = des.rootComponent
    comp = root
    center = adsk.core.Point3D.create(0, 0, 0)
    coilDiameter = diam - tk

    coilHeight = float(hei/10.0)
    coilTaperAngle_deg = 0.0
    sectionSize = tk

    # coilRevolutions = 10

    sketch: adsk.fusion.Sketch = comp.sketches.add(
        comp.xYConstructionPlane
    )
    sketchCircles: adsk.fusion.SketchCircles = sketch.sketchCurves.sketchCircles

    circle: adsk.fusion.SketchCircle = sketchCircles.addByCenterRadius(
        center,
        coilDiameter * 0.5
    )

    comp: adsk.fusion.Component = circle.parentSketch.parentComponent

    app: adsk.core.Application = adsk.core.Application.get()
    ui: adsk.core.UserInterface = app.userInterface

    sels: adsk.core.Selections = ui.activeSelections
    sels.clear()
    sels.add(circle)

    app.executeTextCommand(u'Commands.Start Coil')
    app.executeTextCommand(u'Commands.SetString infoSizeType infoRevolutionAndHeight')
    app.executeTextCommand(u'Commands.SetDouble CoilHeight {}'.format(coilHeight))
    app.executeTextCommand(u'Commands.SetDouble CoilRevolutions {}'.format(float(coilRevolutions)))
    app.executeTextCommand(u'Commands.SetDouble CoilTaperAngle {}'.format(math.radians(coilTaperAngle_deg)))
    if flag:
        app.executeTextCommand(u'Commands.SetString infoSectionType infoRectanglar')
    else:
        app.executeTextCommand(u'Commands.SetString infoSectionType infoCircular')
    app.executeTextCommand(u'Commands.SetString infoSectionPosition infoOutside')
    app.executeTextCommand(u'Commands.SetDouble SectionSize {}'.format(sectionSize))
    app.executeTextCommand(u'Commands.SetString infoBooleanType infoNewBodyType')
    app.executeTextCommand(u'NuCommands.CommitCmd')


    return comp.features.coilFeatures[-1]

def merge_bodies(body1, body2):
    # 获取活动文档和设计空间
    app = adsk.core.Application.get()
    product = app.activeProduct
    design = adsk.fusion.Design.cast(product)
    
    # 获取根构件
    root_comp = design.rootComponent
    
    # 创建一个布尔运算特征
    boolean_features = root_comp.features.booleanFeatures
    
    # 创建合并操作
    merge_input = boolean_features.createInput(body1, body2)
    merge_input.operation = adsk.fusion.BooleanOperations.UniteBooleanOperation
    
    # 执行合并操作
    boolean_features.add(merge_input)


def get_coils_from_dialog():
    # 创建一个输入框对话框
    app = adsk.core.Application.get()
    # create_coil2(10)
    ui = app.userInterface
    result1 = ui.inputBox("please enter coil revolutions", "revs", "10")
    result2 = ui.inputBox("please enter coil thickness", "Thickness(mm)", "1.5")
    result3 = ui.inputBox("please enter coil height", "Height(mm)", "40.0")
    result4 = ui.inputBox("please enter coil diameter", "Diameter(mm)", "10.0")
    result5 = ui.inputBox("please enter coil type", "rec/1 square/0", "1")
    revolutions = int(result1[0])
    thickness = float(result2[0])/10.0
    height = float(result3[0])
    diam = float(result4[0])/10.0
    recflag = int(result5[0])

    coil = create_coil(revolutions, thickness, height, diam, recflag)
    
    ext = create_col_join(
            app,
            adsk.core.Point3D.create(diam/2, 0, math.floor(height/10.0)),
            thickness,
            1.0
        )
    
    ext2 = create_col_join(
            app,
            adsk.core.Point3D.create(diam/2, 0, 0),
            thickness,
            -1.0
        )
    
        # 选择要合并的两个身体
    
    col = create_col(
            app,
            adsk.core.Point3D.create(0, 0, 0),
            diam,
            height/10.0
        )  
      
    
    oper_1 = split_remove(
            app,
            cutter = coil.bodies.item(0),
            cuttee = col.bodies.item(0)
        )


def run(context):
    ui = None
    app = adsk.core.Application.get()
    try:
        # app: adsk.core.Application = adsk.core.Application.get()
        # ui = app.userInterface
        # design: adsk.fusion.Design = app.activeProduct
        # root: adsk.fusion.Component = design.rootComponent
        get_coils_from_dialog()

        # colFeat_1 = create_col(
        #     app,
        #     adsk.core.Point3D.create(3, 0, 0),
        #     1.0,
        #     4.1
        # )     

    
    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
