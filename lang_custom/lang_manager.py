import os
import json
import random

class LangManager:
    def __init__(self):
        self.lang_dir = self.find_or_create_lang_dir()
        self.default_lang = "en"
        self.selected_group = None
        self.cache_enabled = True
        self.lang_cache = {}
        self.current_lang = None

    def find_or_create_lang_dir(self):
        project_root = os.getcwd()
        lang_path = os.path.join(project_root, "Lang_data")

        if not os.path.exists(lang_path):
            os.makedirs(lang_path)
            self.create_default_lang_file(lang_path)

        return lang_path

    def create_default_lang_file(self, lang_path):
        default_data = {
            "bot_reply": {
                "text1": "hello :D",
                "text2": "hi :3"
            },
            "bot_random": {
                "instruct": "use square brackets to random",
                "text_random": ["text1", "text2","text.."]
            }
        }
        en_path = os.path.join(lang_path, "en.json")
        with open(en_path, "w", encoding="utf-8") as f:
            json.dump(default_data, f, indent=4, ensure_ascii=False)

    def load_lang(self, lang):
        if self.cache_enabled and lang in self.lang_cache:
            return self.lang_cache[lang]

        lang_path = os.path.join(self.lang_dir, f"{lang}.json")
        if not os.path.exists(lang_path):
            raise FileNotFoundError(f"Language file '{lang}.json' not found in '{self.lang_dir}'.")

        try:
            with open(lang_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if self.cache_enabled:
                    self.lang_cache[lang] = data
                return data
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{lang_path}'.")

    def lang(self, lang):
        self.current_lang = lang
        return self

    def group(self, group_name, cache=True):
        self.selected_group = group_name
        self.cache_enabled = cache
        return self

    def get_text(self, key, default=None):
        if not self.selected_group:
            raise ValueError("No language group selected. Use 'group(group_name)' first.")
        if not self.current_lang:
            raise ValueError("No language selected. Use 'lang(lang)' first.")

        data = self.load_lang(self.current_lang)
        group_data = data.get(self.selected_group, {})

        return group_data.get(key, default)
    
    def random_text(self, key, default=None):
        if not self.selected_group:
            raise ValueError("No language group selected. Use 'group(group_name)' first.")
        if not self.current_lang:
            raise ValueError("No language selected. Use 'lang(lang)' first.")

        data = self.load_lang(self.current_lang)
        group_data = data.get(self.selected_group, {})
        value = group_data.get(key, default)
        
        if isinstance(value, list):
            return random.choice(value) if value else default
        return value

    def get(self):
        files = os.listdir(self.lang_dir)
        langs = [f[:-5] for f in files if f.endswith(".json")]
        return ",".join(langs)

    def reload(self):
        self.lang_cache.clear()

lang_manager = LangManager()

def lang(lang):
    return lang_manager.lang(lang)

def get():
    return lang_manager.get()

def reload():
    lang_manager.reload()
