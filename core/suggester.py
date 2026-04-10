from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from .storage import load_history

class LuminaSuggester(AutoSuggest):
    def get_suggestion(self, buffer, document):
        text = document.text
        if not text:
            return None
        
        history = load_history()
        
        # Look for the first match in history that starts with current input
        for command in history:
            if command.startswith(text) and command != text:
                return Suggestion(command[len(text):])
        
        return None