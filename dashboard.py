import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import logging
from .database import CreatineDatabase
import dash_bootstrap_components as dbc

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CreatineDashboard:
    def __init__(self, db: CreatineDatabase):
        """Initialize dashboard with database connection."""
        self.db = db
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
        self.setup_layout()
        self.setup_callbacks()
        logger.info("Dashboard initialized")

    def setup_layout(self):
        """Set up the dashboard layout."""
        self.app.layout = dbc.Container([
            dbc.Row([
                dbc.Col(html.H1("Creatine Supplementation Study Dashboard", 
                               className="text-center mb-4"), width=12)
            ]),

            dbc.Row([
                dbc.Col([
                    html.H4("Study Metrics"),
                    dcc.Dropdown(
                        id='metric-selector',
                        options=[
                            {'label': 'Strength (1RM)', 'value': 'strength_1rm_kg'},
                            {'label': 'Lean Mass', 'value': 'lean_mass_kg'},
                            {'label': 'Performance Score', 'value': 'performance_score'}
                        ],
                        value='strength_1rm_kg'
                    )
                ], width=6),

                dbc.Col([
                    html.H4("Group Filter"),
                    dcc.Dropdown(
                        id='group-selector',
                        options=[
                            {'label': 'All Groups', 'value': 'all'},
                            {'label': 'Creatine', 'value': 'creatine'},
                            {'label': 'Placebo', 'value': 'placebo'}
                        ],
                        value='all'
                    )
                ], width=6)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='progression-chart')
                ], width=12)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='age-comparison-chart')
                ], width=6),
                dbc.Col([
                    dcc.Graph(id='training-impact-chart')
                ], width=6)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col([
                    html.H4("Summary Statistics", className="text-center"),
                    html.Div(id='summary-stats')
                ], width=12)
            ])
        ], fluid=True)

    def setup_callbacks(self):
        """Set up dashboard callbacks."""
        @self.app.callback(
            [Output('progression-chart', 'figure'),
             Output('age-comparison-chart', 'figure'),
             Output('training-impact-chart', 'figure'),
             Output('summary-stats', 'children')],
            [Input('metric-selector', 'value'),
             Input('group-selector', 'value')]
        )
        def update_charts(metric, group_filter):
            try:
                # Get data
                progress_data = self.db.get_progress_data()
                if group_filter != 'all':
                    progress_data = progress_data[progress_data['group_assignment'] == group_filter]

                # Progression Chart
                prog_fig = px.line(progress_data, 
                                 x='measurement_date', 
                                 y=metric,
                                 color='group_assignment',
                                 line_group='participant_id',
                                 title='Progression Over Time')

                # Age Comparison Chart
                age_data = progress_data.copy()
                age_data['age_group'] = pd.cut(age_data['age'], 
                                             bins=[0, 30, 50, 100],
                                             labels=['Young', 'Middle', 'Older'])
                age_fig = px.box(age_data,
                               x='age_group',
                               y=metric,
                               color='group_assignment',
                               title='Results by Age Group')

                # Training Impact Chart
                training_fig = px.box(progress_data,
                                    x='training_status',
                                    y=metric,
                                    color='group_assignment',
                                    title='Results by Training Status')

                # Summary Statistics
                stats = progress_data.groupby('group_assignment')[metric].agg(['mean', 'std', 'count']).round(2)
                stats_table = dbc.Table.from_dataframe(stats, 
                                                     striped=True, 
                                                     bordered=True,
                                                     hover=True)

                return prog_fig, age_fig, training_fig, stats_table
            except Exception as e:
                logger.error(f"Error updating dashboard: {e}")
                raise

    def create_comparison_chart(self, data: pd.DataFrame, metric: str) -> go.Figure:
        """Create a comparison chart for the selected metric."""
        try:
            fig = make_subplots(rows=1, cols=2,
                              subplot_titles=('Individual Progression', 'Group Averages'))

            # Individual progression lines
            for group in data['group_assignment'].unique():
                group_data = data[data['group_assignment'] == group]
                fig.add_trace(
                    go.Scatter(x=group_data['measurement_date'],
                             y=group_data[metric],
                             mode='lines',
                             name=f'{group} (individual)',
                             opacity=0.3),
                    row=1, col=1
                )

            # Group averages
            avg_data = data.groupby(['measurement_date', 'group_assignment'])[metric].mean().reset_index()
            for group in avg_data['group_assignment'].unique():
                group_avg = avg_data[avg_data['group_assignment'] == group]
                fig.add_trace(
                    go.Scatter(x=group_avg['measurement_date'],
                             y=group_avg[metric],
                             mode='lines+markers',
                             name=f'{group} (average)',
                             line=dict(width=3)),
                    row=1, col=2
                )

            fig.update_layout(height=500, title_text=f"{metric.replace('_', ' ').title()} Comparison")
            return fig
        except Exception as e:
            logger.error(f"Error creating comparison chart: {e}")
            raise

    def run_server(self, debug: bool = False, port: int = 8050):
        """Run the dashboard server."""
        try:
            logger.info(f"Starting dashboard server on port {port}")
            self.app.run_server(debug=debug, port=port)
        except Exception as e:
            logger.error(f"Error running dashboard server: {e}")
            raise

if __name__ == '__main__':
    # Example usage
    db = CreatineDatabase()
    dashboard = CreatineDashboard(db)
    
    try:
        dashboard.run_server(debug=True)
    finally:
        db.close()