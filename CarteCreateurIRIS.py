# coding: utf8
import os
import webbrowser
import argparse
import pandas
import geopandas
import folium
from ast import literal_eval

# construct the argument parse 
parser = argparse.ArgumentParser(
    description='Createur de carte IRIS par département')
parser.add_argument('departement', help="numero du département")
parser.add_argument('localisationGPS', help="donner la localisation du centre du département, format: [40.5,5.2]")
args = parser.parse_args()
dep = args.departement
loc = literal_eval(args.localisationGPS)


# Ouverture IRIS contours
iris_geo = os.path.join('IRIS/contours-iris-2016.geojson')
iris_geo_data0 = geopandas.read_file(iris_geo)
iris_geo_data = iris_geo_data0[iris_geo_data0.code_dept == dep]

# Ouvre communes
communes_geo_path = os.path.join('communes-20190101/communes-20190101.json')
communes_geo0 = geopandas.read_file(communes_geo_path)
insee_dep_start = dep + '000'
insee_dep_end = dep + '999'
communes_geo = communes_geo0[(communes_geo0.insee >= insee_dep_start) & (communes_geo0.insee < insee_dep_end)]

# Ouvre données
log = os.path.join('communes-20190101/base-cc-logement-2015.csv')
dtype = {}
for i in range(0,3) :
	dtype[i] = 'str'

for i in range(4,88) :
	dtype[i] = 'float'
