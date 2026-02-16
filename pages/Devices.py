import streamlit as st, json
from validators.devices import validate_devices


st.title("Devices File Validator")

st.markdown(
    """
### How to use

1. Upload the **devices JSON** file (named `devices.json`).
2. Click **Validate**.

The validator will check:
- The file is valid JSON
- The structure matches the expected schema
- Required fields are present and values have the expected types
"""
)

file = st.file_uploader("Upload devices.json", type="json")

if file and st.button("Validate", type="primary"):
    devices = json.load(file)
    result = validate_devices(devices)

    for m in result.messages:
        getattr(st, m.level)(m.message)

    if not result.has_errors:
        if result.has_warnings:
            st.warning("Valid with warnings ⚠")
        else:
            st.success("Valid ✔")
    else:
        st.error("Errors found ❌")