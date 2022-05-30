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

app.layout = html.Div([
    get_markdown('markdowns/headnotes.md'),
    get_markdown('markdowns/table.md'),
    
    dash_table.DataTable(
        id="data_table",
        data=repo.get_table(),
        columns=[
            {"name": i, "id": i} for i in  ['alim_nom_eng','Carbohydrate (g/100g)','Fat (g/100g)','Protein (g/100g)']],
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
    
    values,names,title = repo.get_calorie_info(selected_row_id)
    
    fig = px.pie(values=values, names=names, title=title)
    return fig

@app.callback(
    Output("nutrient_composition_graph", "figure"),
    Input("data_table",'selected_rows'))
def generate_nutrient_chart(selected_row_id):
    
    data_frame,path,values = repo.get_nutrient_composition(selected_row_id)
    print(values)
    fig = px.sunburst(data_frame, path=path, values=values)
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))

    return fig

# @app.callback(
#     Output("macros_bar_chart", "figure"),
#     Input("data_table",'selected_rows'),
#     #Input("food_amount_slider","value")
#     )
# def generate_macros_bar_chart(selected_row_id,food_amount_value):
#     pass
# @app.callback(
#     Output("top_foods_by_nutrient_chart", "figure"),
#    # Input("nutrient_picker",'value/id')
#    )
# def generate_top_foods_by_nutrient(selected_row_id):
#     pass
# @app.callback(
#     Output("food_category_nutrient_plot", "figure"),
#    # Input("nutrient_picker_2",'value/id')
#    )
# def generate_food_category_nutrient_plot(selected_row_id):
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)



