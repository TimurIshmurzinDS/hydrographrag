import streamlit as st
import requests
import geopandas as gpd
import folium
from shapely import wkt
from streamlit_folium import st_folium
import os

st.set_page_config(page_title="HydroGraphRAG", page_icon="🌊", layout="wide")

st.title("🌊 HydroGraphRAG: Intelligent GIS Assistant")
st.markdown("Geospatial code generation and visualization based on knowledge graphs.")

API_URL = "http://127.0.0.1:8088/geo/plan_and_code/"
SHP_PATH = r"C:\Users\Timur\Desktop\Diplomme\Code\evaluation\data\basin_data.shp"

# --- STATE INITIALIZATION (SESSION CACHING) ---
if "api_data" not in st.session_state:
    st.session_state.api_data = None

# Хранилище для точек, у которых открыты таблички
if "opened_popups" not in st.session_state:
    st.session_state.opened_popups = set()

def render_map(points_data):
    if not os.path.exists(SHP_PATH):
        st.error(f"File not found: {SHP_PATH}")
        return
    
    basin_gdf = gpd.read_file(SHP_PATH)
    if basin_gdf.crs != "EPSG:4326":
        basin_gdf = basin_gdf.to_crs("EPSG:4326")
    
    centroid = basin_gdf.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=7, tiles="CartoDB positron")
    
    folium.GeoJson(
        basin_gdf,
        name="Basin boundaries",
        style_function=lambda x: {'fillColor': '#3498db', 'color': '#2980b9', 'weight': 1.5, 'fillOpacity': 0.1}
    ).add_to(m)
    
    coord_to_name = {}

    if points_data:
        for pt in points_data:
            try:
                geom = wkt.loads(pt['wkt'])
                lat, lon = geom.y, geom.x
                name = pt['name']
                
                coord_to_name[(round(lat, 4), round(lon, 4))] = name
                
                # Проверяем, должна ли табличка быть открытой
                is_opened = name in st.session_state.opened_popups

                if is_opened:
                    # Табличка висит постоянно
                    tooltip = folium.Tooltip(name, permanent=True, direction="top", opacity=0.9)
                    popup = None
                else:
                    # Подсказка только при наведении
                    tooltip = "Click to toggle info"
                    popup = name

                folium.Marker(
                    location=[lat, lon],
                    popup=popup,
                    tooltip=tooltip,
                    icon=folium.Icon(color='red', icon='tint') # Цвет всегда остается красным
                ).add_to(m)
            except Exception as e:
                continue
                
    map_data = st_folium(m, width=1200, height=500, returned_objects=["last_object_clicked"])
    
    # --- ОБРАБОТКА КЛИКОВ ПО КАРТЕ ---
    if map_data and map_data.get("last_object_clicked"):
        clicked_lat = round(map_data["last_object_clicked"]["lat"], 4)
        clicked_lon = round(map_data["last_object_clicked"]["lng"], 4)
        
        clicked_name = coord_to_name.get((clicked_lat, clicked_lon))
        
        if clicked_name:
            if clicked_name in st.session_state.opened_popups:
                st.session_state.opened_popups.remove(clicked_name)
            else:
                st.session_state.opened_popups.add(clicked_name)
            
            st.rerun()


query = st.text_area(
    "Enter hydrology query:", 
    placeholder="For example: Monitoring posts on the Tekes river", 
    height=100
)

if st.button("Generate solution", type="primary"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        # Сбрасываем открытые таблички при новом запросе
        st.session_state.opened_popups = set()
        
        with st.spinner("Agents are analyzing the graph..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        st.session_state.api_data = data
                    else:
                        st.error(f"⚠️ Failed: {data.get('message')}")
                else:
                    st.error(f"Server error: {response.status_code}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

# --- RENDERING FROM SESSION STATE ---
if st.session_state.api_data:
    data = st.session_state.api_data
    
    st.success("✅ Solution generated!")
    
    cols = st.columns(3)
    cols[0].metric("Category", data.get("category", "").upper())
    cols[1].metric("Triples extracted", data.get("triples_extracted", 0))
    cols[2].metric("Points on map", len(data.get("map_points", [])))
    
    st.divider()
    st.subheader("🗺️ Geospatial Visualization")
    
    # Отрисовка карты
    render_map(data.get("map_points", []))
    
    st.divider()
    st.subheader("📝 Analytical Report and Code")
    st.markdown(data.get("solution_code", ""))