import argparse
import asyncio
import functools
import inspect
import os
import pkgutil
import subprocess  # nosec B404
import sys
from argparse import (  # noqa: F401
    _AppendConstAction,
    _CountAction,
    _StoreConstAction,
    _SubParsersAction,
)
from importlib import import_module
from io import TextIOBase
from typing import List, TextIO

from colored import Back, Fore, Style

from service.core.settings import settings


def find_commands(app_dir):
    """
    Collect all project commands in the project
    """

    command_dir = os.path.join(app_dir, "commands")
    return [
        name
        for _, name, is_pkg in pkgutil.iter_modules([command_dir])
        if not is_pkg and not name.startswith("_")
    ]


def load_command_class(app_name, name):
    """
    Load the command class
    """

    command_module = import_module(f"{app_name}.commands.{name}")

    if not hasattr(command_module, "Command"):
        raise AttributeError(f"Command class '{name}' not found in {app_name}")
    return command_module.Command()


@functools.cache
def get_commands():
    """
    Get the list of commands from the app list
    """

    commands = {}
    for app in tuple(settings.app_list):
        path = app.replace(".", "/")
        commands.update({name: app for name in find_commands(path)})
    return commands


class CommandError(Exception):
    """
    Command error class
    """

    def __init__(self, *args, returncode=1, **kwargs):
        self.returncode = returncode
        super().__init__(*args, **kwargs)


class SystemCheckError(CommandError):
    """
    System check error class
    """

    pass


def handle_default_options(options):
    """
    Handle the default options
    """

    if options.settings:
        os.environ["API_SETTINGS_MODULE"] = options.settings


class Colors:
    """
    Colors class for colored
    """

    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BLACK = Fore.BLACK


class Styles:
    """
    Styles class for colored
    """

    BOLD = Style.bold
    ITALIC = Style.italic
    DIM = Style.dim
    RESET = Style.reset


class StdoutWrapper:
    """
    Style class for colored

    This class is responsible for styling the text

    Heavily inspired by Django's OutputWrapper class
    see: https://github.com/django/django/blob/main/django/core/management/base.py#L145
    """

    fore = Fore
    back = Back

    @staticmethod
    def style(
        text,
        color: str = Colors.WHITE,
        style: str = None,
    ):
        """
        Style the text with the given style
        """

        if color not in Colors.__dict__.values():
            raise ValueError(f"Invalid color: {color}")

        if style and style not in Styles.__dict__.values():
            raise ValueError(f"Invalid style: {style}")

        if style:
            text = f"{color}{style}{text}{Style.RESET}"
        else:
            text = f"{color}{text}{Style.RESET}"
        return text

    def __init__(self, out, ending="\n"):
        self._out = out
        self.style_func = None
        self.ending = ending

    def __getattr__(self, name):
        return getattr(self._out, name)

    def flush(self):
        """
        Flush the output stream to the console
        """
        if hasattr(self._out, "flush"):
            self._out.flush()

    def isatty(self):
        """
        Check if the output is a tty terminal
        """
        return hasattr(self._out, "isatty") and self._out.isatty()

    def write(self, msg="", ending=None):
        """
        Write the text with the given style to the console
        """

        ending = self.ending if ending is None else ending
        if ending and not msg.endswith(ending):
            msg += ending
        self._out.write(msg)


TextIOBase.register(StdoutWrapper)


class CommandManager:
    """
    Command manager class

    This class is responsible for managing the commands
    """

    def __init__(self, argv):
        self.commands = get_commands()
        self.argv = argv

    def execute(self, command, raise_exception=False):
        """
        Execute the command with the given arguments and return the result
        """

        if not self.valid_command(command):
            if raise_exception:
                raise CommandError(f"Command '{command}' not found in application")
            sys.stderr.write("Invalid command: %s\n" % command)
            self.print_commands()
            return

        app = self.commands[command]
        command = load_command_class(app, command)
        return command.run_from_argv(self.argv)

    def valid_command(self, command):
        """
        Check if the command is valid
        """
        return command in self.commands

    def print_commands(self):
        """
        Print the list of commands
        """

        sys.stdout.write("Available commands:\n")
        app_commands = {}
        for command, app in self.commands.items():
            if app not in app_commands:
                app_commands[app] = []
            app_commands[app].append(command)

        for app, commands in app_commands.items():
            sys.stdout.write(f"{app}:\n")
            for command in commands:
                sys.stdout.write(f"  {command}\n")


