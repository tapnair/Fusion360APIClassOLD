import adsk.core
import adsk.fusion
import traceback

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


# Create Block based on user input
def make_block(length, width, height):

    ao = AppObjects()

    # Get reference to the sketchs and plane
    sketches = ao.root_comp.sketches
    xy_plane = ao.root_comp.xYConstructionPlane

    # Create a new sketch and get lines reference
    sketch = sketches.add(xy_plane)
    lines = sketch.sketchCurves.sketchLines

    # Use Autodesk methods to create input geometry
    point0 = adsk.core.Point3D.create(0, 0, 0)
    point1 = adsk.core.Point3D.create(length, 0, 0)
    point2 = adsk.core.Point3D.create(length, width, 0)
    point3 = adsk.core.Point3D.create(0, width, 0)

    # Create lines
    lines.addByTwoPoints(point0, point1)
    lines.addByTwoPoints(point1, point2)
    lines.addByTwoPoints(point2, point3)
    lines.addByTwoPoints(point3, point0)

    # Get the profile defined by the circle
    profile = sketch.profiles.item(0)

    # Create an extrusion input
    extrudes = ao.root_comp.features.extrudeFeatures
    ext_input = extrudes.createInput(profile, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)

    # Define that the extent is a distance extent of height
    distance = adsk.core.ValueInput.createByReal(height)

    # Set the distance extent to be single direction
    ext_input.setDistanceExtent(False, distance)

    # Set the extrude to be a solid one
    ext_input.isSolid = True

    # Create the extrusion
    extrudes.add(ext_input)


# Class for Fusion 360 Block Command
class BlockCommand(Fusion360CommandBase):

    # Run when the user presses OK
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):

        # Get the values from the user input
        length = input_values['length_input']
        width = input_values['width_input']
        height = input_values['height_input']

        # Run the block function
        make_block(length, width, height)

    # Run when the user selects your command icon from the Fusion 360 UI
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Create a default value using a string
        default_length = adsk.core.ValueInput.createByString('6.0 in')
        default_width = adsk.core.ValueInput.createByString('4.0 in')
        default_height = adsk.core.ValueInput.createByString('.5 in')

        ao = AppObjects()

        inputs.addValueInput('length_input', 'Length', ao.units_manager.defaultLengthUnits, default_length)
        inputs.addValueInput('width_input', 'Width', ao.units_manager.defaultLengthUnits, default_width)
        inputs.addValueInput('height_input', 'Height', ao.units_manager.defaultLengthUnits, default_height)
