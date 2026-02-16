import streamlit as st, json
from validators.config import validate_config


st.title("Config File Validator")

st.markdown(
    """
### How to use

1. Upload the **config JSON** file (named `config.json`).
2. Click **Validate**.

The validator will check:
- The file is valid JSON
- The structure matches the expected schema
- Required fields are present and values have the expected types
"""
)

file = st.file_uploader("Upload config.json", type="json")

if file and st.button("Validate", type="primary"):
    data = json.load(file)
    result = validate_config(data)

    for m in result.messages:
        getattr(st, m.level)(m.message)

    if not result.has_errors:
        if result.has_warnings:
            st.warning("Valid with warnings ⚠")
        else:
            st.success("Valid ✔")
    else:
        st.error("Errors found ❌")
