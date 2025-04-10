import sys

if __name__ == "__main__":
    from service.core.cli import execute_from_command_line

    execute_from_command_line(sys.argv[:])
