import json
import os

# Utility function to load texts from JSON file based on language

def load_texts(language):
    base_path = os.path.dirname(__file__)
    i18n_path = os.path.join(base_path, '..', 'i18n')
    file_map = {
        'en': 'texts_en.json',
        'maori': 'texts_maori.json'
    }
    file_name = file_map.get(language, 'texts_en.json')
    file_path = os.path.join(i18n_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Example usage:
# texts = load_texts('en')
# user_txts = texts['UserTexts']
# print(user_txts['txt_admin_option'])
