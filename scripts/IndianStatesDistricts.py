import json

import pandas as pd


df = pd.read_csv('IndianStatesDistricts.csv')

states_list = df['State / Union Territory'].unique()

country = []
for s in states_list:
    districts_list = df.loc[df['State / Union Territory']
                            == s]['District'].unique()

    state = {
        "state": s,
        "districts": list(districts_list)
    }

    country.append(state)

with open('IndianStatesDistricts.json', 'w+') as fp:
    json.dump(country, fp)
