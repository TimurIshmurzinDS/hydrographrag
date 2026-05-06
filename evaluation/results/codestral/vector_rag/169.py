python
       import geopandas as gpd
       from shapely.geometry import LineString

       # Предположим, что у нас есть данные о реках в формате GeoDataFrame
       # rivers_gdf = gpd.read_file("rivers_data.geojson")

       # Для примера, создадим простые линейные объекты для рек Шынжалы и Талгар
       shynzhaly_river = LineString([(71.4502, 51.1683), (71.4955, 51.1800)])
       talgar_river = LineString([(71.4700, 51.1700), (71.4500, 51.1600)])

       # Создаем GeoDataFrame для этих рек
       rivers_gdf = gpd.GeoDataFrame({'river': ['Shynzhaly', 'Talgar'], 'geometry': [shynzhaly_river, talgar_river]})

       # Определяем точки пересечения русел рек
       intersection_points = rivers_gdf.unary_union.intersection(rivers_gdf['geometry'].iloc[0].intersection(rivers_gdf['geometry'].iloc[1]))

       print("Точки пересечения русел рек Шынжалы и Талгар:", intersection_points)