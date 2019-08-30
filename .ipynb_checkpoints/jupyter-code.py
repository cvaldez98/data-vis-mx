# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), '.ipynb_checkpoints'))
	print(os.getcwd())
except:
	pass
#%%
import os
import numpy as np
import pandas as pd
import folium
import json
dirpath = os.getcwd()
print('dirpath', dirpath)


#%%
data = pd.read_csv('delitos.csv', encoding="latin_1")

print("Shape!", data.shape)
print(data.index)
print(data.keys())
def total_abs(data):
    d = {} # dictionary!
    for index, series in data.iterrows():
        if(series['Entidad'] in d):
            curr = d[series['Entidad']] # the tuple curr[0] == total, curr[1] == homicidios totales
            d[series['Entidad']] = (curr[0], curr[1] + sumMonths(series), curr[2] + checkHomicide(series))
#             d[series['Entidad']] += sumMonths(series)
        else:
            d[series['Entidad']] = (series['Entidad'], sumMonths(series), checkHomicide(series))
        
#     print('estados', d)
    return d

def checkHomicide(series):
    if(series['Tipo de delito'] == 'Homicidio'):
        return sumMonths(series)
    else:
        return 0

# get the total of all 12 months, take in a 'series'
def sumMonths(s):
#     print('SERIESSSSS', s[])
    result = 0
    for i in range(9, 21):
        result += s[i]
    return result

d = total_abs(data)
state_results = pd.DataFrame.from_dict(d, orient='index', columns=['Estado', 'Total', 'Homicidios'])
state_results


#%%
# mapping data
centro_lat, centro_lon = 22.396092, -101.731430
folium_map = folium.Map(location=[centro_lat, centro_lon], zoom_start=5, tiles='cartodb positron')
fg = folium.FeatureGroup(name='Estados Mexicanos')
fg.add_child(folium.GeoJson(open("statesGEOJSON.json",encoding = "utf-8-sig").read()))
# folium_map
folium_map.add_child(fg)
folium.LayerControl().add_to(folium_map)
# save it, (won't render here for some reason...)
folium_map.save('test.html')


#%%
# using choropleth
centro_lat, centro_lon = 22.396092, -101.731430
m = folium.Map(location=[centro_lat, centro_lon], zoom_start=5, tiles='cartodb positron')
folium.Choropleth(
    geo_data=open("statesGEOJSON.json",encoding = "utf-8-sig").read(),
    name='Mexico',
    highlight=True,
    data=state_results,
    columns=['Estado', 'Homicidios'],
    key_on='feature.properties.NOM_ENT',
    fill_color='RdPu',
    nan_fill_color='Gray',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Estados'
).add_to(m)

m.save('test.html')


#%%



