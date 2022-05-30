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
        page_size=25,
        filter_action="native",
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },),
    get_markdown('markdowns/calorie_chart.md'), 
    dcc.Graph(id="calorie_graph"),
    get_markdown('markdowns/nutrient_composition.md'),
    dcc.Graph(id="nutrient_composition_graph"),
    get_markdown('markdowns/top_nutrients.md'),
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
    
    get_markdown('markdowns/macros_filled.md'),
    dcc.Input(
            id="input_mass",
            type="number",
            placeholder="input type {}".format("number"),
        ),
    dcc.Graph(id="rda_bar_chart"),
    get_markdown('markdowns/footnotes.md')
    ])
    

@app.callback(
    Output("calorie_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_calorie_chart(selected_row_id):
    
    values,names,title = repo.get_calorie_info(selected_row_id)
    
    fig = px.pie(values=values, names=names, title=title, height=800)
    return fig

@app.callback(
    Output("nutrient_composition_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_nutrient_chart(selected_row_id):
    
    data_frame,path,values = repo.get_nutrient_composition(selected_row_id)
    print(values)
    fig = px.sunburst(data_frame, path=path, values=values, height=800)
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    return fig

# @app.callback(
#     Output("macros_bar_chart", "figure"),
#     Input("data_table",'selected_rows'),
#     #Input("food_amount_slider","value")
#     )
# def generate_macros_bar_chart(selected_row_id,food_amount_value):
#     pass
@app.callback(
    Output("nutrient_corelation_scatter", "figure"),
    Input("x-dropdown",'value'),
    Input('y-dropdown','value'),
    Input('z-dropdown','value')
   )
def generate_nutrient_corelation_scatter(x_column,y_column, z_column):
    if z_column=="None":
        #2d plot
        return px.scatter(repo.df,x=x_column,y=y_column,hover_name="Name",symbol='alim_grp_nom_eng')
    else:
        #3d plot
        return px.scatter_3d(repo.df,x=x_column,y=y_column,z=z_column,hover_name="Name",symbol='alim_grp_nom_eng')
    
@app.callback(
   Output("nutrient_corelation_grouped_scatter", "figure"),
    Input("x-dropdown_2",'value'),
    Input('y-dropdown_2','value'),
    Input('z-dropdown_2','value')
   )
def generate_food_category_nutrient_plot(x_column,y_column, z_column):
    df = repo.get_category_standardized_df()
   # print(df.head())
    if z_column=="None":
        #2d plot
        return px.scatter(df,x=x_column,y=y_column,hover_name=df.index)
    else:
        #3d plot
        return px.scatter_3d(df,x=x_column,y=y_column,z=z_column,hover_name=df.index)

@app.callback(
    Output("rda_bar_chart", "figure"),
    Input("data_table",'selected_rows'))
def generate_bar_chart(selected_row_id):
    rda_df = repo.get_rda_chart(selected_row_id)
    return px.bar(rda_df,x='nutrient',y='value')


if __name__ == '__main__':
    app.run_server(debug=True)



