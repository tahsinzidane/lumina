import subprocess
import sys
import os
import shutil
import random
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.key_binding import KeyBindings
from core.suggester import LuminaSuggester, LuminaCompleter
from core.storage import save_command, update_dir_cache, maintain_cache
from core.commands import handle_args

# Aesthetic styling for the terminal
lumina_style = Style.from_dict({
    'auto-suggestion': '#666666 italic', 
    'prompt': '#00ff00 bold',            
    'path': '#00afff',                   
})

# Key bindings to handle "Enter" accepting suggestion
kb = KeyBindings()

@kb.add('enter')
def _(event):
    buffer = event.current_buffer
    suggestion = buffer.suggestion
    if suggestion:
        buffer.insert_text(suggestion.text)
    buffer.validate_and_handle()

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
    handle_args()
    maintain_cache() # Run maintenance on startup
    
    session = PromptSession(
        auto_suggest=LuminaSuggester(),
        completer=LuminaCompleter(),
        key_bindings=kb,
        style=lumina_style
    )
    
    print("-" * 50)
    print("🌌 LUMINA SHELL WRAPPER INITIALIZED")
    print("   > 'quit' : Return to host shell")
    print("   > 'exit' : Close terminal window")
    print("-" * 50)

    while True:
        try:
            # Dynamic Prompt Path
            current_dir = os.getcwd().replace(os.path.expanduser("~"), "~")
            prompt_tokens = [
                ('class:path', f'[{current_dir}] '),
                ('class:prompt', 'lumina ❯ '),
            ]
            
            # Get Input
            user_input = session.prompt(prompt_tokens).strip()
            
            if not user_input:
                continue

            # --- logic update for closing terminal window ---
            if user_input.lower() == 'exit':
                print("Closing terminal session...")
                os.kill(os.getppid(), 9) 
                sys.exit(0)

            if user_input.lower() == 'quit':
                print("Exiting Lumina Shell...")
                break

            # Persistence & Parsing
            save_command(user_input)
            parts = user_input.split()
            command = parts[0]

            # Built-in Overrides
            if command == "cd":
                try:
                    path = parts[1] if len(parts) > 1 else os.path.expanduser("~")
                    abs_path = os.path.abspath(os.path.expanduser(path))
                    os.chdir(path)
                    # Update cache frequency if it's a directory
                    if os.path.isdir(abs_path):
                        update_dir_cache([abs_path])
                except Exception as e:
                    print(f"cd: {e}")
                continue

            if command == "clear":
                print("\033[H\033[J", end="")
                continue

            # Execution & Skill Issue Check
            try:
                if shutil.which(command) is None:
                    print(f"❌ {random.choice(ROASTS)}: '{command}'")
                else:
                    if command in ['ls', 'dir']:
                        # Run and capture for ls/dir to get directories
                        result = subprocess.run(user_input, shell=True, capture_output=True, text=True)
                        print(result.stdout, end="")
                        print(result.stderr, end="", file=sys.stderr)
                        
                        # Extract directories from output or just scan the target directory
                        # To be safe and fulfill "from the output", we can try to parse it
                        # But it's more reliable to scan the directory targeted by ls
                        target_dir = "."
                        for part in parts[1:]:
                            if not part.startswith("-"):
                                target_dir = part
                                break
                        
                        try:
                            abs_target = os.path.abspath(os.path.expanduser(target_dir))
                            if os.path.isdir(abs_target):
                                found_dirs = [os.path.join(abs_target, d) for d in os.listdir(abs_target) if os.path.isdir(os.path.join(abs_target, d))]
                                update_dir_cache(found_dirs)
                        except:
                            pass
                    else:
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