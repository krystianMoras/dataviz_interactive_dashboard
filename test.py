from dash import dcc
from dash import Dash, dcc, html, Input, Output
from dash import html
from dash import Dash, dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


df = pd.read_excel("Table Ciqual 2020_ENG_2020 07 07.xls",decimal=",",na_values=["-","traces"]).fillna(0)
df = df.replace({'< ':'',",":'.'},regex=True)
df = df.apply(pd.to_numeric,errors="ignore")

print(df.keys())
# print(df.head())

level_1 = ['Water (g/100g)',
       'Protein (g/100g)',
       'Carbohydrate (g/100g)', 'Fat (g/100g)','Ash (g/100g)', 'Alcohol (g/100g)','Organic acids (g/100g)']
carbos = ['Sugars (g/100g)','Starch (g/100g)','Fibres (g/100g)', 'Polyols (g/100g)']
sugars = ['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)',
       'lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']
fats = ['FA saturated (g/100g)', 'FA mono (g/100g)', 'FA poly (g/100g)']
omega9 = ['FA 18:1 n-9 cis (g/100g)']
omega6 = ['FA 18:2 9c,12c (n-6) (g/100g)','FA 20:4 5c,8c,11c,14c (n-6) (g/100g)']
omega3 = ['FA 18:3 c9,c12,c15 (n-3) (g/100g)','FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)']
polyunsaturated_fats = ['omega9','omega6', 'omega3']




df['other sugars'] = df['Sugars (g/100g)'] - df[['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']].sum(axis=1)

omega9 = ['FA 18:1 n-9 cis (g/100g)']
omega6 = ['FA 18:2 9c,12c (n-6) (g/100g)','FA 20:4 5c,8c,11c,14c (n-6) (g/100g)']
omega3 = ['FA 18:3 c9,c12,c15 (n-3) (g/100g)','FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)']
sugars = ['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)',
       'lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)','other sugars']

parents_0 = ['fats','fats','fats','fats','fats','fats','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','fats','fats','carbohydrates','carbohydrates','carbohydrates','water','protein','ash','alcohol','organic acids']
parents_1 = ['polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','sugars','sugars','sugars','sugars','sugars','sugars','sugars','saturated fats','monounsaturated fats','starch','fibres','polyols',None,None,None,None,None]
parents_2 = ["omega 3","omega 3","omega 3","omega 6","omega 6","omega 9",'fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)','no data/other',None,None,None,None,None,None,None,None,None,None]
parents_3 = ["ala","epa","dha",'linoleic','arachidonic',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

print(len(parents_0),len(parents_1),len(parents_2),len(parents_3))


# parents_0 = ['fats','fats','fats','fats','fats','fats','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','fats','fats','carbohydrates','carbohydrates','carbohydrates','water','protein','ash','alcohol','organic acids']
# parents_1 = ['polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','sugars','sugars','sugars','sugars','sugars','sugars','saturated fats','monounsaturated fats','starch','fibres','polyols',None,None,None,None,None]
# parents_2 = ["omega 3","omega 3","omega 3","omega 6","omega 6","omega 9",'fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)',None,None,None,None,None,None,None,None,None,None]
# parents_3 = ["ala","epa","dha",'linoleic','arachidonic',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]


# df['other sugars'] = df['Sugars (g/100g)'] - df[['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']].sum(axis=1)
# row = df.iloc[0]

# values = row[omega3 + omega6 + omega9 + sugars + ['FA saturated (g/100g)','FA mono (g/100g)','Starch (g/100g)','Fibres (g/100g)','Polyols (g/100g)','Water (g/100g)','Protein (g/100g)','Ash (g/100g)','Alcohol (g/100g)','Organic acids (g/100g)','other sugars']]
# print(values)

# new_df = ['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)',
#         'FA 18:1 n-9 cis (g/100g)','FA 18:2 9c,12c (n-6) (g/100g)','FA 20:4 5c,8c,11c,14c (n-6) (g/100g)','FA 18:3 c9,c12,c15 (n-3) (g/100g)','FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)']
# ['Cholesterol (mg/100g)', 'Salt (g/100g)', 'Calcium (mg/100g)',
#        'Chloride (mg/100g)', 'Copper (mg/100g)', 'Iron (mg/100g)',
#        'Iodine (µg/100g)', 'Magnesium (mg/100g)', 'Manganese (mg/100g)',
#        'Phosphorus (mg/100g)', 'Potassium (mg/100g)', 'Selenium (µg/100g)',
#        'Sodium (mg/100g)', 'Zinc (mg/100g)', 'Retinol (µg/100g)',
#        'Beta-carotene (µg/100g)', 'Vitamin D (µg/100g)', 'Vitamin E (mg/100g)',
#        'Vitamin K1 (µg/100g)', 'Vitamin K2 (µg/100g)', 'Vitamin C (mg/100g)',
#        'Vitamin B1 or Thiamin (mg/100g)', 'Vitamin B2 or Riboflavin (mg/100g)',
#        'Vitamin B3 or Niacin (mg/100g)',
#        'Vitamin B5 or Pantothenic acid (mg/100g)', 'Vitamin B6 (mg/100g)',
#        'Vitamin B9 or Folate (µg/100g)', 'Vitamin B12 (µg/100g)']
# columns_to_drop = ['alim_grp_code', 'alim_ssgrp_code', 'alim_ssssgrp_code',
#                    'alim_grp_nom_eng', 'alim_ssgrp_nom_eng', 'alim_ssssgrp_nom_eng',
#                    'alim_nom_sci', 'Energy, Regulation EU No 1169/2011 (kJ/100g)',
#                    'Energy, N x Jones\' factor, with fibres (kJ/100g)',
#                    'Energy, N x Jones\' factor, with fibres (kcal/100g)',
#                    'Protein, crude, N x 6.25 (g/100g)']
# df = df.drop(columns_to_drop, axis=1)


# # df.drop([])

# df["Protein kcal"] = df['Protein (g/100g)'] * 4
# df["Carbohydrate kcal"] = df["Carbohydrate (g/100g)"] * 4
# df["Fat kcal"] = df['Fat (g/100g)'] * 9
# df["Alcohol kcal"] = df['Alcohol (g/100g)'] * 7
# pieChartDf = df[['alim_nom_eng','Protein kcal','Carbohydrate kcal','Fat kcal','Alcohol kcal']]

# # print(pieChartDf.iloc[:1].to_numpy().transpose())



# new_frame = pd.DataFrame()

# new_frame


