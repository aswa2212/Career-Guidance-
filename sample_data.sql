-- Sample Data for Career Tracking System Database
-- Run these SQL commands in your PostgreSQL database to add sample data

-- Add SNS College and other sample colleges
INSERT INTO colleges (name, address, city, state, pincode, website, latitude, longitude) VALUES
('SNS College of Technology', 'Sathy Road, Coimbatore', 'Coimbatore', 'Tamil Nadu', '641035', 'https://snsct.org', 11.0168, 76.9558),
('Indian Institute of Technology Madras', 'IIT Madras, Chennai', 'Chennai', 'Tamil Nadu', '600036', 'https://iitm.ac.in', 12.9916, 80.2336),
('Anna University', 'Sardar Patel Road, Guindy', 'Chennai', 'Tamil Nadu', '600025', 'https://annauniv.edu', 13.0067, 80.2206),
('PSG College of Technology', 'Avinashi Road, Peelamedu', 'Coimbatore', 'Tamil Nadu', '641004', 'https://psgtech.edu', 11.0194, 76.9319),
('VIT University', 'Katpadi, Vellore', 'Vellore', 'Tamil Nadu', '632014', 'https://vit.ac.in', 12.9692, 79.1559)
ON CONFLICT (name) DO NOTHING;

-- Add sample courses
INSERT INTO courses (title, description, category, duration, level, skills_required, career_opportunities) VALUES
('Computer Science Engineering', 'Comprehensive program covering programming, algorithms, data structures, and software engineering', 'Engineering', '4 years', 'Undergraduate', ARRAY['Programming', 'Mathematics', 'Problem Solving'], ARRAY['Software Developer', 'Data Scientist', 'System Architect']),
('Data Science', 'Master data analysis, machine learning, statistics, and big data technologies', 'Technology', '2 years', 'Postgraduate', ARRAY['Python', 'Statistics', 'Machine Learning'], ARRAY['Data Scientist', 'ML Engineer', 'Business Analyst']),
('Artificial Intelligence', 'Advanced AI concepts including neural networks, deep learning, and cognitive computing', 'Technology', '2 years', 'Postgraduate', ARRAY['Python', 'Mathematics', 'Neural Networks'], ARRAY['AI Engineer', 'ML Researcher', 'Robotics Engineer']),
('Web Development', 'Full-stack web development with modern frameworks and technologies', 'Technology', '6 months', 'Certificate', ARRAY['HTML', 'CSS', 'JavaScript', 'React'], ARRAY['Frontend Developer', 'Backend Developer', 'Full Stack Developer']),
('Mechanical Engineering', 'Design, development, and manufacturing of mechanical systems and machines', 'Engineering', '4 years', 'Undergraduate', ARRAY['Mathematics', 'Physics', 'CAD Design'], ARRAY['Mechanical Engineer', 'Design Engineer', 'Manufacturing Engineer']),
('Business Administration', 'Develop leadership and management skills for business success', 'Business', '2 years', 'Postgraduate', ARRAY['Leadership', 'Management', 'Communication'], ARRAY['Business Manager', 'Consultant', 'Entrepreneur']),
('Digital Marketing', 'Learn modern digital marketing strategies and tools', 'Business', '3 months', 'Certificate', ARRAY['SEO', 'Social Media', 'Analytics'], ARRAY['Digital Marketer', 'SEO Specialist', 'Content Manager'])
ON CONFLICT (title) DO NOTHING;

-- Add sample careers
INSERT INTO careers (title, description, field, average_salary, growth_rate, required_skills, education_requirements) VALUES
('Software Developer', 'Design, develop, and maintain software applications and systems', 'Technology', 800000, 15.5, ARRAY['Programming', 'Problem Solving', 'Software Design'], ARRAY['Bachelor in Computer Science', 'Programming Bootcamp']),
('Data Scientist', 'Analyze complex data to help companies make better business decisions', 'Technology', 1200000, 22.0, ARRAY['Python', 'Statistics', 'Machine Learning', 'Data Analysis'], ARRAY['Master in Data Science', 'Statistics Background']),
('Mechanical Engineer', 'Design and develop mechanical systems, machines, and tools', 'Engineering', 600000, 8.5, ARRAY['CAD Design', 'Mathematics', 'Physics', 'Problem Solving'], ARRAY['Bachelor in Mechanical Engineering']),
('AI Engineer', 'Develop artificial intelligence systems and machine learning models', 'Technology', 1500000, 25.0, ARRAY['Python', 'Machine Learning', 'Neural Networks', 'Deep Learning'], ARRAY['Master in AI/ML', 'Computer Science Background']),
('Web Developer', 'Create and maintain websites and web applications', 'Technology', 500000, 18.0, ARRAY['HTML', 'CSS', 'JavaScript', 'React', 'Node.js'], ARRAY['Web Development Bootcamp', 'Computer Science Degree']),
('Business Analyst', 'Analyze business processes and recommend improvements', 'Business', 700000, 12.0, ARRAY['Data Analysis', 'Communication', 'Problem Solving'], ARRAY['Business Administration Degree', 'Analytics Certification']),
('Digital Marketing Specialist', 'Plan and execute digital marketing campaigns', 'Marketing', 450000, 20.0, ARRAY['SEO', 'Social Media', 'Analytics', 'Content Creation'], ARRAY['Marketing Degree', 'Digital Marketing Certification'])
ON CONFLICT (title) DO NOTHING;

-- Verify the data was inserted
SELECT 'Colleges inserted:' as info, COUNT(*) as count FROM colleges;
SELECT 'Courses inserted:' as info, COUNT(*) as count FROM courses;
SELECT 'Careers inserted:' as info, COUNT(*) as count FROM careers;

-- Show sample data
SELECT 'Sample Colleges:' as info;
SELECT name, city, state FROM colleges LIMIT 5;

SELECT 'Sample Courses:' as info;
SELECT title, category, level FROM courses LIMIT 5;

SELECT 'Sample Careers:' as info;
SELECT title, field, average_salary FROM careers LIMIT 5;
