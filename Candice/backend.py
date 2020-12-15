import io

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_table

import pandas as pd 
import plotly.express as px
import urllib

df_csv =  pd.read_csv('discursos_final.csv')

def create_layout(app):
    # Actual layout of the app
    return html.Div(
        className="row",
        style={"max-width": "100%", "font-size": "1.5rem", "padding": "0px 0px"},
        children=[
            # Header
            html.Div(
                className="row header",
                id="app-header",
                style={"background-color": "#5e9ea0"}, 
                children=[
                    html.H3("Candice",id="app-title"),
                    html.A(href='https://github.com/Tatianafp/Candice_MT_2020.1/', children=[
                        html.Img(
                            src=app.get_asset_url("github-logo.png"),
                            className="logo",
                            id="logo",
                        ),
                    ]),
                ]
            ),
            
            # Homepage
            html.Div(
                className="row background",
                id="homepage",
                style={"padding": "15px",
                       "display": "grid",
                       "grid-template-columns": "auto 400px",
                       "height": "100vh"
                       },
                children=[
                    html.Div(
                        style={"height": "100%"},
                        children=[
                            # menu com os controles
                            html.Div(
                                className="row background",
                                id="menu",
                                children=[
                                    # controle/botões/menu da página de exploração
                                    html.Div(
                                        id="explore-data",
                                        style={"display": "grid",
                                               "grid-template-columns": "80% 20%",
                                               "margin-bottom":"10px",
                                               },
                                        children=[
                                            # controles referentes ao conjunto de dados
                                            html.Div(
                                                style={"display": "grid",
                                                       "grid-template-columns": "50% 50%",
                                                       },
                                                children=[
                                                    # seleção do dataset
                                                    html.Div(
                                                        style={
                                                            "display": "grid", "grid-template-columns": "minmax(150px, auto) 27vh"},
                                                        children=[
                                                            html.Label(
                                                                style={
                                                                    "display": "grid",
                                                                    "place-items": "center start"
                                                                },
                                                                children=[
                                                                    "Select a technique: "]
                                                            ),
                                                            dcc.Dropdown(
                                                                id="dropdown-dataset",
                                                                searchable=False,
                                                                clearable=False,
                                                                options=[
                                                                    {
                                                                        "label": "UMAP",
                                                                        "value": "UMAP",
                                                                    },
                                                                    {
                                                                        "label": "t-SNE",
                                                                        "value": "t-SNE",
                                                                    },                                                                    
                                                                ],
                                                                placeholder="Select a dataset",
                                                                value="UMAP",
                                                            )
                                                        ]),
                                                    # seleção do ano do dataset, caso tenha essa opção
                                                    html.Div(
                                                        id="segmentos-controls",
                                                        style={"display": "grid","grid-template-columns": "minmax(125px, auto) 27vh"},
                                                        children=[
                                                            html.Label(
                                                                style={"display": "grid", "place-items": "center"}, children=["Select a label: "]),
                                                            dcc.Dropdown(
                                                                id="dropdown-segmentos",
                                                                searchable=False,
                                                                clearable=False,
                                                                options=[
                                                                    {
                                                                        "label": "Presidente da época",
                                                                        "value": "presidente",
                                                                    },
                                                                    {
                                                                        "label": "Partido do parlamentar",
                                                                        "value": "SiglaPartidoParlamentar",
                                                                    },
                                                                    {
                                                                        "label": "UF do parlamentar",
                                                                        "value": "UfParlamentar",
                                                                    },
                                                                    {
                                                                        "label": "Sexo do parlamentar",
                                                                        "value": "SexoParlamentar",
                                                                    },
                                                                    {
                                                                        "label": "Parlamentar",
                                                                        "value": "NomeParlamentar",
                                                                    },
                                                                ],
                                                                placeholder="Select a year",
                                                                value="presidente",
                                                            ),
                                                        ],
                                                    ),
                                                ],                                               
                                            ),
                                        ]
                                    ),                                    
                                ],
                            ),
                            # gráfico/ aréa destinada às visualizações
                            dcc.Graph(
                                id="graph-3d-plot-tsne", style={"height": "83vh", "margin-bottom":"0px", "padding": "0px !important"})
                        ],
                    ),
                    # telas que mostram informações extras sob demanda
                    html.Div(
                        id="control-tabs",
                        style={"height": "89vh", "margin-bottom":"0px", "padding": "0px !important"},
                        children=[
                            dcc.Tabs(id='tabs', value='data', children=[
                                # guia referente a breve descrição do conjunto de dados presente no layout
                                dcc.Tab(
                                    label='Discurso',
                                    value='data',
                                    children=html.Div(className='control-tab', style={"padding": "5px"}, children=[
                                        html.Div(id="tab-discurso"),
                                    ]),
                                ),
                                # guia referente às informações do ponto que foi clicado por último
                                dcc.Tab(
                                    label='Parlamentar',
                                    value='point',
                                    children=html.Div(className='control-tab', style={"padding": "5px"}, children=[
                                        html.Div(id="tab-parlamentar"),
                                    ]),
                                ),

                                # guia referente às informações do ponto que foi clicado por último
                                dcc.Tab(
                                    label='Pronunciamento',
                                    value='pronun',
                                    children=html.Div(className='control-tab', style={"padding": "5px"}, children=[
                                        html.Div(id="tab-pronunciamento"),
                                    ]),
                                ),
                                
                            ])
                        ]
                    ),
                ],
            ),


        ],
    )


