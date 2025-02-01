# Creatine Supplementation Study Analysis

A comprehensive system for analyzing and visualizing the effects of creatine supplementation on strength, muscle mass, and performance metrics.

## Features

- **Data Management**: SQLite database for storing participant data and measurements.
- **Advanced Analysis**: Statistical analysis of supplementation effects across different populations.
- **Interactive Visualization**: Dynamic plots and charts using Plotly and Dash.
- **Research-Based**: Implementation based on peer-reviewed research findings.
- **Comprehensive Testing**: Full test coverage with pytest.
- **Interactive Dashboard**: Web-based dashboard for real-time data exploration.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Ronsini/Creatine-Study.git
cd creatine-study
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package and dependencies:
```bash
pip install -e .[dev]
```

## Quick Start

1. Initialize the database:
```bash
python -m src.main --init-db
```

2. Run the analysis:
```bash
python -m src.main --analyze
```

3. Generate visualizations:
```bash
python -m src.main --visualize
```

4. Launch the dashboard:
```bash
python -m src.main --dashboard
```

## Project Structure

```
creatine-study/
├── database/               # Database files
│   ├── schema.sql         # Database schema
│   └── queries.sql        # Analysis queries
├── src/                   # Source code
│   ├── database.py        # Database operations
│   ├── analysis.py        # Data analysis
│   ├── visualization.py   # Data visualization
│   └── dashboard.py       # Web dashboard
├── tests/                 # Test files
│   ├── test_database.py
│   ├── test_analysis.py
│   └── test_visualization.py
├── notebooks/             # Jupyter notebooks
└── docs/                  # Documentation
```

## Usage Examples

### Basic Analysis
```python
from src.database import CreatineDatabase
from src.analysis import CreatineAnalysis

# Initialize database
db = CreatineDatabase()

# Create analysis instance
analysis = CreatineAnalysis(db)

# Generate comprehensive report
report = analysis.generate_summary_report()
```

### Visualization
```python
from src.visualization import CreatineVisualization

# Create visualization instance
viz = CreatineVisualization(db)

# Generate plots
viz.generate_summary_plots('output/plots')
```

### Interactive Dashboard
```python
from src.dashboard import CreatineDashboard

# Create and run dashboard
dashboard = CreatineDashboard(db)
dashboard.run_server(debug=True)
```

## Testing

Run the test suite:
```bash
pytest tests/
```

Generate coverage report:
```bash
pytest --cov=src tests/
```

## Contributing

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## Development Setup

Install development dependencies:
```bash
pip install -e .[dev,docs]
```

Format code:
```bash
black src/ tests/
isort src/ tests/
```

Run linters:
```bash
flake8 src/ tests/
mypy src/ tests/
```

## Documentation

Build the documentation:
```bash
cd docs
make html
```

View the documentation at `docs/_build/html/index.html`.

## Acknowledgments

- Research based on [PMC8949037](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8949037/).
- Database design inspired by clinical trial data management systems.
- Visualization approaches based on scientific publication standards.

## Contact

Ronald Orsini - ronniej7orsini@gmail.com

Project Link: [https://github.com/Ronsini/creatine-study](https://github.com/Ronsini/creatine-study)

