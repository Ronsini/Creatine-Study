import pytest
import pandas as pd
from datetime import datetime, timedelta
import os
from src.database import CreatineDatabase

@pytest.fixture
def test_db():
    """Create a temporary test database."""
    db_path = "test_creatine_study.db"
    db = CreatineDatabase(db_path)
    db.init_database()
    yield db
    db.close()
    # Cleanup: remove test database
    if os.path.exists(db_path):
        os.remove(db_path)

def test_database_initialization(test_db):
    """Test database initialization."""
    # Verify tables exist
    with test_db.engine.connect() as conn:
        # Check if tables exist
        tables = ['participants', 'measurements', 'dosing_protocols', 
                 'training_programs', 'participant_training']
        for table in tables:
            result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            assert result.fetchone() is not None

def test_add_participant(test_db):
    """Test adding a participant."""
    participant_data = {
        'age': 25,
        'gender': 'male',
        'weight_kg': 75.5,
        'height_cm': 180.0,
        'training_experience_years': 2.5,
        'training_status': 'trained',
        'group_assignment': 'creatine',
        'dosing_protocol': 'loading',
        'population_category': 'young_trained'
    }
    
    # Add participant
    participant_id = test_db.add_participant(participant_data)
    assert participant_id is not None
    
    # Verify participant was added
    df = test_db.get_participant_data(participant_id)
    assert len(df) == 1
    assert df['age'].iloc[0] == 25
    assert df['weight_kg'].iloc[0] == 75.5

def test_add_measurement(test_db):
    """Test adding a measurement."""
    # First add a participant
    participant_id = test_db.add_participant({
        'age': 25,
        'gender': 'male',
        'weight_kg': 75.5,
        'height_cm': 180.0,
        'training_status': 'trained',
        'group_assignment': 'creatine',
        'dosing_protocol': 'loading',
        'population_category': 'young_trained'
    })
    
    # Add measurement
    measurement_data = {
        'participant_id': participant_id,
        'measurement_date': datetime.now().date(),
        'strength_1rm_kg': 100.0,
        'lean_mass_kg': 65.0,
        'muscle_thickness_mm': 35.0,
        'creatine_kinase_level': 150.0,
        'performance_score': 8.5,
        'fatigue_level': 3
    }
    
    measurement_id = test_db.add_measurement(measurement_data)
    assert measurement_id is not None
    
    # Verify measurement was added
    measurements = test_db.get_measurements(participant_id)
    assert len(measurements) == 1
    assert measurements['strength_1rm_kg'].iloc[0] == 100.0

def test_get_progress_data(test_db):
    """Test retrieving progress data."""
    # Add participant and measurements
    participant_id = test_db.add_participant({
        'age': 25,
        'gender': 'male',
        'weight_kg': 75.5,
        'height_cm': 180.0,
        'training_status': 'trained',
        'group_assignment': 'creatine',
        'dosing_protocol': 'loading',
        'population_category': 'young_trained'
    })
    
    # Add multiple measurements
    dates = [datetime.now().date() + timedelta(days=i*7) for i in range(3)]
    for i, date in enumerate(dates):
        test_db.add_measurement({
            'participant_id': participant_id,
            'measurement_date': date,
            'strength_1rm_kg': 100.0 + i*5,
            'lean_mass_kg': 65.0 + i*0.5,
            'muscle_thickness_mm': 35.0,
            'creatine_kinase_level': 150.0,
            'performance_score': 8.5,
            'fatigue_level': 3
        })
    
    # Get progress data
    progress_data = test_db.get_progress_data()
    assert len(progress_data) == 3
    assert list(progress_data['strength_1rm_kg']) == [100.0, 105.0, 110.0]

def test_run_analysis_query(test_db):
    """Test running analysis queries."""
    # Add test data
    participant_id = test_db.add_participant({
        'age': 25,
        'gender': 'male',
        'weight_kg': 75.5,
        'height_cm': 180.0,
        'training_status': 'trained',
        'group_assignment': 'creatine',
        'dosing_protocol': 'loading',
        'population_category': 'young_trained'
    })
    
    # Add measurements
    dates = [datetime.now().date(), datetime.now().date() + timedelta(days=30)]
    for date in dates:
        test_db.add_measurement({
            'participant_id': participant_id,
            'measurement_date': date,
            'strength_1rm_kg': 100.0,
            'lean_mass_kg': 65.0,
            'muscle_thickness_mm': 35.0,
            'creatine_kinase_level': 150.0,
            'performance_score': 8.5,
            'fatigue_level': 3
        })
    
    # Run analysis query
    result = test_db.run_analysis_query("Population Category Analysis")
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0

def test_backup_database(test_db):
    """Test database backup functionality."""
    # Add some test data
    test_db.add_participant({
        'age': 25,
        'gender': 'male',
        'weight_kg': 75.5,
        'height_cm': 180.0,
        'training_status': 'trained',
        'group_assignment': 'creatine',
        'dosing_protocol': 'loading',
        'population_category': 'young_trained'
    })
    
    # Create backup
    backup_path = test_db.backup_database()
    
    # Verify backup file exists
    assert os.path.exists(backup_path)
    
    # Cleanup
    os.remove(backup_path)

def test_invalid_participant_data(test_db):
    """Test handling of invalid participant data."""
    invalid_data = {
        'age': 25  # Missing required fields
    }
    
    with pytest.raises(ValueError):
        test_db.add_participant(invalid_data)

def test_invalid_measurement_data(test_db):
    """Test handling of invalid measurement data."""
    invalid_data = {
        'participant_id': 999  # Non-existent participant
    }
    
    with pytest.raises(ValueError):
        test_db.add_measurement(invalid_data)

if __name__ == '__main__':
    pytest.main([__file__])