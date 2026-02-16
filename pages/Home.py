import streamlit as st


st.title("Power Platform - File Validator")

st.write(
    "This app validates the configuration files for the Power Platform controller. "
    "Use it to confirm that your JSON files are correctly structured before deploying or sharing them."
)

st.info(
    "Tip: If you have a full set of files, start with **Full Project Validator** for both schema checks and cross-file checks.",
    icon=None,
)

st.markdown(
    """
## How it works

1. You upload the relevant JSON file(s).
2. The validator checks the content against the expected schema.
3. You get a clear pass/fail result plus detailed messages for anything that needs attention.
"""
)

st.markdown("## Validators")

left, right = st.columns(2)

with left:
    st.subheader("Address Map Validator")
    st.write("Validates a single `address_map.json` against the schema for a selected protocol/format.")
    st.markdown("Open: [Address Map Validator](/address-map)")

    st.subheader("Devices File Validator")
    st.write("Validates `devices.json` (device definitions and required fields).")
    st.markdown("Open: [Devices File Validator](/devices-file)")

with right:
    st.subheader("Control Map Validator")
    st.write("Validates a single `control_map.json` (control commands and expected structure).")
    st.markdown("Open: [Control Map Validator](/control-map)")

    st.subheader("Config File Validator")
    st.write("Validates `config.json` (controller/config settings and required fields).")
    st.markdown("Open: [Config File Validator](/config-file)")

st.subheader("Full Project Validator")
st.write(
    "Upload a ZIP or multiple JSON files to validate everything at once. "
    "Includes cross-file checks (for example, verifying references between control maps, devices, and address maps)."
)
st.markdown("Open: [Full Project Validator](/full-project)")

st.caption("You can also navigate between pages using the sidebar.")
