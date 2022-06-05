from dash import dcc
from dash import Dash, dcc, html, Input, Output
from dash import html
from dash import Dash, dash_table
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import data_util


def get_markdown(filename) -> dcc.Markdown:
    return dcc.Markdown(open(filename).read())


# df.drop([])


app = Dash(__name__)
server = app.server
repo = data_util.NutrientInfoRepo()
table, columns = repo.get_table()
app.layout = html.Div(
    [
    get_markdown('markdowns/headnotes.md'),
    get_markdown('markdowns/table.md'),
    
    dash_table.DataTable(
        id="data_table",
        data=table,
        columns=[
            {"name": i, "id": i} for i in columns],
        row_selectable='single',
        page_size=15,
        filter_action="native",
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },),
    html.Div(children=[
    dcc.Graph(id="calorie_graph"),
    html.Div(children=[
        html.H1("Composition of food"),
    dcc.Graph(id="nutrient_composition_graph"),
    ])
    
    ],style={'display': 'flex', 'flex-direction': 'row'}),
    
    get_markdown('markdowns/macros_filled.md'),
    dcc.Input(
            id="input_mass",
            type="number",
            placeholder="input type {}".format("number"),
        ),
    dcc.Graph(id="rda_bar_chart"),
    
    get_markdown('markdowns/correlations_nutrients.md'),
    html.Div(children=[
       dcc.Dropdown(options=repo.get_dropdown_options(), value=repo.get_dropdown_options()[0],placeholder="Select X axis", id='x-dropdown'),
        dcc.Dropdown(options=repo.get_dropdown_options(), value=repo.get_dropdown_options()[0],placeholder="Select Y axis", id='y-dropdown'),
        dcc.Dropdown(options=["None"] + repo.get_dropdown_options(),value= "None",placeholder="Select Z axis", id='z-dropdown'),
    ]),
    dcc.Graph(id="nutrient_corelation_scatter"),
    get_markdown('markdowns/nutrients_categories.md'),
    html.Div(children=[
       dcc.Dropdown(options=repo.get_dropdown_options(), value=repo.get_dropdown_options()[0],placeholder="Select X axis", id='x-dropdown_2'),
        dcc.Dropdown(options=repo.get_dropdown_options(), value=repo.get_dropdown_options()[0],placeholder="Select Y axis", id='y-dropdown_2'),
        dcc.Dropdown(options=["None"] + repo.get_dropdown_options(),value= "None",placeholder="Select Z axis", id='z-dropdown_2'),
    ]),
    dcc.Graph(id="nutrient_corelation_grouped_scatter"),
    
    
    get_markdown('markdowns/footnotes.md')
    ])
    

@app.callback(
    Output("calorie_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_calorie_chart(selected_row_id):
    
    values,names,title = repo.get_calorie_info(selected_row_id)
    fig = px.pie(values=values, names=names, title=f"Calories source distribution of {title}", height=600,color=names,color_discrete_map={"Fat kcal":"red","Protein kcal":"green","Carbohydrate kcal":"orange","Alcohol kcal":"purple"})
    return fig

@app.callback(
    Output("nutrient_composition_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_nutrient_chart(selected_row_id):
    
    data_frame,path,values,title = repo.get_nutrient_composition(selected_row_id)
   # print(values)
    #title not visible :-(
    fig = px.sunburst(data_frame, path=path, values=values,width=600,height=600,color='parents_0',color_discrete_map={"fats":"red","protein":"green","carbohydrates":"orange","alcohol":"cyan",'water':"blue"})
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    return fig


@app.callback(
    Output("nutrient_corelation_scatter", "figure"),
    Input("x-dropdown",'value'),
    Input('y-dropdown','value'),
    Input('z-dropdown','value')
   )
def generate_nutrient_corelation_scatter(x_column,y_column, z_column):
    if z_column=="None":
        #2d plot
        return px.scatter(repo.df,x=x_column,y=y_column,hover_name="Name",color='category',symbol='category')
    else:
        #3d plot
        return px.scatter(repo.df,x=x_column,y=y_column,size=z_column,hover_name="Name",color='category',symbol='category')
    
@app.callback(
   Output("nutrient_corelation_grouped_scatter", "figure"),
    Input("x-dropdown_2",'value'),
    Input('y-dropdown_2','value'),
    Input('z-dropdown_2','value')
   )
def generate_food_category_nutrient_plot(x_column,y_column, z_column):
    df = repo.get_category_standardized_df()
    if z_column=="None":
        #2d plot
        return px.scatter(df,x=x_column,y=y_column,hover_name=df.index,color=df.index,symbol=df.index)
    else:
        #3d plot
        return px.scatter(df,x=x_column,y=y_column,size=z_column,hover_name=df.index,color=df.index,symbol=df.index)

@app.callback(
    Output("rda_bar_chart", "figure"),
    Input("data_table",'selected_rows'),
    Input('input_mass',"value"))
def generate_bar_chart(selected_row_id,value):
    print(value)
    value = 100 if value is None else value
    rda_df = repo.get_rda_chart(selected_row_id,value/100)
    fig =  px.bar(rda_df,x='nutrient',y='value')
    max_range = 100
    for value in rda_df.value:
        max_range = value + 10 if value > max_range else max_range
    fig.update_layout(
   xaxis={'title': 'Nutrients'},
   yaxis= {'title': 'Recommended intake (%)', 'range': [1, max_range]})
    fig.add_hline(y=100, line_width=3, line_dash="dash", line_color="green")
    return fig


if __name__ == '__main__':
    app.run_server()



