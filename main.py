import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cli import TerminalPetsCLI
def main():
    try:
        cli = TerminalPetsCLI()
        cli.start()
    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()