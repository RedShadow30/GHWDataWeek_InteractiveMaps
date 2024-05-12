import streamlit as st
# importing scatter_mapbox function from state_city_map.py file
from state_city_map import state_city_choropleth_mapbox, state_city_scatter_mapbox
from aa_flight_paths import aa_flight_paths
from global_companies_map import global_companies_map

# always set page config
st.set_page_config(layout="wide")

st.title("GHW Data Week")

# make sure that the keys are connect to the chart types offered
SIDEBAR_DICT = {
    # making sure that first option is selected by default for testing easily
    "GLOBAL COMPANIES MAP": global_companies_map,
    "AA FLIGHT PATHS": aa_flight_paths,
    "STATE-CITY SCATTER MAP": state_city_scatter_mapbox,
    "STATE-CITY CHOROPLETH MAP": state_city_choropleth_mapbox
}


def main():
  # allowing user to select a 'key'/desired map from the sidebar
  chart_type = st.sidebar.radio("Select chart type:", SIDEBAR_DICT.keys())
  # when someone clicks on the radio button, the function is called
  SIDEBAR_DICT[chart_type]()


if __name__ == "__main__":
  main()
