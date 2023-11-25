from pathlib import Path
import json

import plotly
import plotly.express as px

path = Path('eq data/eq_data_30_day_m1.geojson')
contents = path.read_text(encoding='utf-8')
all_eq_data = json.loads(contents)

all_eq_dicts = all_eq_data['features']

mags,lons,lats,eq_titles =[],[],[],[]
for eq_dict in all_eq_dicts:
     mag = eq_dict['properties']['mag']
     eq_title = eq_dict['properties']['title']
     lon = eq_dict['geometry']['coordinates'][0]
     lat = eq_dict['geometry']['coordinates'][1]

     mags.append(mag)
     eq_titles.append(eq_title)
     lons.append(lon)
     lats.append(lat)

title = 'global earthquakes'
fig = px.scatter_geo(lat=lats,lon=lons,size=mags,title=title,
                     color=mags,
                     color_continuous_scale='Viridis',
                     labels={'color':'Magnitude'},
                     projection='orthographic',
                     hover_name=eq_titles,
                     )

plotly.offline.plot(fig)