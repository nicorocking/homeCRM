from msilib.schema import Error
from xml.dom.pulldom import ErrorHandler
import plotly.express as px
import plotly.io as pio
import pandas as pd
import dash_bootstrap_components as dbc
import mysql.connector
from dash import dcc, html, dash_table

sqlcon = mysql.connector.connect(
    host='localhost',
    database='',
    user='root',
    password=''
)

pio.templates.default = "plotly_dark"

def buscar(n_clicks, n_submit, cliente):
    if cliente != '' and cliente is not None:
        try:
            datacliente = f'''
                SELECT DISTINCT * FROM cali_g WHERE Persona_Id LIKE '%{cliente}'
            '''
            cursor = sqlcon.cursor(buffered=True)
            cursor.execute(datacliente)
            record = cursor.fetchone()
            consulta = pd.read_sql(datacliente, sqlcon)
            CG = record[5]
            usoCG_valor = pd.DataFrame(consulta['Uso_Calificacion_Global'])
            CG_valor = consulta['Calificacion_Global']
            # z = usoCG_valor.transpose()
            # productos = ['Tarjetas', 'Tarjetas', 'Préstamos', 'Préstamos', 'Acuerdo', 'Acuerdo'],['Calificacion_TC', 'Uso_Calificacion_TC', 'Calificacion_Prestamo', 'Uso_Calificacion_Prestamo', 'Calificacion_Acuerdo', 'Uso_Calificacion_Acuerdo']
            # monto = ['Calificacion_TC', 'Uso_Calificacion_TC', 'Calificacion_Prestamo', 'Uso_Calificacion_Prestamo', 'Calificacion_Acuerdo', 'Uso_Calificacion_Acuerdo']
            usoCG = px.pie(consulta, values='Uso_Calificacion_Global')
            usoCG_TJ = px.bar(consulta, x=[''], y=['Uso_Calificacion_TC'], labels={'x': 'Tarjetas', 'value': 'Monto en Uso'})
            usoCG_ACC = px.bar(consulta, x=[''], y=['Uso_Calificacion_Acuerdo', 'Uso_Calificacion_TC'], labels={'x': 'Total en Uso', 'value': 'Monto'})
            return dbc.Container([
                dbc.Row([
                    dbc.Col([
                        html.H1(f'Buscaste al cliente {cliente}')
                    ], width=10),
                    dbc.Col([
                        html.A(
                            html.Img(
                                src='assets/whatsapp.png', width='80', height='80', title='Enviar un mensaje', style={'vertical-align': 'top', 'float': 'right'}
                            ),
                            href='https://api.whatsapp.com/send?phone=^{tel}&text=Hola! Tenés un préstamo a tasa preferencial y me gustaría contarte cómo aprovecharlo.', target='_blank'
                        )
                    ], width=2),
                ]),
                dbc.Row([html.H3(f'El cliente tiene una calificación global de ${CG}')]),
                html.Br(),
                dbc.Alert([
                    html.I(className="bi bi-info-circle-fill me-2"),
                    'Este cliente está incluido en la acción comercial "Activación de Clientes"',
                ], color="info", className="d-flex align-items-center"),
                dbc.Alert([
                    html.I(className="bi bi-check-circle-fill me-2"),
                    'Podés ofrecerle tasa preferencial para préstamo personal',
                ], color="success", className="d-flex align-items-center"),
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='usoCG', figure=usoCG, className='one columns')], className='one columns'),
                        dbc.Col([
                            dcc.Graph(id='CG_TJ', figure=usoCG_TJ, className='one columns')], className='one columns'),
                        dbc.Col([
                            dcc.Graph(id='CG_ACC', figure=usoCG_ACC, className='one columns')], className='one columns')
                        ], className='three columns'),
                ]),
                html.Div([
                    dbc.Container([
                        dash_table.DataTable(
                            data = consulta.to_dict('records'),
                            columns=[{'id': c, 'name': c} for c in consulta.columns[3:8]],

                            style_header={
                                'backgroundColor': 'rgb(30, 30, 30)',
                                'color': 'white'
                            },
                            style_data={
                                'backgroundColor': 'rgb(50, 50, 50)',
                                'color': 'white'
                            }
                        )
                    ])
                ], className='four columns')
            ])
        except ValueError:
            return ErrorHandler('Por favor, ingresá un documento válido')
    else:
        return 'No buscaste clientes'