def demo_callbacks(app):
    def generate_figure_TSNE(df, mp, label):
        if mp == 'UMAP':
            figure = px.scatter(df, x='x_umap', y='y_umap', color= label,
                                color_discrete_sequence=px.colors.qualitative.Pastel)
        elif mp == 't-SNE':
            figure = px.scatter(df, x='x_tsne', y='y_tsne', color= label, 
                                color_discrete_sequence=px.colors.qualitative.Pastel)

        figure.update_traces(marker=dict(line=dict(width=1, color='white')),)

        figure.update_layout(legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1,
            title=dict(text="Legenda", font=dict(
                family="Arial", size=22), side="top"),
            valign="top", 
            itemclick="toggleothers"
        ),
            margin=dict(l=40, r=40, t=50, b=40))

        return figure

    @app.callback(
        Output("graph-3d-plot-tsne", "figure"),
        [
            Input("dropdown-dataset", "value"),
            Input("dropdown-segmentos", "value"),
        ],
    )
    def display_scatter_plot(mp, label):
        df = df_csv

        figure = generate_figure_TSNE(df,mp,label)
        return (figure)

    @app.callback(
        [   
            Output("tab-discurso", "children"),
            Output("tab-parlamentar", "children"),
            Output("tab-pronunciamento", "children"),
        ],
        [
            Input("graph-3d-plot-tsne", "clickData"),
            
        ],
        [
            State("dropdown-dataset", "value"),
        ]
    )
    def explore_data(clickData, mp):      
        df = df_csv
        
        discurso_content = []
        contents = []
        pronun_content = []

        discurso_content.append(html.Div(
            style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
            children=[html.H6("Clique em um ponto para visualizar o discurso selecionado.")]
        ))

        contents.append(html.Div(
            style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
            children=[html.H6("Clique em um ponto para visualizar os dados referentes ao parlamentar que fez o discurso selecionado.")]
        ))

        pronun_content.append(html.Div(
            style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
            children=[html.H6("Clique em um ponto para visualizar os dados referentes ao pronunciamento.")]
        ))

        

        if clickData:

            XY = {}
            XY['x'] = clickData["points"][0]['x']
            XY['y'] = clickData["points"][0]['y']
            #mp = "UMAP"

            XY2 = []
            XY2.append(XY['x'])
            
            #XY2.append(XY['y'])
            if mp == 'UMAP':
                achar_indice = df[df['x_umap'].isin(XY2)].index
                                
            elif mp == 't-SNE':
                achar_indice = df[df['x_tsne'].isin(XY2)].index

            else: 
                achar_indice = df[df['x_umap'].isin(XY2)].index

            # Retrieve the index of the point clicked, given it is present in the set
            t = 1
            if t == 1:

                
                #label = df['label'][achar_indice]
                contents = []
                discurso_content = []
                pronun_content = []

                #tab discurso

                discurso = df['Discurso'][achar_indice]
                discurso_content.append(html.P(discurso))

                #tab parlamentar

                nome = df['NomeParlamentar'][achar_indice]
                nomeCompleto = df['NomeCompletoParlamentar'][achar_indice]
                sexo = df['SexoParlamentar'][achar_indice]
                siglaPartido = df['SiglaPartidoParlamentar'][achar_indice]
                uf = df['UfParlamentar'][achar_indice]

                contents.append(
                    html.Ul(
                        style={"list-style-type": "none","margin-bottom": "1px"},
                        className="list",
                        children=[
                            (html.Li("Nome: " + nome)),
                            (html.Li("Nome completo: " + nomeCompleto)),
                            (html.Li("Sexo: " + sexo)),
                            (html.Li("Sigla do partido: " + siglaPartido)),
                            (html.Li("UF: " + uf)),                           
                        ]
                    )
                )

                #tab pronunciamento

                resumo = df['TextoResumo'][achar_indice]
                data = df['DataPronunciamento'][achar_indice]
                presidente = df['presidente'][achar_indice]
                
                pronun_content.append(
                    html.Ul(
                        style={"list-style-type": "none","margin-bottom": "1px"},
                        className="list",
                        children=[
                            (html.Li("Resumo: " + resumo)),
                            (html.Li("Data: " + data)),
                            (html.Li("Presidente da época: " + presidente)),
                                                    
                        ]
                    )
                )

            else:
                contents = []
                discurso_content = []
                pronun_content = []
                
                discurso_content.append(html.Div(
                    style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
                    children=[html.H6("Clique em um ponto para visualizar os dados referentes ao discurso selecionado.")]
                ))

                contents.append(html.Div(
                    style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
                    children=[html.H6("Clique em um ponto para visualizar os dados referentes ao parlamentar que fez o discurso selecionado.")]
                ))

                pronun_content.append(html.Div(
                    style={"width": "100%", "height": "80vh","display": "grid", "place-items": "center","text-align": "center"},
                    children=[html.H6("Clique em um ponto para visualizar os dados referentes ao pronunciamento.")]
                ))

        return [discurso_content,contents, pronun_content]

'''
    @app.callback(
        [
            Output("about-us", "style")   
        ],
        [
            Input("about-button", "n_clicks")
        ]
    )
    def display_about(clicks):
        if clicks is None:
            clicks = 0
        if (clicks % 2) == 1:
            clicks += 1
            return [{"display": "grid"}]
        else:
            clicks += 1 

        return [{"display": "none"}]
'''



