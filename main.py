import subprocess
import sys
import os
import shutil
import random
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from core.suggester import LuminaSuggester
from core.storage import save_command

# Aesthetic styling for the terminal
lumina_style = Style.from_dict({
    'auto-suggestion': '#666666 italic', 
    'prompt': '#00ff00 bold',            
    'path': '#00afff',                   
})

# roasts for failed commands
ROASTS = [
    "L + Ratio + ssssskill issue",
    "Aura depleted. Command not found.",
    "Bros trying to run a ghost command 💀",
    "Invalid input. Go touch grass.",
    "Check your spelling, no cap.",
    "Negative Aura detected. Fix your command."
]

def main():
    session = PromptSession(
        auto_suggest=LuminaSuggester(),
        style=lumina_style
    )
    
    print("Lumina Shell Wrapper Initialized. Type 'exit' to quit.")
    
    while True:
        try:
            # Dynamic Prompt Path
            current_dir = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt_tokens = [
                ('class:path', f'[{current_dir}] '),
                ('class:prompt', 'lumina ❯ '),
            ]
            
            # Get Input
            user_input = session.prompt(prompt_tokens)
            
            if not user_input.strip():
                continue

            if user_input.lower() in ['exit', 'quit']:
                break

            # Persistence & Parsing
            save_command(user_input)
            parts = user_input.split()
            command = parts[0]

            # Built-in Overrides
            if command == "cd":
                try:
                    path = parts[1] if len(parts) > 1 else os.path.expanduser("~")
                    os.chdir(path)
                except Exception as e:
                    print(f"cd: {e}")
                continue

            if command == "clear":
                print("\033[H\033[J", end="")
                continue

            # Execution & Skill Issue Check
            try:
                # Check if the command exists before running
                if shutil.which(command) is None:
                    print(f"❌ {random.choice(ROASTS)}: '{command}'")
                else:
                    # Run the actual system command
                    subprocess.run(user_input, shell=True)
            except Exception as e:
                print(f"Execution Error: {e}")
                
        except KeyboardInterrupt:
            print("") 
            continue 
        except EOFError:
            break    

if __name__ == "__main__":
    main()