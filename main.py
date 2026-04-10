import subprocess
import sys
import os
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from core.suggester import LuminaSuggester
from core.storage import save_command

# Aesthetic styling for the terminal
lumina_style = Style.from_dict({
    'auto-suggestion': '#666666 italic', # Ghost text color
    'prompt': '#00ff00 bold',            # Green prompt
    'path': '#00afff',                   # Cyan for directory path
})

def main():
    session = PromptSession(
        auto_suggest=LuminaSuggester(),
        style=lumina_style
    )
    
    print("Lumina Shell Wrapper Initialized. Type 'exit' to quit.")
    
    while True:
        try:
            # Get current directory and shorten Home path to '~'
            current_dir = os.getcwd().replace(os.path.expanduser("~"), "~")
            
            # Create a dynamic prompt: [path] lumina ❯ 
            # We use a list of style tuples for prompt_toolkit
            prompt_tokens = [
                ('class:path', f'[{current_dir}] '),
                ('class:prompt', 'lumina ❯ '),
            ]
            
            # 1. Capture User Input
            user_input = session.prompt(prompt_tokens)
            
            # Handle empty input
            if not user_input.strip():
                continue

            # Internal commands to quit
            if user_input.lower() in ['exit', 'quit']:
                break

            # 2. Save command to history (JSON)
            save_command(user_input)
            
            # 3. Handle Built-in Commands (manual override)
            parts = user_input.split()
            command = parts[0]

            if command == "cd":
                try:
                    # Move to path or home if no args
                    path = parts[1] if len(parts) > 1 else os.path.expanduser("~")
                    os.chdir(path)
                except Exception as e:
                    print(f"cd: {e}")
                continue # Skip subprocess, we handled it manually

            if command == "clear":
                # Clear terminal screen properly
                print("\033[H\033[J", end="")
                continue

            # 4. Execute all other system commands via Subprocess
            try:
                subprocess.run(user_input, shell=True)
            except Exception as e:
                print(f"Execution Error: {e}")
                
        except KeyboardInterrupt:
            print("") # New line on Ctrl+C
            continue 
        except EOFError:
            break    # Handle Ctrl+D

if __name__ == "__main__":
    main()