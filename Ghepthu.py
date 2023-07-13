import dash
from dash import html
from dash import dcc
import plotly.express as px
import numpy as np
import pandas as pd
import os
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


WUR = pd.read_csv(os.path.join('WUR.csv'), delimiter=';', index_col=False)
dropdown_options = [{'label': region, 'value': region} for region in WUR['region'].unique()]
# Replace commas with empty string in 'international_students' column
WUR['international_students'] = WUR['international_students'].str.replace(',', '')
# Replace commas with empty string in 'international_students' column
WUR['faculty_count'] = WUR['faculty_count'].str.replace(',', '')
WUR['international_students'] = pd.to_numeric(WUR['international_students'], errors='coerce')
WUR['faculty_count'] = pd.to_numeric(WUR['international_students'], errors='coerce')
blue_accent_color_1 = "#e3efff"
green_color = "#CCFF99"
near_dark = "#003399"
dark_green = "#6F7B50"
selected_region = WUR['region'].unique()[0]
# Define the layout of the app
app.layout = html.Div(
    id="main-container",
    style={
        'background-image': 'url("https://www.tibco.com/sites/tibco/files/media_entity/2020-05/r-analytics.svg")',
        'background-size': 'contain',
        'background-repeat': 'no-repeat',
        'background-position': 'center',
        'height': '100vh'  # set the height to 100% of the viewport height
    },
    children=[
        html.Div([
            dbc.Navbar(
                [
                    dbc.Container([
                        dbc.Nav(
                            [
                                dbc.NavItem(dbc.NavLink("Bar Chart & Scatter Plot", href="#", id="bar-chart-link")),
                                dbc.NavItem(dbc.NavLink("Pie Chart & Box Plot", href="#", id="pie-chart-link")),
                                dcc.Dropdown(
                                    id="my-dropdown",
                                    options=dropdown_options,
                                    value=selected_region,
                                    style={'width': '160px'}
                                ),
                                
                                dbc.NavItem(dbc.NavLink("Our Datasheet", href="https://docs.google.com/spreadsheets/d/1VtEFT9SMw6ycI8DRby995D0CWscuVwQEzjKTEwhpXtQ/edit?usp=sharing", target="_blank")),
                            ],
                            className="ml-auto",
                            navbar=True,
                        ),
                    ]),
                ],
                color="dark",
                dark=True,
            ),
        ], style={'max-width': '100%', 'border-bottom': '1px solid #ddd'}),
        
        html.Div(
            id="title-container",
            children=[
                html.H3(
                    children=[
                        'The Analysis of',
                        html.Br(),
                        'World University',
                        html.Br(),
                        'Ranking 2017-2022'
                    ],
                    style={
                        'text-align': 'right',
                        'font-size': '50px',
                        'text-transform': 'uppercase',
                        'color': '#222',
                        'letter-spacing': '1px',
                        'font-family': 'Playfair Display, serif',
                        'font-weight': '400',
                        'position': 'absolute',
                        'bottom': '43%',
                        'right': '4%',
                        "textShadow": f"0px 0px 5px {blue_accent_color_1}",
                        "WebkitTextStroke": f"0.5px {blue_accent_color_1}",
                        "margin-right": "10px"
                    }
                )
            ],
            style={"margin-top": "100px"}
        ),
        
        html.Div(id="page-content")
    ]
)

@app.callback(
    dash.dependencies.Output('my-dropdown', 'value'),
    [dash.dependencies.Input('my-dropdown', 'options')]
)
def update_dropdown_value(options):
    return options[0]['value']

@app.callback(
    dash.dependencies.Output("main-container", "style"),
    [dash.dependencies.Input("bar-chart-link", "n_clicks")],
    [dash.dependencies.Input("pie-chart-link", "n_clicks")]
)
def change_background_image(bar_clicks, pie_clicks):
    if bar_clicks or pie_clicks:
        new_background_image = 'url("https://img.freepik.com/free-photo/light-gray-concrete-wall_53876-89532.jpg?w=2000&t=st=1687283934~exp=1687284534~hmac=4b89c932f8a89d49d197a5a71ce1519c246ba6abe1ea0a31c3f9c72cb6047d5a")'
        return {
            'background-image': new_background_image,
            'background-size': 'cover',
            'background-repeat': 'no-repeat',
            'background-position': 'center',
            'height': '100%'
        }
    else:
        return {
            'background-image': 'url("https://www.tibco.com/sites/tibco/files/media_entity/2020-05/r-analytics.svg")',
            'background-size': 'contain',
            'background-repeat': 'no-repeat',
            'background-position': 'center',
            'height': '100vh'
        }

