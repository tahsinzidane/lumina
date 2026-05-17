from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion
from prompt_toolkit.completion import Completer, Completion
from .storage import load_history, load_dir_cache, save_dir_cache
import os

class LuminaSuggester(AutoSuggest):
    def get_suggestion(self, buffer, document):
        text = document.text
        if not text:
            return None

        # Handle cd suggestions
        if text.startswith('cd '):
            prefix = text[3:].strip()
            return self._get_cd_suggestion(prefix)

        history = load_history()

        # Look for the first match in history that starts with current input
        for command in history:
            if command.startswith(text) and command != text:
                return Suggestion(command[len(text):])

        return None

    def _get_cd_suggestion(self, prefix):
        cache = load_dir_cache()
        directories = cache.get("directories", [])
        frequency = cache.get("frequency", {})

        matches = []
        for d in directories:
            if not os.path.exists(d):
                continue

            basename = os.path.basename(d)
            if basename.startswith(prefix):
                matches.append(d)

        if not matches:
            return None

        # Sort by frequency
        matches.sort(key=lambda x: frequency.get(x, 0), reverse=True)

        best_match = matches[0]
        if os.path.dirname(best_match) == os.getcwd():
            suggestion_text = os.path.basename(best_match)
        else:
            suggestion_text = best_match.replace(os.path.expanduser("~"), "~")

        if suggestion_text.startswith(prefix):
            return Suggestion(suggestion_text[len(prefix):])

        return None

    def _fuzzy_match(self, pattern, target):
        pattern = pattern.lower()
        target = target.lower()
        if not pattern:
            return True
        it = iter(target)
        return all(c in it for c in pattern)

class LuminaCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text
        if not text.startswith('cd '):
            return

        prefix = text[3:].strip()
        cache = load_dir_cache()
        directories = cache.get("directories", [])
        frequency = cache.get("frequency", {})

        matches = []
        for d in directories:
            if not os.path.exists(d):
                continue

            basename = os.path.basename(d)
            if basename.startswith(prefix) or self._fuzzy_match(prefix, basename):
                matches.append(d)

        # Sort by frequency
        matches.sort(key=lambda x: frequency.get(x, 0), reverse=True)

        # Show top 3 in popup if more than 1 match
        for m in matches[:3]:
            if os.path.dirname(m) == os.getcwd():
                display_name = os.path.basename(m)
            else:
                display_name = m.replace(os.path.expanduser("~"), "~")

            yield Completion(display_name, start_position=-len(prefix))

    def _fuzzy_match(self, pattern, target):
        pattern = pattern.lower()
        target = target.lower()
        if not pattern:
            return True
        it = iter(target)
        return all(c in it for c in pattern)