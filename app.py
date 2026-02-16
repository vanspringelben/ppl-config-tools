import streamlit as st

st.set_page_config(page_title="File Validator | Direct Energy Partners", page_icon="images/DEP_LOGO.png", layout="wide")

st.sidebar.image(image="images/DEP_LOGO_COMPLETE.png", use_container_width=True)

home_page = st.Page(page="pages/Home.py", title="Home", url_path="home", default=True)
address_map_page = st.Page(page="pages/Address_Map.py", title="Address Map Validator", url_path="address-map")
control_map_page = st.Page(page="pages/Control_Map.py", title="Control Map Validator", url_path="control-map")
devices_page = st.Page(page="pages/Devices.py", title="Devices File Validator", url_path="devices-file")
config_page = st.Page(page="pages/Config.py", title="Config File Validator", url_path="config-file")
full_project_page = st.Page(page="pages/Full_Project.py", title="Full Project Validator", url_path="full-project")

pg = st.navigation([home_page, address_map_page, control_map_page, devices_page, config_page, full_project_page])
pg.run()
