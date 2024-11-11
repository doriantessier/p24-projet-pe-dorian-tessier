# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# # Projet info

# On importe les bibliothèques qui seront utiles

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ## Première observation des fichiers

# On commence par lire les fichiers et observer ce qu'ils contiennent

df1 = pd.read_csv("cities.csv", sep=",",)
print(df1.head())
df1.describe()

df2 = pd.read_csv("countries.csv")
print(df2.head())
df2.describe()

df3 = pd.read_csv("daily-weather-cities.csv")
print(df3.head())
df3.describe()

# On change les index des dataframe pour y voir plus clair

df1.set_index("station_id")


df2.set_index("country")

df3.set_index("station_id")

# La première dataframe contient une liste de villes, associées aux pays et à leurs coordonnées GPS (latitude, longitude).
# La deuxième dataframe contient une liste de pays, leur population , leur capitale, leur superficie, ainsi que les régions et  continent auxquels ces pays appartiennent.
# La troisième dataframe contient une liste de relevé de mesure de température, précipitations et autres, dans plusieurs villes européennes.

# ## Tri des dataframes

# Je vais commencer par trier la 3ème dataframe

# +
#tri des différentes data frame

#tri de df3 par ordre alphabétique et par date croissante
df3.sort_values(['city_name','date'], inplace=True)

# -

# Je vais maintenant trier la deuxième dataframe, en ajoutant les données manquantes.

#5 pays ne sont pas renseignés, j'ajoute leurs populations
df2.loc[10, 'population'] = 2.6768589e+7  #australie
df2.loc[66, 'population'] = 2.3e+6        #gabon
df2.loc[71, 'population'] = 1.0482487e+7  #grèce
df2.loc[208, 'population'] = 3.1e+6       #pays de galles

#tri de df2 par population croissante
df4 = df2.sort_values('population', inplace = False)
df5 = df2.sort_values('area', inplace = False)


#on complète les lignes des superficie où il manque des valeurs
df2.loc[173, 'area'] = 4190   #south georgia
df2.loc[180, 'area'] = 62045  #svalbard and jan mayen
df2.loc[157, 'area'] = 121.7  #saint hélène
df2.loc[123, 'area'] = 374    #mayotte
df2.loc[63, 'area'] = 83534   #guyane française
df2.loc[156, 'area'] = 2512   #réunion
df2.loc[208, 'area'] = 20761  #pays de galles

# J'ajoute une colonne 'densité', qui est le quotient de la population du pays et de sa superficie.

#on crée une colonne densité
df2['density'] = df2['population']/df2['area']
df2.sort_values('density', inplace = True)
df2.tail(7)

# ## Tracés des mesures réalisées par les stations de la 3eme dataframe

# Maintenant, je vais tracer plusieurs mesures réalisées par les stations de la dataframe 3, et les tracer en fonction du temps, afin de pouvoir observer certaines tendances.

# On commence par faire une moyenne sur les températures minimales et maximales relevées chaque années

# +
#on commence par changer le type de la colonne date
df3['date'] = pd.to_datetime(df3['date'])
df3['year'] = df3['date'].dt.year  #colonne année pour faire ensuite la moyenne


moy_min_ville_annee = df3.groupby(['city_name', 'year'])['min_temp_c'].mean().reset_index()
moy_max_ville_annee = df3.groupby(['city_name', 'year'])['max_temp_c'].mean().reset_index()


#on trace pour chaque ville la courbe des températures maximale

plt.figure(1, figsize=(10, 6))


for ville in moy_max_ville_annee['city_name'].unique():
    data_ville = moy_max_ville_annee[moy_max_ville_annee['city_name'] == ville]
    plt.plot(data_ville['year'], data_ville['max_temp_c'], marker='o', label=ville)


plt.xlabel("Année")
plt.ylabel("Température moyenne maximale (°C)")
plt.title("Température moyenne maximale annuelle par ville")
plt.legend(title="Ville")
plt.grid(True)


#idem avec minimale

plt.figure(2, figsize=(10, 6))


for ville in moy_min_ville_annee['city_name'].unique():
    data_ville = moy_min_ville_annee[moy_min_ville_annee['city_name'] == ville]
    plt.plot(data_ville['year'], data_ville['min_temp_c'], marker='o', label=ville)


plt.xlabel("Année")
plt.ylabel("Température moyenne minimale (°C)")
plt.title("Température moyenne minimale annuelle par ville")
plt.legend(title="Ville")
plt.grid(True)

plt.show()
# -
# On remarque une hausse des températures minimales et globales de 2°C environ pour toutes les villes, avec une forte hausse depuis 1975. Regardons l'évolution de la température annuelle moyenne.

# +
moy_avg_ville_annee = df3.groupby(['city_name', 'year'])['avg_temp_c'].mean().reset_index()


