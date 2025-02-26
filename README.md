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

### 2. Get available language files
The library will automatically detect all JSON language files stored in the `Lang_data` directory inside your source code. To list all available language files, use:
```python
languages = lang_custom.get()
print(languages)  # Example: ['en.json', 'vi.json']
```
Where each item represents a JSON file found in the language directories.

### 3. Select a data group
Before retrieving text, you need to select a data group from the JSON file:
```python
lang_custom.set_group("name")
```
Where `name` is the group you want to access in the JSON structure.

### 4. Retrieve text data
After selecting a group, retrieve text using:
```python
text = lang_custom.get_text("en", "text")
print(text)  # Displays the corresponding value for key "text" in group "name" from en.json
```
Where:
- `"en.json"` is the file name of the language you want to use.
- `"text"` is the key to retrieve within the selected group.

## Language File Structure
Each language file is stored in either the `Lang_Custom` directory (default translations) or `Lang_data` (user-added translations). Example of `Lang_Custom/en.json`:
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
Users can add their own JSON language files in the `Lang_data` directory, as long as they follow the correct structure.

## Feedback & Issues
For any feedback or issues, please contact me:
[Discord me](https://discord.gg/pGcSyr2bcY)

Thank you for using Lang_custom

![Thank You](https://github.com/GauCandy/WhiteCat/blob/main/thank.gif)
