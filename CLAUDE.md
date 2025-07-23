# LLM Translator Project

This project provides a Python library for parsing and manipulating XLIFF and SDLXLIFF translation files.

## Project Structure

The core functionality is in `src/parsers/xliff.py`, which provides a simple wrapper around lxml.objectify for perfect roundtrip parsing of XLIFF files.

## Key Files

- `src/parsers/xliff.py` - Main XLIFF/SDLXLIFF parser using lxml.objectify
- `pyproject.toml` - Project configuration, requires Python >=3.11

## Usage

```python
from src.parsers.xliff import XliffDocument

# Parse XLIFF file
doc = XliffDocument.from_file('file.xlf')

# Access translation units
for tu in doc.get_translation_units():
    print(f"Source: {tu.source}")
    if hasattr(tu, 'target'):
        print(f"Target: {tu.target}")

# Modify content
tu_list = list(doc.get_translation_units())
tu_list[0].target = "New translation"
tu_list[0].target.attrib['state'] = 'translated'

# Write back to file
doc.to_file('output.xlf')
```

## Technical Details

- Uses lxml.objectify for automatic XML-to-object conversion
- Supports both XLIFF 1.2 and SDLXLIFF (SDL Trados) formats
- Perfect structure preservation for roundtrip capability
- Automatic namespace handling
- All elements accessible via dot notation and dictionary syntax

## Dependencies

- lxml>=6.0.0 (for XML parsing and objectify)

## Running Commands

Use `uv run python` to run Python scripts with proper dependencies.

## Code Practices

- Prefer not to swallow exceptions and just return them to the caller.