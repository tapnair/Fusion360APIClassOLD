import adsk.core
import adsk.fusion
import traceback

import os
from os.path import expanduser
import csv

from .Fusion360Utilities.Fusion360Utilities import AppObjects
from .Fusion360Utilities.Fusion360CommandBase import Fusion360CommandBase


# Function to convert a csv file to a list of dictionaries.
# Takes in one variable called "csv_file_name"
def csv_dict_list(csv_file_name):

    # Open variable-based csv,
    # Iterate over the rows and map values to a list of dictionaries
    reader = csv.DictReader(open(csv_file_name, 'r'))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


# Create Block
def make_block(length, width, height):

    ao = AppObjects()

    # Get reference to the sketchs and plane
    sketches = ao.root_comp.sketches
    xy_plane = ao.root_comp.xYConstructionPlane

    # Create a new sketch and get lines reference
    sketch = sketches.add(xy_plane)
    lines = sketch.sketchCurves.sketchLines

    # Use autodesk methods to create input geometry
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


def make_holes(hole_list):

    ao = AppObjects()

    profile_collection = adsk.core.ObjectCollection.create()

    # Get reference to the sketches and plane
    sketches = ao.root_comp.sketches
    xy_plane = ao.root_comp.xYConstructionPlane

    # Create a new sketch and get lines reference
    sketch = sketches.add(xy_plane)
    circles = sketch.sketchCurves.sketchCircles

    input_units = 'in'

    for hole in hole_list:
        x = ao.units_manager.evaluateExpression(hole['x'], input_units)
        y = ao.units_manager.evaluateExpression(hole['y'], input_units)
        radius = ao.units_manager.evaluateExpression(hole['radius'], input_units)
        # x = float(hole['x'])
        # y = float(hole['y'])
        # radius = float(hole['radius'])

        center_point = adsk.core.Point3D.create(x, y, 0)
        circles.addByCenterRadius(center_point, radius)

    for profile in sketch.profiles:
        profile_collection.add(profile)

    # Create an extrusion input
    extrudes = ao.root_comp.features.extrudeFeatures
    ext_input = extrudes.createInput(profile_collection, adsk.fusion.FeatureOperations.CutFeatureOperation)

    # Set the distance extent to be single direction
    extent_all = adsk.fusion.ThroughAllExtentDefinition.create()
    ext_input.setOneSideExtent(extent_all, adsk.fusion.ExtentDirections.PositiveExtentDirection)

    # Create the extrusion
    extrudes.add(ext_input)


# Simple add-in to create a plate with holes
class HolesCommand(Fusion360CommandBase):

    # Run when the user presses OK
    def on_execute(self, command: adsk.core.Command,
                   inputs: adsk.core.CommandInputs,
                   args, input_values):

        # Get the values from the user input
        length = input_values['length_input']
        width = input_values['width_input']
        height = input_values['height_input']
        the_file_name = input_values['the_file_name']

        # Read in the csv hole and return a list of 1 dictionary per hole
        hole_list = csv_dict_list(the_file_name)

        # Create a block based on user input
        make_block(length, width, height)

        # Create holes based on the imported csv
        make_holes(hole_list)

    # Run when the user selects your command icon from the Fusion 360 UI
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Create a default value using a string
        default_length = adsk.core.ValueInput.createByString('6.0 in')
        default_width = adsk.core.ValueInput.createByString('4.0 in')
        default_height = adsk.core.ValueInput.createByString('.5 in')

        csv_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'holes_csv.csv')

        ao = AppObjects()

        inputs.addValueInput('length_input', 'Length', ao.units_manager.defaultLengthUnits, default_length)
        inputs.addValueInput('width_input', 'Width', ao.units_manager.defaultLengthUnits, default_width)
        inputs.addValueInput('height_input', 'Height', ao.units_manager.defaultLengthUnits, default_height)
        inputs.addStringValueInput('the_file_name', 'Input File: ', csv_file)
