# Lang Custom

Lang Custom is a simple Python library for managing and loading translations from JSON files.

## Installation

You can install this library using pip:
```sh
pip install lang_custom
```

## Usage Guide

### 1. Import the library
```python
import lang_custom
```

### 2. Get available languages
To list all available languages in the `Lang_data` directory, use:
```python
languages = lang_custom.get()
print(languages)  # Example: ['en', 'vi']
```

### 3. Select a data group
Before retrieving text, you need to select a data group from the JSON file:
```python
lang_custom.set_group("name")
```
Where `name` is the group you want to access in the JSON file.

### 4. Retrieve text data
After selecting a group, retrieve text using:
```python
text = lang_custom.get_text("en", "text")
print(text)  # Displays the corresponding value for key "text" in group "name" from en.json
```
Where:
- `"en"` is the language code.
- `"text"` is the key to retrieve within the selected group.

## Language File Structure
Each language is stored in the `Lang_data` directory as a JSON file. Example of `en.json`:
```json
{
    "name": {
        "text": "hello friend :D",
        "example": "text2"
    },
    "name2": {
        "example": "text",
        "example2": "text2"
    }
}
```

## Feedback & Issues
For any feedback or issues, please contact me:
[Discord me](https://discord.gg/pGcSyr2bcY)

