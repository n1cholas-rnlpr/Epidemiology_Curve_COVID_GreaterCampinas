#!/usr/bin/env python
# coding: utf-8

print("OBSERVATÓRIO PUC-CAMPINAS  -  BOLETIM COVID-19 DRS RMC Campinas\nSCRIPT PY - CURVA EPIDEMIOLÓGICA PARA A REGIÃO METROPOLITANA DE CAMPINAS")

import pandas as pd
import numpy as np

import plotly.express as px

import locale

locale.setlocale(locale.LC_TIME, 'pt_BR')




df = pd.read_csv("https://raw.githubusercontent.com/seade-R/dados-covid-sp/master/data/dados_covid_sp.csv", sep=";", decimal=",")



# Selecionando as observações correspondentes a Campinas.
dfcps = df[df['codigo_ibge'] == 3509502]
print(dfcps.shape)

# Selecionando as observações correspondentes a Regiao Metropolitana de Campinas.
cod_rmc = [3501608, 3503802, 3509502, 3512803, 3515152, 3519055, 3519071,
           3520509, 3523404, 3524709, 3531803, 3532009, 3533403, 3536505,
           3537107, 3545803, 3548005, 3552403, 3556206, 3556701]

dfrmc = df[df['codigo_ibge'].isin(cod_rmc)]

# Selecionando as observações correspondentes ao Departamento de Saude
cod_dep_saude = [3500501, 3501608 ,3501905, 3503802, 3504107, 3507100, 3507605,
                 3508405, 3509502, 3509601, 3512803, 3519055, 3519071, 3520509,
                 3523404, 3524006, 3524709, 3525201, 3525508, 3525904, 3527009,
                 3527306, 3531209, 3531803, 3532009, 3532405, 3533403, 3536505,
                 3536802, 3537107, 3538204, 3538600, 3545803, 3548005, 3551603,
                 3552106, 3552403, 3554953, 3556206, 3556354, 3556503, 3556701]

df_dep_saude = df[df['codigo_ibge'].isin(cod_dep_saude)]


dfsp = df[df['codigo_ibge'] < 3600000]


dfcps = dfcps[['datahora', 'casos_novos', 'obitos_novos']]
dfcps.columns = ['date', 'newCases', 'newDeaths']


dfrmc = dfrmc[['datahora', 'casos_novos', 'obitos_novos']]
dfrmc.columns = ['date', 'newCases', 'newDeaths']


df_dep_saude = df_dep_saude[['datahora', 'casos_novos', 'obitos_novos']]
df_dep_saude.columns = ['date', 'newCases', 'newDeaths']


dfsp = dfsp[['datahora', 'casos_novos', 'obitos_novos']]
dfsp.columns = ['date', 'newCases', 'newDeaths']



dfcps['date'] = pd.to_datetime(dfcps['date'], format="%Y/%m/%d")

dfrmc['date'] = pd.to_datetime(dfrmc['date'], format="%Y/%m/%d")

df_dep_saude['date'] = pd.to_datetime(df_dep_saude['date'], format="%Y/%m/%d")

dfsp['date'] = pd.to_datetime(dfsp['date'], format="%Y/%m/%d")



dfcps_grouped = dfcps.groupby(by = "date", sort=True).sum().reset_index(drop=False)

dfrmc_grouped = dfrmc.groupby(by = "date", sort=True).sum().reset_index(drop=False)

df_ds_grouped = df_dep_saude.groupby(by = "date", sort=True).sum().reset_index(drop=False)

dfsp_grouped = dfsp.groupby(by = "date", sort=True).sum().reset_index(drop=False)
dfsp_grouped.tail()



dfcps_gweek = dfcps_grouped.groupby(pd.Grouper(key = 'date', freq = 'W-SAT')).sum().reset_index().sort_values('date')

dfrmc_gweek = dfrmc_grouped.groupby(pd.Grouper(key = 'date', freq = 'W-SAT')).sum().reset_index().sort_values('date')

df_ds_gweek = df_ds_grouped.groupby(pd.Grouper(key = 'date', freq = 'W-SAT')).sum().reset_index().sort_values('date')
df_ds_gweek



todays_date = pd.to_datetime("today")
todays_date = pd.to_datetime(todays_date.strftime(format="%d/%m/%Y"), format="%d/%m/%Y")



last_obs = df_ds_gweek[-1:]['date']
last_obs_index = last_obs.index
last_obs = last_obs.item()

