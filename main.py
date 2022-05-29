from dash import dcc
from dash import Dash, dcc, html, Input, Output
from dash import html
from dash import Dash, dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


def get_markdown(filename) -> dcc.Markdown:
    return dcc.Markdown(open(filename).read())

df = pd.read_excel("Table Ciqual 2020_ENG_2020 07 07.xls",decimal=",",na_values=["-","traces"]).fillna(0)
df = df.replace({'< ':'',",":'.'},regex=True)
df = df.apply(pd.to_numeric,errors="ignore")
# print(df)
# print(df.keys())
columns_to_drop = ['alim_grp_code', 'alim_ssgrp_code', 'alim_ssssgrp_code',
                   'alim_grp_nom_eng', 'alim_ssgrp_nom_eng', 'alim_ssssgrp_nom_eng',
                   'alim_nom_sci', 'Energy, Regulation EU No 1169/2011 (kJ/100g)',
                   'Energy, N x Jones\' factor, with fibres (kJ/100g)',
                   'Energy, N x Jones\' factor, with fibres (kcal/100g)',
                   'Protein, crude, N x 6.25 (g/100g)']
df = df.drop(columns_to_drop, axis=1)
# df.drop([])

caloriePieChartDf = pd.DataFrame()
caloriePieChartDf["Protein kcal"] = df['Protein (g/100g)'] * 4
caloriePieChartDf["Carbohydrate kcal"] = df["Carbohydrate (g/100g)"] * 4
caloriePieChartDf["Fat kcal"] = df['Fat (g/100g)'] * 9
caloriePieChartDf["Alcohol kcal"] = df['Alcohol (g/100g)'] * 7


# nutrient_lvl_1 = df[['Water (g/100g)',
#        'Protein (g/100g)',
#        'Carbohydrate (g/100g)', 'Fat (g/100g)','Ash (g/100g)', 'Alcohol (g/100g)']]

df['other sugars'] = df['Sugars (g/100g)'] - df[['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)','lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)']].sum(axis=1)
df['other carbs'] = df['Carbohydrate (g/100g)'] - df[['Sugars (g/100g)','Starch (g/100g)','Fibres (g/100g)', 'Polyols (g/100g)']].sum(axis=1)
df['other fats'] = df['Fat (g/100g)'] - df[['FA saturated (g/100g)', 'FA mono (g/100g)', 'FA poly (g/100g)']].sum(axis=1)

omega9 = ['FA 18:1 n-9 cis (g/100g)']
omega6 = ['FA 18:2 9c,12c (n-6) (g/100g)','FA 20:4 5c,8c,11c,14c (n-6) (g/100g)']
omega3 = ['FA 18:3 c9,c12,c15 (n-3) (g/100g)','FA 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100g)', 'FA 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100g)']
sugars = ['fructose (g/100g)', 'galactose (g/100g)', 'glucose (g/100g)',
       'lactose (g/100g)', 'maltose (g/100g)', 'sucrose (g/100g)','other sugars']

parents_0 = ['fats','fats','fats','fats','fats','fats','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','carbohydrates','fats','fats','carbohydrates','carbohydrates','carbohydrates','water','protein','ash','alcohol','organic acids','carbohydrates','fats']
parents_1 = ['polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','polyunsaturated fats','sugars','sugars','sugars','sugars','sugars','sugars','sugars','saturated fats','monounsaturated fats','starch','fibres','polyols',None,None,None,None,None,'no data/other','no data/other']
parents_2 = ["omega 3","omega 3","omega 3","omega 6","omega 6","omega 9",'fructose', 'galactose', 'glucose','lactose', 'maltose', 'sucrose','no data/other',None,None,None,None,None,None,None,None,None,None,None,None]
parents_3 = ["ala","epa","dha",'linoleic','arachidonic',None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

print(len(parents_0),len(parents_1),len(parents_2),len(parents_3))
app = Dash(__name__)

app.layout = html.Div([
    get_markdown('markdowns/headnotes.md'),
    get_markdown('markdowns/table.md'),
    
    dash_table.DataTable(
        id="data_table",
        data=df.to_dict('records'),
        columns=[
            {"name": i, "id": i} for i in df.columns],
        row_selectable='single'),
    get_markdown('markdowns/calorie_chart.md'), 
    dcc.Graph(id="calorie_graph"),
    get_markdown('markdowns/nutrient_composition.md'),
    dcc.Graph(id="nutrient_composition_graph"),
    get_markdown('markdowns/top_nutrients.md'),
    get_markdown('markdowns/nutrients_categories.md'),
    get_markdown('markdowns/macros_filled.md'),
    get_markdown('markdowns/footnotes.md')
    ])

@app.callback(
    Output("calorie_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_calorie_chart(selected_row_id):
    
    if selected_row_id is None:
        values = caloriePieChartDf.iloc[0].to_numpy().transpose().flatten()
    else:
        values = caloriePieChartDf.iloc[selected_row_id[0]].to_numpy().transpose().flatten()
    print(selected_row_id,values)

    fig = px.pie(values=values, names=['Protein calories','Carbohydrate calories','Fat calories','Alcohol calories'], title=df.iloc[selected_row_id[0]]['alim_nom_eng'])
    return fig

@app.callback(
    Output("nutrient_composition_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_nutrient_chart(selected_row_id):
    if selected_row_id is None:
        row = df.iloc[0]
    else:
        row = df.iloc[selected_row_id[0]]
    values = row[omega3 + omega6 + omega9 + sugars + ['FA saturated (g/100g)','FA mono (g/100g)','Starch (g/100g)','Fibres (g/100g)','Polyols (g/100g)','Water (g/100g)','Protein (g/100g)','Ash (g/100g)','Alcohol (g/100g)','Organic acids (g/100g)','other carbs','other fats']]
    print(values)
    values = values.to_numpy().transpose().flatten()
    nutrient_df = pd.DataFrame(
    dict(values=values, parents_3=parents_3, parents_2=parents_2, parents_1= parents_1,parents_0=parents_0))
    fig = px.sunburst(nutrient_df, path=['parents_0','parents_1', 'parents_2', 'parents_3'], values=values)
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    return fig

if __name__ == '__main__':
    app.run_server()



