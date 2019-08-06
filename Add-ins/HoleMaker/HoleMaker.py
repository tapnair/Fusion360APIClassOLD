#Author-Patrick
#Description-Basic demo of reading a CSV file and creating geometry.

# Importing sample Fusion Command
# Could import multiple Command definitions here
from .HolesCommand import HolesCommand

commands = []
command_definitions = []

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Holes in a Plate',
    'cmd_description': 'Fusion Demo Command 1 Description',
    'cmd_id': 'cmdID_HolesCommand',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'AU 2018',
    'command_promoted': True,
    'class': HolesCommand
}
command_definitions.append(cmd)


# Set to True to display various useful messages when debugging your app
debug = False

# Don't change anything below here:
for cmd_def in command_definitions:
    command = cmd_def['class'](cmd_def, debug)
    commands.append(command)


def run(context):
    for run_command in commands:
        run_command.on_run()


def stop(context):
    for stop_command in commands:
        stop_command.on_stop()
