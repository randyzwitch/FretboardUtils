import adsk.core, adsk.fusion, adsk.cam, traceback

# Global variable to hold command definitions
handlers = []

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Create a new command definition without the resource folder argument
        cmdDef = ui.commandDefinitions.addButtonDefinition('createCenterlineCmd', 
                                                           'Create Centerline', 
                                                           'Creates a centerline in the current sketch')
        
        # Access the Sketch panel
        sketchPanel = ui.allToolbarPanels.itemById('SketchCreatePanel')

        # Create a drop-down control if it doesn't exist
        dropDownControl = sketchPanel.controls.itemById('customSketchDropdown')
        if not dropDownControl:
            dropDownControl = sketchPanel.controls.addDropDown('Guitar Fretboard Utilities', 
                                                               'resources',
                                                               'customSketchDropdown', 
                                                               'Utilities for generating fretboards')
        
        # Add the command to the drop-down
        dropDownControl.controls.addCommand(cmdDef)
        
        # Connect the command created event
        onCommandCreated = CenterlineCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CenterlineCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            eventArgs = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = eventArgs.command
            
            onExecute = CenterlineCommandExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
            
        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

class CenterlineCommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            design = app.activeProduct
            rootComp = design.rootComponent
            sketches = rootComp.sketches
            sketch = sketches.item(0)  # Assumes the first sketch is active

            # Create a centerline
            lines = sketch.sketchCurves.sketchLines
            centerLine = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(1, 0, 0))
            centerLine.isConstruction = True

        except:
            app = adsk.core.Application.get()
            ui = app.userInterface
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Remove the command from the drop-down
        sketchPanel = ui.allToolbarPanels.itemById('SketchCreatePanel')
        dropDownControl = sketchPanel.controls.itemById('customSketchDropdown')
        if dropDownControl:
            cmdControl = dropDownControl.controls.itemById('createCenterlineCmd')
            if cmdControl:
                cmdControl.deleteMe()

        # Remove the drop-down if empty
        if dropDownControl and dropDownControl.controls.count == 0:
            dropDownControl.deleteMe()

        # Remove the command definition
        cmdDef = ui.commandDefinitions.itemById('createCenterlineCmd')
        if cmdDef:
            cmdDef.deleteMe()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))