@app.callback(
    dash.dependencies.Output("title-container", "children"),
    [dash.dependencies.Input("bar-chart-link", "n_clicks"),
     dash.dependencies.Input("pie-chart-link", "n_clicks")],
)
def update_title(bar_clicks, pie_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [
            html.H3(
                children=[
                    'The Analysis of',
                    html.Br(),
                    'World University',
                    html.Br(),
                    'Ranking 2017-2022'
                ],
                style={
                    'text-align': 'right',
                    'font-size': '50px',
                    'text-transform': 'uppercase',
                    'color': '#222',
                    'letter-spacing': '1px',
                    'font-family': 'Playfair Display, serif',
                    'font-weight': '400',
                    'position': 'absolute',
                    'bottom': '43%',
                    'right': '4%',
                    "textShadow": f"0px 0px 5px {blue_accent_color_1}",
                    "WebkitTextStroke": f"0.5px {blue_accent_color_1}",
                    "margin-right": "10px"
                }
            )
        ]
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "bar-chart-link" or "pie-chart-link":
            return None

@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("bar-chart-link", "n_clicks"),
     dash.dependencies.Input("pie-chart-link", "n_clicks")],
    [dash.dependencies.State('my-dropdown', 'value'),
     dash.dependencies.State("bar-chart-link", "n_clicks"),
     dash.dependencies.State("pie-chart-link", "n_clicks")]
)
def render_page_content(bar_clicks, pie_clicks, selected_region, bar_link_clicks, pie_link_clicks):
    if pie_clicks is not None and bar_clicks is not None and pie_clicks > bar_clicks:
        bar_clicks = 0
    elif bar_clicks is not None and pie_clicks is not None and bar_clicks > pie_clicks:
        pie_clicks = 0    
    
    if pie_clicks is not None and pie_clicks > 0:
        filtered_data = WUR[WUR['region'] == selected_region]
        Count_country = filtered_data.groupby('country')['university'].count().reset_index(name='count')
        fig = px.pie(Count_country, values='count', names='country', color='country', labels={'country': 'Country', 'count': 'Number of universities'}, title=f'The percentage of the number of universities in each country in {selected_region}')
        fig.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph3 = dcc.Graph(id="my-pie-chart", figure=fig)
        
        # Create a new pie chart next to the old chart
        filtered_data = WUR[WUR['region'] == selected_region]
        Count_Size = filtered_data.groupby('size')['university'].count().reset_index(name='count')
        fig2 = px.pie(Count_Size, values='count', names='size', color='size', labels={'size': 'Size', 'count': 'Number of universities'}, title=f'The percentage of 4 sizes of university in {selected_region}')
        fig2.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph2 = dcc.Graph(id="my-pie-chart-2", figure=fig2)
        
        # Create a new pie chart next to the old chart
        filtered_data = WUR[WUR['region'] == selected_region]
        Count_city = filtered_data.groupby('type')['university'].count().reset_index(name='count')
        fig3 = px.pie(Count_city, values='count', names='type', color='type', labels={'size': 'Size', 'count': 'Number of universities'}, title=f'The percentage of 2 types of university in {selected_region}')
        fig3.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph = dcc.Graph(id="my-pie-chart-3", figure=fig3)
      
        # Create a new pie chart next to the old chart
        filtered_data = WUR[WUR['region'] == selected_region]
        fig4 = px.box(filtered_data, x='country', y='score', color='country', labels={'country': 'Country of University', 'score': 'Score of University'}, title=f'The average score of each country in {selected_region}')
        fig4.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph4 = dcc.Graph(id="my-pie-chart-4", figure=fig4)
        
        # Create a new box  next to the old chart
        filtered_data = WUR[WUR['region'] == selected_region]
        fig5 = px.box(filtered_data, x='country', y='rank_display', color='size', labels={'country': 'Country of University', 'rank_display': 'University Ranking', 'type': 'Type'}, title=f'The average university ranking of each country in {selected_region}')
        fig5.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph5 = dcc.Graph(id="my-pie-chart-5", figure=fig5)
        
        # Create a new pie chart next to the old chart
        filtered_data = WUR[WUR['region'] == selected_region]
        
        fig6 = px.box(filtered_data, x='size', y='score', color='size', facet_col='type', labels={'country': 'Country of University', 'rank_display': 'University Ranking', 'type': 'Type'}, title=f'The average score divided into 4 sizes in {selected_region}')
        fig6.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph6 = dcc.Graph(id="my-pie-chart-6", figure=fig6)
        # Return both pie charts side by side
        return html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph2]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph3]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph4]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "100%",
                    "height": "100%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph5]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "100%",
                    "height": "100%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph6]
            )
            
        ]
    )
    
    # Reset the scatter_clicks variable to 0
      

    elif bar_clicks is not None and bar_clicks > 0:
        filtered_data = WUR[WUR['region'] == selected_region][:10]
        fig = px.bar(filtered_data, x='university', y='student_faculty_ratio', color='size', 
                     labels={'university': 'University', 'student_faculty_ratio': 'Ratio of student faculty', 'size': 'Size'},
                     title=f'The Ratio of student in each faculty of top 10 UNIVERSITY in {selected_region}')
        fig.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph = dcc.Graph(id="my-bar-chart", figure=fig)

        #Create a new bar chart:
        filtered_data = WUR[WUR['region'] == selected_region][:10]
        fig2 = px.bar(filtered_data, x='university', y='international_students', color='city', 
                     labels={'university': 'University', 'international_students': 'International Students', 'city': 'City'},
                     title=f'The number of international student of top 10 UNIVERSITY in {selected_region}')
        fig2.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph2 = dcc.Graph(id="my-bar-chart-2", figure=fig2)
        
        #Create a new bar chart:
        filtered_data = WUR[WUR['region'] == selected_region]
        fig3 = px.treemap(filtered_data, path=['country','university'], values='rank_display', color='score', color_continuous_scale='Rdbu', 
                 hover_data=['score'], color_continuous_midpoint=np.average(WUR['score']))
        fig3.update_traces(textposition='middle center')
        fig3.update_layout(title=f'The summary chart illustrate the information of university in the country of {selected_region}', title_font=dict(size=25, color='black'))  # set the title y position to the top
        fig3.update_layout(
    # set the plot border color to black and width to 2
        plot_bgcolor='white',
        paper_bgcolor='rgba(1,1,1,0.2)',
        font=dict(color='black'),
        title_font=dict(size=19, family='Arial, sans-serif'),
        title_x=0.5,
        title_y=0.9,
    # set the border color and width
        xaxis=dict(showline=True, linewidth=100, linecolor='black', mirror=True),
        yaxis=dict(showline=True, linewidth=100, linecolor='black', mirror=True),
        margin=dict(l=50, r=50, t=90, b=50)
        )
              # đặt giá trị tối đa của trục y

        graph3 = dcc.Graph(id="my-bar-chart-3", figure=fig3) 
        
    # Create a new scatter plot:
        filtered_data = WUR[WUR['region'] == selected_region]
        fig4 = px.scatter(filtered_data, x='country', y='score', color='size', size='score', hover_name='country', labels={'score': 'University Score', 'country': 'Country of University', 'size': 'Size'})
        fig4.update_layout(
            title=f'The average score of university in each country in {selected_region}', title_font=dict(size=19, color='black', family='Arial, sans-serif'),
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph4 = dcc.Graph(id="my-bar-chart-4", figure=fig4)
       
    # Create a new scatter plot:
        filtered_data = WUR[WUR['region'] == selected_region]
        fig5 = px.scatter(filtered_data, x='country', y='rank_display', color='city', size='score', hover_name='country', labels={'rank_display': 'University Ranking', 'country': 'Country of University', 'city': 'City'})
        fig5.update_layout(
            title=f'The rank of university in each country in {selected_region}', title_font=dict(size=19, color='black', family='Arial, sans-serif'),
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph5 = dcc.Graph(id="my-bar-chart-5", figure=fig5)
        
        #Create a new bar chart:
        filtered_data = WUR[WUR['region'] == selected_region]
        grouped_data_1 = filtered_data.groupby('size')['international_students'].mean().reset_index()
        fig6 = px.bar(grouped_data_1, x='size', y='international_students', color='size', 
                     labels={'size': 'Size', 'international_students': 'Average number of international students'},
                     title=f'The Average number of international students by university size in {selected_region}')
        fig6.update_layout(
            plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
            paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
            font=dict(color='black'), # set the font color to black
            title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
            title_x=0.5, # set the title x position to the center
            title_y=0.9, # set the title font size and weight
        )
        graph6 = dcc.Graph(id="my-bar-chart-6", figure=fig6)
        
        #Create a new bar chart:
        filtered_data = WUR[WUR['region'] == selected_region]
        Sum_faculty = filtered_data.groupby('size')['faculty_count'].sum().reset_index(name='sum')
        fig7 = px.bar(Sum_faculty, x='size', y='sum', color='size', 
             labels={'size': 'Size', 'sum': 'Total number of faculty count'},
             title=f'Total number of faculty count by university size in {selected_region}')
        fig7.update_layout(
        plot_bgcolor='rgba(1,1,1,0)',  # set the plot background color to transparent
        paper_bgcolor='rgba(1,1,1,0)',  # set the paper background color to transparent
        font=dict(color='black'), # set the font color to black
        title_font=dict(size=19, family='Arial, sans-serif'), # set the title font size and family
        title_x=0.5, # set the title x position to the center
        title_y=0.9, # set the title font size and weight
        )
        graph7 = dcc.Graph(id="my-bar-chart-7", figure=fig7)
        
        return html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph2]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "100%",
                    "height": "100%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph3]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph4]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph5]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph6]
            ),
            html.Div(
                className="six columns",
                style={
                    "width": "50%",
                    "height": "50%",
                    'display': 'inline-block',
                    "border": "1px solid #000000"
                },
                children=[graph7]
            )
        ]
    )

    else:
        return None
    
if __name__ == "__main__":
    app.run_server(port=8083,debug=True)
