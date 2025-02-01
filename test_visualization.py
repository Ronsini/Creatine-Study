import pytest
import matplotlib.pyplot as plt
import pandas as pd
import os
from pathlib import Path
from datetime import datetime, timedelta
from src.database import CreatineDatabase
from src.visualization import CreatineVisualization

@pytest.fixture
def test_db():
    """Create a temporary test database with sample data."""
    db_path = "test_creatine_study.db"
    db = CreatineDatabase(db_path)
    db.init_database()
    
    # Add test participants
    participants = [
        {
            'age': 25,
            'gender': 'male',
            'weight_kg': 75.5,
            'height_cm': 180.0,
            'training_status': 'trained',
            'group_assignment': 'creatine',
            'dosing_protocol': 'loading',
            'population_category': 'young_trained'
        },
        {
            'age': 28,
            'gender': 'male',
            'weight_kg': 78.0,
            'height_cm': 175.0,
            'training_status': 'trained',
            'group_assignment': 'placebo',
            'dosing_protocol': 'loading',
            'population_category': 'young_trained'
        },
        {
            'age': 52,
            'gender': 'male',
            'weight_kg': 82.0,
            'height_cm': 178.0,
            'training_status': 'untrained',
            'group_assignment': 'creatine',
            'dosing_protocol': 'loading',
            'population_category': 'older_untrained'
        }
    ]
    
    participant_ids = []
    for p in participants:
        participant_ids.append(db.add_participant(p))
    
    # Add measurements for each participant
    dates = [datetime.now().date() + timedelta(days=i*7) for i in range(6)]
    for pid in participant_ids:
        for i, date in enumerate(dates):
            # Simulate different progression rates
            if pid == participant_ids[0]:  # Young trained creatine
                strength_increment = 5
                mass_increment = 0.5
            elif pid == participant_ids[1]:  # Young trained placebo
                strength_increment = 3
                mass_increment = 0.3
            else:  # Older untrained creatine
                strength_increment = 2
                mass_increment = 0.2
            
            db.add_measurement({
                'participant_id': pid,
                'measurement_date': date,
                'strength_1rm_kg': 100.0 + i * strength_increment,
                'lean_mass_kg': 65.0 + i * mass_increment,
                'muscle_thickness_mm': 35.0 + i * 0.2,
                'creatine_kinase_level': 150.0 + i * 10,
                'performance_score': 8.5 + i * 0.2,
                'fatigue_level': 3
            })
    
    yield db
    db.close()
    if os.path.exists(db_path):
        os.remove(db_path)

@pytest.fixture
def visualization(test_db):
    """Create visualization instance with test database."""
    return CreatineVisualization(test_db)

@pytest.fixture
def test_output_dir():
    """Create and clean up a test output directory."""
    output_dir = Path("test_plots")
    output_dir.mkdir(exist_ok=True)
    yield output_dir
    # Cleanup
    for file in output_dir.glob("*"):
        file.unlink()
    output_dir.rmdir()

def test_plot_strength_progression(visualization, test_output_dir):
    """Test strength progression plot generation."""
    fig = visualization.plot_strength_progression(str(test_output_dir / "strength.png"))
    
    assert isinstance(fig, plt.Figure)
    assert os.path.exists(test_output_dir / "strength.png")
    
    # Check plot components
    ax = fig.gca()
    assert ax.get_xlabel().lower() == 'date'
    assert 'strength' in ax.get_ylabel().lower()
    assert len(ax.lines) > 0  # Should have at least one line

def test_plot_mass_changes(visualization, test_output_dir):
    """Test mass changes plot generation."""
    fig = visualization.plot_mass_changes(str(test_output_dir / "mass.png"))
    
    assert isinstance(fig, plt.Figure)
    assert os.path.exists(test_output_dir / "mass.png")
    
    # Check plot components
    ax = fig.gca()
    assert ax.get_xlabel().lower() == 'date'
    assert 'mass' in ax.get_ylabel().lower()
    assert len(ax.lines) > 0

def test_plot_effect_sizes(visualization, test_output_dir):
    """Test effect sizes plot generation."""
    fig = visualization.plot_effect_sizes(str(test_output_dir / "effects.png"))
    
    assert isinstance(fig, plt.Figure)
    assert os.path.exists(test_output_dir / "effects.png")
    
    # Check plot components
    ax = fig.gca()
    assert 'effect' in ax.get_title().lower()
    assert len(ax.patches) > 0  # Should have bars

def test_plot_age_comparison(visualization, test_output_dir):
    """Test age comparison plot generation."""
    fig = visualization.plot_age_comparison(str(test_output_dir / "age.png"))
    
    assert isinstance(fig, plt.Figure)
    assert os.path.exists(test_output_dir / "age.png")
    
    # Should have two subplots
    assert len(fig.axes) == 2

def test_plot_training_compliance(visualization, test_output_dir):
    """Test training compliance plot generation."""
    fig = visualization.plot_training_compliance(str(test_output_dir / "compliance.png"))
    
    assert isinstance(fig, plt.Figure)
    assert os.path.exists(test_output_dir / "compliance.png")
    
    # Should have two subplots
    assert len(fig.axes) == 2

def test_generate_summary_plots(visualization, test_output_dir):
    """Test generation of all summary plots."""
    visualization.generate_summary_plots(str(test_output_dir))
    
    # Check that all expected plot files were created
    expected_files = [
        'strength_progression.png',
        'mass_changes.png',
        'effect_sizes.png',
        'age_comparison.png',
        'training_compliance.png'
    ]
    
    for filename in expected_files:
        assert os.path.exists(test_output_dir / filename)

def test_plot_style_consistency(visualization):
    """Test consistency of plot styling."""
    fig1 = visualization.plot_strength_progression()
    fig2 = visualization.plot_mass_changes()
    
    # Compare style elements between plots
    ax1 = fig1.gca()
    ax2 = fig2.gca()
    
    assert ax1.get_figure().get_figwidth() == ax2.get_figure().get_figwidth()
    assert ax1.get_figure().get_figheight() == ax2.get_figure().get_figheight()

def test_empty_data_handling(test_db, test_output_dir):
    """Test handling of empty database."""
    # Create new empty database
    empty_db = CreatineDatabase("empty_test.db")
    empty_db.init_database()
    viz = CreatineVisualization(empty_db)
    
    try:
        # Should handle empty database gracefully
        fig = viz.plot_strength_progression(str(test_output_dir / "empty.png"))
        assert isinstance(fig, plt.Figure)
        assert os.path.exists(test_output_dir / "empty.png")
    finally:
        empty_db.close()
        if os.path.exists("empty_test.db"):
            os.remove("empty_test.db")

def test_figure_cleanup(visualization):
    """Test that figures are properly cleaned up."""
    initial_figures = len(plt.get_fignums())
    
    visualization.plot_strength_progression()
    visualization.plot_mass_changes()
    
    # Check that figures are closed
    plt.close('all')
    assert len(plt.get_fignums()) == initial_figures

if __name__ == '__main__':
    pytest.main([__file__])