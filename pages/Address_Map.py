import streamlit as st, json
from validators.address_map import validate_address_map
from schemas.schemas import addressMapSchemas


st.title("Address Map Validator")

st.markdown(
    """
### How to use

1. Upload the **address map JSON** file (typically named `address_map.json`).
2. Select the correct **Map type** from the dropdown (this must match the protocol/format your address map was created for).
3. Click **Validate**.

The validator will check:
- The file is valid JSON
- The structure matches the selected map type schema
- Required fields are present and values have the expected types
"""
)

file = st.file_uploader("Upload address_map.json", type="json")
map_type = st.selectbox("Map type", list(addressMapSchemas.keys()))

if file and st.button("Validate", type="primary"):
    data = json.load(file)
    result = validate_address_map(data, map_type)

    for m in result.messages:
        getattr(st, m.level)(m.message)

    if not result.has_errors:
        if result.has_warnings:
            st.warning("Valid with warnings ⚠")
        else:
            st.success("Valid ✔")
    else:
        st.error("Errors found ❌")