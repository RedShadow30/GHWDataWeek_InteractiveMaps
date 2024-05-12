import time
import folium
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from folium.plugins import MarkerCluster
from geopy.exc import GeocoderQuotaExceeded, GeocoderTimedOut
from geopy.geocoders import Nominatim

PATH_TO_DATA = "companies_data.csv"


def global_companies_map():
  # add a subtitle
  st.subheader("Global Distribution of Top Companies")

  # load data into Pandas DF
  companies_data = pd.read_csv(PATH_TO_DATA, index_col="Ranking")
  companies_data = companies_data[0:50]

  # show a table, index will alaready be plotted
  st.dataframe(companies_data[["Company", "Country"]])

  # initialize a geocode with a user agent
  geolocator = Nominatim(user_agent="redshadow30_ghw_data_week")

  # create a folim map
  map = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb dark_matter")

  # create a MarkerCluster
  marker_cluster = MarkerCluster().add_to(map)

  # iterate over the DF
  for index, row in companies_data.iterrows():
    country_query = row["Country"]
    try:
      # location stores the lat and long of company
      location = geolocator.geocode(country_query, timeout=10, language='en')
      if location:
        st.write(f"Geocoding result for {row['Company']}, {country_query} {location.address}")
        # plot the location
        popup_message = f"{index}: {row['Company']}, {row['Country']}"
        folium.Marker(location=[location.latitude,
                      location.longitude],
                      popup=popup_message).add_to(marker_cluster)
      else:
        st.error(f"Geocoding failure for {index}: {country_query}")
        # wait for one second
      time.sleep(0.5)
    except (GeocoderTimedOut, GeocoderQuotaExceeded) as e:
      st.error(f"Geocoding error: {e} for {country_query}")

  # save map as HTML file
  map.save("companies_map.html")
  HtmlFile = open("companies_map.html", "r", encoding="utf-8")
  my_map = HtmlFile.read()
  components.html(my_map, height=700)
