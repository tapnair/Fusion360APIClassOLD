# Author-Patrick
# Description-Basic demo of creating a block
from .BlockCommand import BlockCommand

commands = []
command_definitions = []

# Define parameters for 1st command
cmd = {
    'cmd_name': 'Create a block',
    'cmd_description': 'Create a block',
    'cmd_id': 'cmdID_BlockCommand',
    'cmd_resources': './resources',
    'workspace': 'FusionSolidEnvironment',
    'toolbar_panel_id': 'AU 2018',
    'command_promoted': True,
    'class': BlockCommand
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
