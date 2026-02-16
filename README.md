# PPL Configuration Tools

A collection of Python scripts for generating and validating configuration files for the PPL (Power Platform) controller. This repository provides tools for device configuration, validation, and address mapping.

## Tools Overview

### 1. Devices Configurator
The Devices Configurator helps create a devices.json file for the PPL controller. It generates properly formatted JSON files based on your device specifications.

### 2. Devices Validator
The Devices Validator ensures that your devices.json file meets all required specifications and standards. It checks for:
- Proper file format
- Unique device IDs
- Required fields
- Optional fields
- Field types

### 3. Address Map Validator
The Address Map Validator verifies that your address mapping files are correct and conflict-free. It checks for:
- Proper file format
- Unique register names
- Required fields
- Optional fields
- Field types

## Installation

To use these tools, you'll need:

- Python 3.x
- No additional modules required for basic usage
- Streamlit (optional) for web interface versions:
```bash
pip install streamlit
```

## Usage

### Running the Tools

**Note:** For command-line versions, make sure to copy your JSON files into the repository directory before running the tools.

1. **Devices Configurator**

Command-line version:
```bash
python devices_configurator.py
```

Web interface version (requires streamlit):
```bash
streamlit run devices_configurator_streamlit.py
```

2. **Devices Validator**

Command-line version:
```bash
python devices_validator.py
```

Web interface version (requires streamlit):
```bash
streamlit run devices_validator_streamlit.py
```

3. **Address Map Validator**

Command-line version:
```bash
python address_map_validator.py <address_map_file>
```

Web interface version (requires streamlit):
```bash
streamlit run address_map_validator_streamlit.py
```

### Input/Output Formats

- Input files should be in JSON format
- Output files will be generated in the same directory as the script or can be downloaded from the web interface

## Requirements

- Python 3.x
- Streamlit (optional)