class BaseCommand:
    """
    Base command class for all commands

    ``require_migration``
        A boolean indicating whether the command requires the app to be
        migrated before running.

    ``requires_migrations_checks``
        A boolean indicating whether the command requires the app to be
        migrated before running.

    ``stealth_options``
        A tuple of any options the command uses which aren't defined by the
        argument parser.
    """

    requires_migrations_checks = False
    require_migration = False
    base_stealth_options = ("stderr", "stdout")
    stealth_options = ()
    suppressed_base_arguments = set()

    def __init__(self, stdout=None, stderr=None):
        self.styles = Styles()
        self.colors = Colors()
        self.stdout = StdoutWrapper(stdout or sys.stdout)
        self.stderr = StdoutWrapper(stderr or sys.stderr)

    def add_base_argument(self, parser, *args, **kwargs):
        """
        Call the parser's add_argument() method, suppressing the help text
        according to BaseCommand.suppressed_base_arguments.
        """
        for arg in args:
            if arg in self.suppressed_base_arguments:
                kwargs["help"] = argparse.SUPPRESS
                break
        parser.add_argument(*args, **kwargs)

    def add_arguments(self, parser):
        """
        Add arguments to the parser
        """

        pass

    def handle(self, *args, **options):
        """
        Handle the command
        """

        raise NotImplementedError("Subclasses must implement the handle method")

    def create_parser(self, prog_name, subcommand):
        """
        Create the parser
        """

        parser = argparse.ArgumentParser(
            prog="%s %s" % (os.path.basename(prog_name), subcommand),
            description=self.__doc__,
        )
        self.add_base_argument(
            parser,
            "--traceback",
            action="store_true",
            help="Display a full stack trace on CommandError exceptions.",
        )
        self.add_base_argument(
            parser,
            "--settings",
            help=(
                "The Python path to a settings module, e.g. "
                '"myproject.settings.main". If this isn\'t provided, the '
                "API_SETTINGS_MODULE environment variable will be used."
            ),
        )
        self.add_arguments(parser)
        return parser

    def run_from_argv(self, argv):
        """
        Run the command from the command line arguments
        """

        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop("args", ())
        handle_default_options(options)
        try:
            self.execute(*args, **cmd_options)
        except CommandError as e:
            if options.traceback:
                raise

                # SystemCheckError takes care of its own formatting.
            if isinstance(e, SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(e.returncode)

    def execute(self, *args, **options):
        """
        Execute the command with the given arguments
        """

        if options.get("stdout"):
            self.stdout = StdoutWrapper(options["stdout"])
        if options.get("stderr"):
            self.stderr = StdoutWrapper(options["stderr"])

        if self.requires_migrations_checks:  # Check if a new migration is needed
            if self.migration_required():
                self.stdout.write("New migrations are needed")
                self.stdout.write(
                    "Run 'python main.py createmigrations', "
                    "run the migrations and try again"
                )

        if inspect.iscoroutinefunction(self.handle):
            output = asyncio.run(self.handle(*args, **options))
        else:
            output = self.handle(*args, **options)
        if output:
            self.stdout.write(output)
        return output

    @staticmethod
    def shell_exec(command: List[str], **options):
        """
        Execute a shell command
        """

        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=True
            )  # nosec B603
            return result
        except subprocess.CalledProcessError as error:
            print(error)
            return error

    def migration_required(self):
        """
        Check if a new migration is required
        """

        result = self.shell_exec(
            ["alembic", "check"],
        )

        return (
            "(current)" not in result.stdout
            or "No new upgrade operations detected." not in result.stdout
        )


def call_command(command_name: str, *args, **options):
    """
    Call the command with the given arguments

    heavily inspired by Django's call_command function from django.core.management
    see: https://github.com/django/django/blob/main/django/core/management/__init__.py#L83
    """

    if isinstance(command_name, BaseCommand):
        # Command object passed in.
        command = command_name
        command_name = command.__class__.__module__.split(".")[-1]
    else:
        # Load the command object by name.
        try:
            app_name = get_commands()[command_name]
        except KeyError:
            raise CommandError("Unknown command: %r" % command_name)

        if isinstance(app_name, BaseCommand):
            # If the command is already loaded, use it directly.
            command = app_name
        else:
            command = load_command_class(app_name, command_name)

    # Simulate argument parsing to get the option defaults
    parser = command.create_parser("", command_name)
    # Use the `dest` option name from the parser option
    opt_mapping = {
        min(s_opt.option_strings).lstrip("-").replace("-", "_"): s_opt.dest
        for s_opt in parser._actions
        if s_opt.option_strings
    }
    arg_options = {opt_mapping.get(key, key): value for key, value in options.items()}
    parse_args = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            parse_args += map(str, arg)
        else:
            parse_args.append(str(arg))

    def get_actions(parser):
        # Parser actions and actions from sub-parser choices.
        for opt in parser._actions:
            if isinstance(opt, _SubParsersAction):
                for sub_opt in opt.choices.values():
                    yield from get_actions(sub_opt)
            else:
                yield opt

    parser_actions = list(get_actions(parser))
    mutually_exclusive_required_options = {
        opt
        for group in parser._mutually_exclusive_groups
        for opt in group._group_actions
        if group.required
    }
    # Any required arguments which are passed in via **options must be passed
    # to parse_args().
    for opt in parser_actions:
        if opt.dest in options and (
            opt.required or opt in mutually_exclusive_required_options
        ):
            opt_dest_count = sum(v == opt.dest for v in opt_mapping.values())
            if opt_dest_count > 1:
                raise TypeError(
                    f"Cannot pass the dest {opt.dest!r} that matches multiple "
                    f"arguments via **options."
                )
            parse_args.append(min(opt.option_strings))
            if isinstance(opt, (_AppendConstAction, _CountAction, _StoreConstAction)):
                continue
            value = arg_options[opt.dest]
            if isinstance(value, (list, tuple)):
                parse_args += map(str, value)
            else:
                parse_args.append(str(value))
    defaults = parser.parse_args(args=parse_args)
    defaults = dict(defaults._get_kwargs(), **arg_options)
    # Raise an error if any unknown options were passed.
    stealth_options = set(command.base_stealth_options + command.stealth_options)
    dest_parameters = {action.dest for action in parser_actions}
    valid_options = (dest_parameters | stealth_options).union(opt_mapping)
    unknown_options = set(options) - valid_options
    if unknown_options:
        raise TypeError(
            "Unknown option(s) for %s command: %s. "
            "Valid options are: %s."
            % (
                command_name,
                ", ".join(sorted(unknown_options)),
                ", ".join(sorted(valid_options)),
            )
        )
    # Move positional args out of options to mimic legacy optparse
    args = defaults.pop("args", ())
    if "skip_checks" not in options:
        defaults["skip_checks"] = True

    return command.execute(*args, **defaults)


def execute_from_command_line(argv):
    """
    Execute the command line
    """

    command_manager = CommandManager(argv)
    try:
        command_manager.execute(argv[1])
    except IndexError:
        command_manager.print_commands()
