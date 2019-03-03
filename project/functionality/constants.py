from pathlib import Path

class Constants:
    """
    This class is intended to house constant values used throughout the
    program.
    """

    # The path to the resources directory of the project.
    resources_path = Path(__file__).parents[1]/'resources'

    # The name of the program.
    program_name = '[Placeholder Name] Editor'

    # These values are used to determine whether a key press should count as
    # text input or not in EditorWindow.on_key_press. They're used to check
    # whether Ctrl or Alt were held during the key press.
    forbidden_flags = (
        0x04,  # Ctrl
        0x20000  # Alt
    )

    # The path to the picture of Cloppy used in CloppyWindow
    cloppy_picture_path = str(resources_path/'cloppy.png')

    # The path to the audio of Cloppy used in CloppyWindow
    cloppy_sound_path = str(resources_path/'321947__n-audioman__horseneigh02-03.wav')

    # Cloppy's greeting to the user shown in CloppyWindow
    cloppy_greeting = (
        f"Hi, I'm Cloppy, your {program_name} personal assistant!"
    )
