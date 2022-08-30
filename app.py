# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from funciones import buscar
from datetime import date, timedelta
from xml.dom.pulldom import ErrorHandler

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO, dbc.icons.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#343a40"
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

sidebar = html.Div([
    html.H2("COPER", className="display-4"),
    html.Hr(),
    html.P("Acá podés buscar un cliente:", className="lead"),
    dbc.Container([
        dbc.Row([
            dbc.Input(className='form-control mb-5', id='cliente_id', type='text', inputMode='numeric', valid=True, invalid=True, placeholder='Ingresá el documento', autoFocus=True, autoComplete='on', minLength=6, maxLength=11, pattern='^[0-9]{6,11}$', required=True, style={'width': '13rem'}),
            html.Button(html.Img(src='assets\search.svg'), className='btn btn-primary mb-5', id='btBuscar', style={'width': '3rem'}),
        ], className='form-group'),
        dbc.Row([
            dbc.Textarea(className='mb-1', size='md', placeholder='Cargá acá la próxima gestión para este cliente', rows=3, cols=7, style={'width': '16rem', "background-color": "white", 'text-color': 'black'}),
        ]),
        dbc.Row([
            dcc.DatePickerSingle(
                id='my-date-picker-range',
                min_date_allowed=date.today() + timedelta(days=1),
                max_date_allowed=date.today() + timedelta(days=90),
                initial_visible_month=date.today(),
                month_format='DD MMM YYYY',
                display_format='DD MMM YYYY',
                placeholder='Fecha'
                ),
            html.Div(id='output-container-date-picker-range', style={'align': 'right', 'justify': 'end', 'font-size': '8', 'background-color': 'black', 'text-color': 'white'}),
            html.Button('Agendar', className='btn btn-secondary mb-5'),
        ], className='form-inline'),
    ]),
    dbc.Nav(
        [
        dbc.NavLink("Top 10", href="/top_10", active="exact"),
        dbc.NavLink("Préstamos", href="/page-1", active="exact"),
        dbc.NavLink("Tarjetas", href="/page-2", active="exact"),
        dbc.NavLink("Seguros", href="/page-3", active="exact"),
        dbc.NavLink("Próximos a inactivarse", href="/page-4", active="exact", className='mb-2'),
        dbc.NavLink("Agenda", href="/page-5", active="exact"),
        ],
        vertical=True,
        pills=True,
    ),
], style=SIDEBAR_STYLE)

content = html.Div([

],id="page-content", style=CONTENT_STYLE)


app.layout = html.Div([
        dcc.Location(id="url"), 
        sidebar,
        content,
        html.Div([
            # dcc.Graph()
        ])
        


])


@app.callback(
    Output("page-content", "children"),
    Input("btBuscar", "n_clicks"),
    Input("cliente_id", "n_submit"),
    State("cliente_id", "value")
)
def update_layout(n_clicks, n_submit, cliente):
    # if cliente is not None:
    actualizar = buscar(n_clicks, n_submit, cliente)
    return actualizar
    # else:
    #     raise ErrorHandler('Por favor, ingresá un documento válido')
        


        # return dbc.Jumbotron(
        #     [
        #     html.H1("404: Not found", className="text-danger"),
        #     html.Hr(),
        #     html.P(f"El cliente {cliente} was not recognised..."),
        #     ]
        # )
    # # def show_cliente(df):
    # #     return df.loc[df['Persona_Id'] == 'cliente']
    # return show_cliente(df)
    # return dbc.Jumbotron(
    #     [
    #         html.H1("404: Not found", className="text-danger"),
    #         html.Hr(),
    #         html.P(f"El cliente {cliente} was not recognised..."),
    #         ]
    # )


# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname == "/top_10":
#         def generate_table(df, max_rows=10):
#             return html.Table([
#                 html.Thead(
#                     html.Tr([html.Th(col) for col in df.columns])
#                 ),
#                 html.Tbody([
#                     html.Tr([
#                         html.Td(df.iloc[i][col]) for col in df.columns
#                     ]) for i in range(min(len(df), max_rows))
#                 ])
#             ])
#         return html.H1('Top 10'), html.P(generate_table(df)),
#     elif pathname == "/page-1":
#         return html.P("This is the content of page 1. Yay!")
#     elif pathname == "/page-2":
#         return html.P("Oh cool, this is page 2!")
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )

# colors = {
#     'background': '#111111',
#     'text': '#7FDBFF'
# }

if __name__ == '__main__':
    app.run_server(debug=True, port='3000')