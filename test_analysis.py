import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from src.database import CreatineDatabase
from src.analysis import CreatineAnalysis

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
        }
    ]
    
    participant_ids = []
    for p in participants:
        participant_ids.append(db.add_participant(p))
    
    # Add measurements for each participant
    dates = [datetime.now().date() + timedelta(days=i*7) for i in range(4)]
    for pid in participant_ids:
        for i, date in enumerate(dates):
            # Simulate different progression rates for creatine vs placebo
            strength_increment = 5 if pid == participant_ids[0] else 3
            mass_increment = 0.5 if pid == participant_ids[0] else 0.3
            
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
def analysis(test_db):
    """Create analysis instance with test database."""
    return CreatineAnalysis(test_db)

def test_calculate_effect_sizes(analysis):
    """Test effect size calculations."""
    results = analysis.calculate_effect_sizes()
    
    # Check results structure
    assert isinstance(results, dict)
    assert 'population_effects' in results
    assert 'effect_sizes' in results
    
    # Check effect size calculations
    for metric in results['effect_sizes']:
        df = results['effect_sizes'][metric]
        assert 'effect_size' in df.columns
        assert 'interpretation' in df.columns
        assert all(df['interpretation'].isin(['Negligible', 'Small', 'Medium', 'Large']))

def test_analyze_progression_rates(analysis):
    """Test progression rate analysis."""
    results = analysis.analyze_progression_rates()
    
    # Check results structure
    assert isinstance(results, dict)
    assert 'individual_rates' in results
    assert 'summary_statistics' in results
    
    # Check rate calculations
    rates_df = results['individual_rates']
    assert 'strength_1rm_kg_rate' in rates_df.columns
    assert 'lean_mass_kg_rate' in rates_df.columns
    assert all(rates_df['strength_1rm_kg_rate'] >= 0)  # Rates should be positive

def test_analyze_training_impact(analysis):
    """Test training impact analysis."""
    results = analysis.analyze_training_impact()
    
    assert isinstance(results, dict)
    assert 'program_analysis' in results
    assert 'compliance_analysis' in results
    
    # Verify training impact analysis
    prog_analysis = results['program_analysis']
    assert not prog_analysis.empty
    assert 'strength_gain_percentage' in prog_analysis.columns

def test_analyze_age_effects(analysis):
    """Test age effects analysis."""
    results = analysis.analyze_age_effects()
    
    assert isinstance(results, pd.DataFrame)
    assert 'age_group' in results.columns
    assert 'strength_gain_percentage' in results.columns
    assert 'mass_gain_percentage' in results.columns

def test_analyze_dosing_protocols(analysis):
    """Test dosing protocol analysis."""
    results = analysis.analyze_dosing_protocols()
    
    assert isinstance(results, pd.DataFrame)
    assert 'dosing_protocol' in results.columns
    assert 'strength_gain_percentage' in results.columns
    assert not results.empty

def test_analyze_fatigue_and_recovery(analysis):
    """Test fatigue and recovery analysis."""
    results = analysis.analyze_fatigue_and_recovery()
    
    assert isinstance(results, dict)
    assert 'fatigue_analysis' in results
    assert 'recovery_patterns' in results
    
    # Check recovery patterns
    recovery_df = results['recovery_patterns']
    assert 'avg_fatigue_recovery' in recovery_df.columns
    assert 'avg_performance_recovery' in recovery_df.columns

def test_generate_summary_report(analysis):
    """Test summary report generation."""
    report = analysis.generate_summary_report()
    
    # Check report structure
    assert isinstance(report, dict)
    expected_sections = [
        'effect_sizes',
        'progression_rates',
        'training_impact',
        'age_effects',
        'dosing_protocols',
        'fatigue_recovery'
    ]
    for section in expected_sections:
        assert section in report

def test_invalid_data_handling(test_db):
    """Test handling of invalid or missing data."""
    # Create analysis instance with empty database
    empty_db = CreatineDatabase("empty_test.db")
    empty_db.init_database()
    analysis = CreatineAnalysis(empty_db)
    
    try:
        # Should handle empty database gracefully
        results = analysis.calculate_effect_sizes()
        assert isinstance(results, dict)
    finally:
        empty_db.close()
        if os.path.exists("empty_test.db"):
            os.remove("empty_test.db")

def test_effect_size_interpretation(analysis):
    """Test effect size interpretation function."""
    interpretations = [
        analysis._interpret_effect_size(0.1),  # Should be "Negligible"
        analysis._interpret_effect_size(0.3),  # Should be "Small"
        analysis._interpret_effect_size(0.6),  # Should be "Medium"
        analysis._interpret_effect_size(0.9)   # Should be "Large"
    ]
    
    assert interpretations[0] == "Negligible"
    assert interpretations[1] == "Small"
    assert interpretations[2] == "Medium"
    assert interpretations[3] == "Large"

if __name__ == '__main__':
    pytest.main([__file__])