data0 = pandas.read_csv(log, delimiter=';', skiprows=5, decimal=',',dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(4,88) :
	nom = 'Cartes/base-cc-logement-2015-' + L[i] + '.html'
	print(L[i])
	taux =L[i]+'_TAUX'
	data[taux] = 100 * data[L[i]] / data['P15_LOG']
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = communes_geo,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['CODGEO', L[i]],
		key_on='feature.properties.insee',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	folium.Choropleth(
		geo_data = communes_geo,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['CODGEO', taux],
		key_on='feature.properties.insee',
		name= taux,
		legend_name= taux,
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m	

del dtype, L, nom, data0, data

# Ouvre données
log = os.path.join('communes-20190101/base-cc-filosofi-2015.csv')
dtype = {}
for i in range(0,1) :
	dtype[i] = 'str'
for i in range(2,29) :
	dtype[i] = 'float'
data0 = pandas.read_csv(log, delimiter=';', skiprows=5, decimal=',',dtype=dtype)
data = data0[(data0.CODGEO >= insee_dep_start) & (data0.CODGEO < insee_dep_end)]

L = list(data.columns.values)
for i in range(2,29) :
	nom = 'Cartes/base-cc-filosofi-2015-' + L[i] + '.html'
	print(L[i])
	taux =L[i]+'_TAUX'
	data[taux] = 100 * data[L[i]] / data['NBPERSMENFISC15']
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = communes_geo,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['CODGEO', L[i]],
		key_on='feature.properties.insee',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	folium.Choropleth(
		geo_data = communes_geo,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['CODGEO', taux],
		key_on='feature.properties.insee',
		name= taux,
		legend_name= taux,
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data
	
# Ouverture IRIS structure population
struc_pop = os.path.join('IRIS/base-ic-evol-struct-pop-2015.csv')
dtype1 = {}
for i in range(0,9) :
	dtype1[i] = 'str'

for i in range(10,81) :
	dtype1[i] = 'float'

struc_pop_data0 = pandas.read_csv(struc_pop, delimiter=';', skiprows=5, decimal=',', dtype=dtype1)
struc_pop_data = struc_pop_data0[struc_pop_data0.DEP == dep]

L1 = list(struc_pop_data.columns.values)
for i in range(10,81) :
	nom = 'Cartes/base-ic-evol-struct-pop-2015-' + L1[i] + '.html'
	print(L1[i])
	taux2 =L1[i]+'_TAUX'
	struc_pop_data[taux2] = 100 * struc_pop_data[L1[i]] / struc_pop_data['P15_POP']
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = struc_pop_data,
		columns = ['IRIS', L1[i]],
		key_on='feature.properties.code_iris',
		name= L1[i],
		legend_name= L1[i],
	).add_to(m)
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = struc_pop_data,
		columns = ['IRIS', taux2],
		key_on='feature.properties.code_iris',
		name= taux2,
		legend_name= taux2,
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m	

# Ouverture IRIS activite population
act_pop = os.path.join('IRIS/base-ic-activite-residents-2015.csv')
dtype2 = {}
for i in range(0,11) :
	dtype2[i] = 'str'

for i in range(12,114) :
	dtype2[i] = 'float'
act_pop_data0 = pandas.read_csv(act_pop, delimiter=';', skiprows=5, decimal=',', dtype=dtype2)
act_pop_data = act_pop_data0[act_pop_data0.DEP == dep]

L2 = list(act_pop_data.columns.values)
for i in range(12,114) :
	nom = 'Cartes/base-ic-activite-residents-2015-' + L2[i] + '.html'
	print(L2[i])
	taux =L2[i]+'_TAUX'
	act_pop_data[taux] = 100 * act_pop_data[L2[i]] / act_pop_data['P15_POP1564']
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = act_pop_data,
		columns = ['IRIS', L2[i]],
		key_on='feature.properties.code_iris',
		name= L2[i],
		legend_name= L2[i],
	).add_to(m)
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = act_pop_data,
		columns = ['IRIS', taux],
		key_on='feature.properties.code_iris',
		name= taux,
		legend_name= taux,
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

# Ouverture IRIS service médical
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-medical-para-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,29) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,29) :
	nom = 'Cartes/equip-serv-medical-para-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-action-sociale-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,23) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,23) :
	nom = 'Cartes/equip-serv-action-sociale-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-commerce-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,29) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,29) :
	nom = 'Cartes/equip-serv-commerce-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-ens-1er-degre-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,21) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,21) :
	nom = 'Cartes/equip-serv-ens-1er-degre-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-ens-2e-degre-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,29) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,29) :
	nom = 'Cartes/equip-serv-ens-2e-degre-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-ens-sup-form-serv-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,25) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,25) :
	nom = 'Cartes/equip-serv-ens-sup-form-serv-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-particuliers-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,43) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,43) :
	nom = 'Cartes/equip-serv-particuliers-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-serv-sante-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,23) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,23) :
	nom = 'Cartes/equip-serv-sante-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-sport-loisir-socio-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,97) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,97) :
	nom = 'Cartes/equip-sport-loisir-socio-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data

# Ouverture carte IRIS
chemin = os.path.join('IRIS/Ensemble-infra-2017/equip-tour-transp-infra-2017.csv')
dtype = {}
for i in range(0,5) :
	dtype[i] = 'str'

for i in range(6,13) :
	dtype[i] = 'float'
data0 = pandas.read_csv(chemin, delimiter=';', skiprows=5, decimal=',', dtype=dtype)
data = data0[data0.DEP == dep]

L = list(data.columns.values)
for i in range(6,13) :
	nom = 'Cartes/equip-tour-transp-infra-2017-' + L[i] + '.html'
	print(L[i])
	# Affiche la carte
	m = folium.Map(
    		location=loc,
    		zoom_start=9,
		tiles='OpenStreetMap'
		)
	folium.TileLayer('Stamen Toner').add_to(m)
	# Carte colorimétrique
	folium.Choropleth(
		geo_data = iris_geo_data,
		fill_color='YlOrRd', 
		fill_opacity=0.5, 
		line_opacity=0.8,
	        data = data,
		columns = ['IRIS', L[i]],
		key_on='feature.properties.code_iris',
		name= L[i],
		legend_name= L[i],
	).add_to(m)
	# Pour selection type carte
	folium.LayerControl().add_to(m)
	# Sauvegarde
	m.save(nom)
	# Efface
	del m

del dtype, L, nom, data0, data
