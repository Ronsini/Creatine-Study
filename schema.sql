-- Drop tables if they exist
DROP TABLE IF EXISTS measurements;
DROP TABLE IF EXISTS participant_training;
DROP TABLE IF EXISTS training_programs;
DROP TABLE IF EXISTS dosing_protocols;
DROP TABLE IF EXISTS participants;

-- Participants table storing subject information
CREATE TABLE participants (
    participant_id INTEGER PRIMARY KEY,
    age INTEGER NOT NULL,
    gender TEXT NOT NULL,
    weight_kg FLOAT NOT NULL,
    height_cm FLOAT NOT NULL,
    training_experience_years FLOAT,
    training_status TEXT CHECK(training_status IN ('trained', 'untrained')),
    group_assignment TEXT CHECK(group_assignment IN ('creatine', 'placebo')),
    dosing_protocol TEXT CHECK(dosing_protocol IN ('loading', 'maintenance')),
    population_category TEXT CHECK(population_category IN ('young trained', 'young untrained', 'older untrained')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Dosing protocols table based on research findings
CREATE TABLE dosing_protocols (
    protocol_id INTEGER PRIMARY KEY,
    protocol_name TEXT NOT NULL,
    daily_dose_g FLOAT NOT NULL,
    duration_days INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Training programs based on research protocols
CREATE TABLE training_programs (
    program_id INTEGER PRIMARY KEY,
    program_name TEXT NOT NULL,
    frequency_per_week INTEGER,
    intensity_percentage FLOAT,
    exercise_type TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Participant training assignments
CREATE TABLE participant_training (
    participant_id INTEGER,
    program_id INTEGER,
    start_date DATE,
    end_date DATE,
    compliance_percentage FLOAT,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id),
    FOREIGN KEY (program_id) REFERENCES training_programs(program_id)
);

-- Measurements table tracking all metrics from research
CREATE TABLE measurements (
    measurement_id INTEGER PRIMARY KEY,
    participant_id INTEGER,
    measurement_date DATE,
    strength_1rm_kg FLOAT,
    lean_mass_kg FLOAT,
    muscle_thickness_mm FLOAT,
    creatine_kinase_level FLOAT,
    performance_score FLOAT,
    fatigue_level INTEGER CHECK(fatigue_level BETWEEN 1 AND 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id)
);

-- Insert initial dosing protocols
INSERT INTO dosing_protocols (protocol_name, daily_dose_g, duration_days, description) VALUES
('Loading Phase', 20, 7, 'Initial loading phase: 20g/day for 7 days'),
('Maintenance Phase', 5, 49, 'Maintenance phase: 5g/day for 49 days'),
('Direct Maintenance', 3, 56, 'Direct maintenance without loading: 3g/day for 56 days');

-- Insert initial training programs
INSERT INTO training_programs (program_name, frequency_per_week, intensity_percentage, exercise_type, description) VALUES
('Resistance Training', 3, 75, 'resistance', 'Whole-body resistance training 3x per week'),
('Complex Training', 4, 80, 'complex', 'Combined strength and power training'),
('Soccer Training', 5, 70, 'sport_specific', 'Elite soccer training program');

-- Create indexes for better performance
CREATE INDEX idx_participant_group ON participants(group_assignment);
CREATE INDEX idx_participant_status ON participants(training_status);
CREATE INDEX idx_measurements_date ON measurements(measurement_date);
CREATE INDEX idx_participant_training ON participant_training(participant_id, program_id);