plt.figure(3, figsize=(10, 6))


for ville in moy_max_ville_annee['city_name'].unique():
    data_ville = moy_avg_ville_annee[moy_avg_ville_annee['city_name'] == ville]
    plt.plot(data_ville['year'], data_ville['avg_temp_c'], marker='o', label=ville)


plt.xlabel("Année")
plt.ylabel("Température moyenne (°C)")
plt.title("Température moyenne annuelle par ville")
plt.legend(title="Ville")
plt.grid(True)
plt.show()
# -

# On remarque encore une fois une hausse de 2°C pour l'ensemble des 4 villes.

# On fait pareil pour l'ensoleillement, il n'y a que Berlin de renseigné.


# +
moy_sun_ville_annee = df3.groupby(['city_name', 'year'])['sunshine_total_min'].mean().reset_index()



plt.figure(4, figsize=(10, 6))

data_berlin = moy_sun_ville_annee[moy_sun_ville_annee['city_name'] == "Berlin"]
plt.plot(data_berlin['year'], data_berlin['sunshine_total_min'], marker='o', label="Berlin")


plt.xlabel("Année")
plt.ylabel("Ensoleillement annuel")
plt.title("Ensoleillement minimal moyen annuel à Berlin")
plt.legend()
plt.grid(True)
plt.show()
# -

# Malgré la hausse de la température constatée à Berlin d'après les graphes précédents, l'ensoleillement annuel n'a que très peu évolué. Ainsi cette hausse n'est pas dûe à l'action du Soleil. Il ne peut donc que s'agir de l'action de l'homme. Regardons maintenant l'évolution du niveau de la Mer du Nord en Allemagne.

# +
moy_sea_ville_annee = df3.groupby(['city_name', 'year'])['avg_sea_level_pres_hpa'].mean().reset_index()



plt.figure(5, figsize=(10, 6))

data_berlin2 = moy_sea_ville_annee[moy_sea_ville_annee['city_name'] == "Berlin"]
plt.plot(data_berlin2['year'], data_berlin2['avg_sea_level_pres_hpa'], marker='o', label="Berlin")



#on fait une régression linéaire pour avoir une tendance. On enlève les NaN sinon ça pose problème.

data_berlin22 = data_berlin2.dropna(subset=['year', 'avg_sea_level_pres_hpa'])

a,b = np.polyfit(data_berlin22['year'].to_numpy(), data_berlin22['avg_sea_level_pres_hpa'].to_numpy(), 1)  

regression = a * data_berlin22['year'] + b


plt.plot(data_berlin22['year'], regression, 'r-', label=f"Régression linéaire : y = {a:.3f}x + {b:.3f}")  


plt.xlabel("Année")
plt.ylabel("Pression moyenne au niveau de la mer (hPa)")
plt.title("Régression linéaire de la pression moyenne au niveau de la mer par année")
plt.legend()
plt.grid(True)

plt.show()
# -

# Ainsi, le niveau de la mer a tendance à augmenter lui aussi, un nouvel impact du réchauffement climatique. Cette hausse est de $0,015 hPa$ par an environ.

# ## Observations sur la 2eme dataframe

# Reagardons les données de la deuxième DataFrame, et voyons quelles sont les régions du monde les plus peuplées.

# +
regions = df2.groupby('region').agg(population_totale=('population', 'sum'),superficie_totale=('area', 'sum')).reset_index()

# On calcule la densité de chaque région, puis on trie par ordre décroissant.
regions['densite_population'] = regions['population_totale'] / regions['superficie_totale']
regions = regions.sort_values(by='densite_population', ascending=False).reset_index(drop=True)

print(regions)
# -

# On fait la même chose en triant cette fois par continent

# +
continents = df2.groupby('continent').agg(population_totale=('population', 'sum'),superficie_totale=('area', 'sum')).reset_index()


continents['densite_population'] = continents['population_totale'] / continents['superficie_totale']
continents = continents.sort_values(by='densite_population', ascending=False).reset_index(drop=True)

print(continents)
# -

# Aussi bien pour les régions que pour les continents, c'est l'Asie qui arrive en tête des pays avec la densité la plus élevée avec une densité continentale de 135 personnes par $km^2$, ce qui est presque 4 fois plus que le deuxième continent avec la plus grande densité, l'Afrique, et ses 37 personnes par $km^2$.

# ## Conclusion

# Ainsi, l'évolution de réchauffement climatique se remarque par une hausse globale des températures d'après les relevés européens, mais aussi par une hausse du niveau global des mers. Les aléas étant presque les mêmes pour tout le monde, ce sont les enjeux qui augmenteront les risques. Les pays et régions du monde les plus peuplées seront les plus touchées par les évènements climatiques.