if last_obs > todays_date:
    df_ds_gweek.drop(last_obs_index, axis=0, inplace=True)
    dfrmc_gweek.drop(last_obs_index, axis=0, inplace=True)
    dfcps_gweek.drop(last_obs_index, axis=0, inplace=True)



df_ds_gweek['level'] = 'DRS'
dfrmc_gweek['level'] = 'RMC'
dfcps_gweek['level'] = 'Campinas'



dff = df_ds_gweek.append(dfrmc_gweek.append(dfcps_gweek, ignore_index=True), ignore_index=True)



dff_casos = dff.loc[:, ['date', 'level', 'newCases']]
dff_obitos = dff.loc[:, ['date', 'level', 'newDeaths']]
del dff



pltblue = '#0072b2'
pltred = '#d55e00'
pltgreen = '#009e74'


# GRÁFICO NOVOS CASOS
fig = px.bar(dff_casos, x='date', y='newCases', color='level', text='newCases',
             title='<i><b>CURVA EPIDEMIOLÓGICA<br>OBSERVATÓRIO PUC-CAMPINAS | NOVOS CASOS</b></i>',
             color_discrete_map={'DRS': pltred, 'RMC': pltgreen, 'Campinas': pltblue})

fig.update_layout(
    margin={'t': 117},
    xaxis={
        'title': {'text': ''},
        'tickfont': {'size': 22},
        'tickformat': '%m/%Y',
        'ticks': 'outside',
        'ticklen': 10
    },
    yaxis={
        'title': {
            'text': '<b>NOVOS CASOS POR SEMANA DE NOTIFICAÇÃO</b>',
            'font':{'size': 20},
            'standoff': 0
        },
        'tickfont': {'size': 20}
    },
    legend = {
        'orientation': "h",
        'yanchor': "bottom",
        'y': 1,
        'xanchor': "right",
        'x': 1,
        'title': '',
        'font': {'size': 32}
    },
    title={
        'y':0.9549,
        'x':0.109,
        'xanchor': 'left',
        'yanchor': 'top',
        'font': {
            'size': 40
        }
    }
)

fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/n1cholas-rnlpr/Epidemiology_Curves_COVID_GreaterCampinas/master/logo_observatorio_pucc.png",
        xref="paper", yref="paper",
        x=0.061, y=1.0054,
        sizex=0.12, sizey=0.12,
        xanchor="right", yanchor="bottom"
    )
)

fig.write_image('latest_casos_curva.png', width=1920, height=1080, scale=3)
fig.write_image(f"graph_history\\casos_{todays_date.strftime('%d_%m_%y')}.png", width=1920, height=1080, scale=3)




# GRÁFICO NOVOS ÓBITOS
fig = px.bar(dff_obitos, x='date', y='newDeaths', color='level', text='newDeaths',
             title='<i><b>CURVA EPIDEMIOLÓGICA<br>OBSERVATÓRIO PUC-CAMPINAS | NOVOS OBITOS</b></i>',
             color_discrete_map={'DRS': pltred, 'RMC': pltgreen, 'Campinas': pltblue})

fig.update_layout(
    margin={'t': 117},
    xaxis={
        'title': {'text': ''},
        'tickfont': {'size': 22},
        'tickformat': '%m/%Y',
        'ticks': 'outside',
        'ticklen': 10
    },
    yaxis={
        'title': {
            'text': '<b>NOVOS ÓBITOS POR SEMANA DE NOTIFICAÇÃO</b>',
            'font':{'size': 20},
            'standoff': 0
        },
        'tickfont': {'size': 20}
    },
    legend = {
        'orientation': "h",
        'yanchor': "bottom",
        'y': 1,
        'xanchor': "right",
        'x': 1,
        'title': '',
        'font': {'size': 32}
    },
    title={
        'y':0.9549,
        'x':0.109,
        'xanchor': 'left',
        'yanchor': 'top',
        'font': {
            'size': 40
        }
    }
)

fig.add_layout_image(
    dict(
        source="https://raw.githubusercontent.com/n1cholas-rnlpr/Epidemiology_Curves_COVID_GreaterCampinas/master/logo_observatorio_pucc.png",
        xref="paper", yref="paper",
        x=0.061, y=1.0054,
        sizex=0.12, sizey=0.12,
        xanchor="right", yanchor="bottom"
    )
)

fig.write_image('latest_obitos_curva.png', width=1920, height=1080, scale=3)
fig.write_image(f"graph_history\\obitos_{todays_date.strftime('%d_%m_%y')}.png", width=1920, height=1080, scale=3)


print('Done.')