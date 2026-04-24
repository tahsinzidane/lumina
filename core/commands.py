import sys

def handle_args():
    # Simple dictionary for version and author info
    INFO = {
        "version": "Lumina Shell v0.2.1",
        "author": "Tahsin Zidane (@tahsinzidane)",
        "help": """
Lumina - Aesthetic Shell Wrapper

Usage:
  lumina [options]

Options:
  -v, --version    Show version info
  -h, --help       Show this help message
  -a, --author     Show developer info
        """
    }

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ['-v', '--version']:
            print(INFO["version"])
            sys.exit(0)
        elif arg in ['-h', '--help']:
            print(INFO["help"])
            sys.exit(0)
        elif arg in ['-a', '--author']:
            print(f"Developed by: {INFO['author']}")
            sys.exit(0)