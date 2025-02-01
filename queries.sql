-- Population Category Analysis
SELECT 
    p.population_category,
    p.group_assignment,
    COUNT(DISTINCT p.participant_id) as participant_count,
    ROUND(AVG(m2.strength_1rm_kg - m1.strength_1rm_kg), 2) as avg_strength_gain,
    ROUND(AVG((m2.strength_1rm_kg - m1.strength_1rm_kg) / m1.strength_1rm_kg * 100), 2) as strength_gain_percentage,
    ROUND(AVG(m2.lean_mass_kg - m1.lean_mass_kg), 2) as avg_mass_gain,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY p.population_category, p.group_assignment
ORDER BY strength_gain_percentage DESC;

-- Training Status Effect
SELECT 
    p.training_status,
    p.group_assignment,
    ROUND(AVG(m2.strength_1rm_kg - m1.strength_1rm_kg), 2) as avg_strength_gain,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage,
    ROUND(AVG(m2.performance_score - m1.performance_score), 2) as avg_performance_gain,
    COUNT(DISTINCT p.participant_id) as participant_count
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY p.training_status, p.group_assignment
ORDER BY avg_strength_gain DESC;

-- Weekly Progress Tracking
SELECT 
    p.group_assignment,
    p.training_status,
    m.measurement_date,
    ROUND(AVG(m.strength_1rm_kg), 2) as avg_strength,
    ROUND(AVG(m.lean_mass_kg), 2) as avg_lean_mass,
    ROUND(AVG(m.performance_score), 2) as avg_performance,
    COUNT(DISTINCT p.participant_id) as participant_count
FROM participants p
JOIN measurements m ON p.participant_id = m.participant_id
GROUP BY p.group_assignment, p.training_status, m.measurement_date
ORDER BY m.measurement_date;

-- Training Program Analysis
SELECT 
    p.training_status as program_name,
    p.group_assignment,
    COUNT(DISTINCT p.participant_id) as participant_count,
    ROUND(AVG((m2.strength_1rm_kg - m1.strength_1rm_kg) / m1.strength_1rm_kg * 100), 2) as strength_gain_percentage,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage,
    ROUND(AVG(m2.performance_score - m1.performance_score), 2) as performance_improvement
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY p.training_status, p.group_assignment
ORDER BY strength_gain_percentage DESC;

-- Training Compliance Impact
SELECT 
    p.training_status,
    CASE 
        WHEN m2.performance_score - m1.performance_score > 1.5 THEN TRUE 
        ELSE FALSE 
    END as high_compliance,
    COUNT(DISTINCT p.participant_id) as participant_count,
    ROUND(AVG((m2.strength_1rm_kg - m1.strength_1rm_kg) / m1.strength_1rm_kg * 100), 2) as strength_gain_percentage,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY p.training_status, high_compliance
ORDER BY strength_gain_percentage DESC;

-- Age Group Analysis
SELECT 
    CASE 
        WHEN age < 30 THEN 'Young (18-29)'
        WHEN age BETWEEN 30 AND 50 THEN 'Middle (30-50)'
        ELSE 'Older (50+)'
    END as age_group,
    group_assignment,
    COUNT(DISTINCT p.participant_id) as participant_count,
    ROUND(AVG((m2.strength_1rm_kg - m1.strength_1rm_kg) / m1.strength_1rm_kg * 100), 2) as strength_gain_percentage,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY age_group, group_assignment
ORDER BY strength_gain_percentage DESC;

-- Dosing Protocol Analysis
SELECT 
    p.dosing_protocol,
    p.group_assignment,
    COUNT(DISTINCT p.participant_id) as participant_count,
    ROUND(AVG((m2.strength_1rm_kg - m1.strength_1rm_kg) / m1.strength_1rm_kg * 100), 2) as strength_gain_percentage,
    ROUND(AVG((m2.lean_mass_kg - m1.lean_mass_kg) / m1.lean_mass_kg * 100), 2) as mass_gain_percentage,
    ROUND(AVG(m2.performance_score - m1.performance_score), 2) as performance_improvement
FROM participants p
JOIN measurements m1 ON p.participant_id = m1.participant_id
JOIN measurements m2 ON p.participant_id = m2.participant_id
WHERE m1.measurement_date = (SELECT MIN(measurement_date) FROM measurements)
AND m2.measurement_date = (SELECT MAX(measurement_date) FROM measurements)
GROUP BY p.dosing_protocol, p.group_assignment
ORDER BY strength_gain_percentage DESC;

-- Fatigue Level Analysis
SELECT 
    p.group_assignment,
    m.measurement_date,
    ROUND(AVG(m.fatigue_level), 2) as avg_fatigue,
    ROUND(AVG(m.creatine_kinase_level), 2) as avg_ck_level,
    COUNT(DISTINCT p.participant_id) as participant_count
FROM participants p
JOIN measurements m ON p.participant_id = m.participant_id
GROUP BY p.group_assignment, m.measurement_date
ORDER BY m.measurement_date;