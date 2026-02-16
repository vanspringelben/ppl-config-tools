import streamlit as st, json, zipfile
import os
from validators.project import find_missing_device_references, validate_control_map_commands
from validators.result import merge_validation_results
from validators.address_map import validate_address_map, get_precharge_contactor_feedback
from validators.control_map import validate_control_maps
from validators.devices import validate_devices
from validators.config import validate_config
from schemas.schemas import addressMapSchemas


st.title("Full Project Validator")

st.markdown(
    """
### How to use

You can validate an entire project by uploading either:

- A **ZIP** that contains your project JSON files, or
- Multiple **JSON** files directly.

After uploading, you must **classify each file** so the validator knows what it is:

1. For each uploaded JSON file, choose its **File type**.
2. If you select **Address Map**, you must also choose the correct **Map type**.
3. Click **Validate All Files**.

The validator will check each file’s schema and also perform some cross-file checks (for example, validating control map commands and verifying device references across the uploaded files).
"""
)

if "full_project_uploaders_nonce" not in st.session_state:
    st.session_state.full_project_uploaders_nonce = 0

zip_file = st.file_uploader(
    "Upload folder as ZIP (optional)",
    type="zip",
    key=f"full_project_zip_{st.session_state.full_project_uploaders_nonce}",
)
json_files = st.file_uploader(
    "Or upload multiple JSON files",
    type="json",
    accept_multiple_files=True,
    key=f"full_project_json_{st.session_state.full_project_uploaders_nonce}",
)

if zip_file is not None or json_files:
    if st.button("Remove all uploaded files"):
        st.session_state.full_project_uploaders_nonce += 1
        st.rerun()

items: list[dict] = []

if zip_file is not None:
    try:
        z = zipfile.ZipFile(zip_file)
        for name in z.namelist():
            if name.lower().endswith(".json") and not name.endswith("/"):
                display_name = os.path.basename(name)
                items.append({"name": display_name, "bytes": z.read(name)})
    except Exception as e:
        st.error(f"Could not read ZIP: {e}")

if json_files:
    for f in json_files:
        try:
            items.append({"name": getattr(f, "name", "(uploaded).json"), "bytes": f.getvalue()})
        except Exception as e:
            st.error(f"Could not read uploaded file: {e}")

if items:
    st.subheader("Assign File Types")

    selections: list[dict] = []
    map_types = list(addressMapSchemas.keys())

    for idx, item in enumerate(items):
        name = item["name"]
        default_role = "Config" if name == "config.json" else "Devices" if name == "devices.json" else "Control Map" if "control" in name else "Address Map" if "address" in name else "Address Map"

        with st.container():
            st.markdown(f"**{name}**")
            role = st.selectbox(
                "File type",
                ["Config", "Devices", "Address Map", "Control Map"],
                index=0 if default_role == "Config" else 1 if default_role == "Devices" else 3 if default_role == "Control Map" else 2,
                key=f"role_{idx}_{name}",
            )

            map_type = None
            if role == "Address Map":
                map_type = st.selectbox(
                    "Map type",
                    map_types,
                    index=0 if "Modbus TCP/IP" not in map_types else map_types.index("Modbus TCP/IP"),
                    key=f"maptype_{idx}_{name}",
                )

            selections.append({"name": name, "bytes": item["bytes"], "role": role, "map_type": map_type})

    if st.button("Validate All Files", type="primary"):
        st.subheader("Validation Results")
        any_errors = False
        any_warnings = False

        available_files = {os.path.basename(s["name"]) for s in selections}

        parsed_by_file: dict[str, object] = {}
        address_maps_by_file: dict[str, object] = {}
        devices_payload = None

        device_files = [s for s in selections if s["role"] == "Devices"]
        if len(device_files) == 0:
            st.error("No devices file selected"); any_errors = True
        elif len(device_files) > 1:
            st.error("Multiple devices files selected"); any_errors = True

        config_files = [s for s in selections if s["role"] == "Config"]
        if len(config_files) == 0:
            st.error("No config file selected"); any_errors = True
        elif len(config_files) > 1:
            st.error("Multiple config files selected"); any_errors = True

        for sel in selections:
            file_key = os.path.basename(sel["name"])
            try:
                parsed_by_file[file_key] = json.loads(sel["bytes"].decode("utf-8"))
            except Exception:
                continue

            if sel["role"] == "Devices":
                devices_payload = parsed_by_file[file_key]
            elif sel["role"] == "Address Map":
                address_maps_by_file[file_key] = parsed_by_file[file_key]

        for sel in selections:
            st.markdown(f"**{sel['name']}**")
            try:
                data = json.loads(sel["bytes"].decode("utf-8"))
            except Exception as e:
                st.error(f"Invalid JSON: {e}")
                any_errors = True
                continue

            if sel["role"] == "Devices":
                devices_result = validate_devices(data)
                refs_result = find_missing_device_references(data, available_files)
                result = merge_validation_results(devices_result, refs_result)
            elif sel["role"] == "Config":
                result = validate_config(data)
            elif sel["role"] == "Control Map":
                base_result = validate_control_maps(data)
                cross_result = validate_control_map_commands(
                    control_map_file=sel["name"],
                    control_map=data,
                    devices=devices_payload,
                    address_maps_by_file=address_maps_by_file,
                )
                result = merge_validation_results(base_result, cross_result)
            else:
                if sel["map_type"] == "Precharge" and isinstance(devices_payload, list):
                    address_map_file = os.path.basename(sel["name"])
                    precharge_contactor_feedback = get_precharge_contactor_feedback(devices_payload, address_map_file)
                    result = validate_address_map(data, sel["map_type"], precharge_contactor_feedback)
                else:
                    result = validate_address_map(data, sel["map_type"])

            for m in result.messages:
                getattr(st, m.level)(m.message)

            if not result.has_errors:
                if result.has_warnings:
                    st.warning("Valid with warnings ⚠")
                    any_warnings = True
                else:
                    st.success("Valid ✔")
            else:
                st.error("Errors found ❌")
                any_errors = True
                any_warnings = any_warnings or result.has_warnings

        st.subheader("Validation Summary")
        if any_errors:
            st.error("Errors found ❌")
        elif any_warnings:
            st.warning("Valid with warnings ⚠")
        else:
            st.success("Valid ✔")