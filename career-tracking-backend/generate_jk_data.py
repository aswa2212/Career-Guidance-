#!/usr/bin/env python3
"""
J&K Data Generator
Creates JSON files with J&K colleges and aptitude questions for ML model
"""

import json
import os
from datetime import datetime

def create_jk_colleges_data():
    """Create comprehensive J&K colleges data"""
    colleges = [
        {
            'id': 1,
            'name': 'University of Kashmir',
            'address': 'Hazratbal, Srinagar, Jammu and Kashmir, India',
            'city': 'Srinagar',
            'state': 'Jammu and Kashmir',
            'pincode': '190006',
            'website': 'https://www.kashmiruniversity.net',
            'latitude': 34.1269,
            'longitude': 74.8370,
            'scholarship_details': 'UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships available.',
            'type': 'University',
            'established': '1948',
            'courses_offered': 'Arts, Science, Commerce, Engineering, Medical, Law, Management'
        },
        {
            'id': 2,
            'name': 'University of Jammu',
            'address': 'Baba Saheb Ambedkar Road, Jammu, Jammu and Kashmir, India',
            'city': 'Jammu',
            'state': 'Jammu and Kashmir',
            'pincode': '180006',
            'website': 'https://www.jammuuniversity.ac.in',
            'latitude': 32.7266,
            'longitude': 74.8570,
            'scholarship_details': 'UGC scholarships, Merit scholarships, SC/ST/OBC scholarships, State government scholarships available.',
            'type': 'University',
            'established': '1969',
            'courses_offered': 'Arts, Science, Commerce, Engineering, Medical, Law, Management'
        },
        {
            'id': 3,
            'name': 'Central University of Kashmir',
            'address': 'Nunar, Ganderbal, Jammu and Kashmir, India',
            'city': 'Ganderbal',
            'state': 'Jammu and Kashmir',
            'pincode': '191201',
            'website': 'https://www.cukashmir.ac.in',
            'latitude': 34.2307,
            'longitude': 74.7847,
            'scholarship_details': 'Central government scholarships, UGC scholarships, Merit scholarships, Research fellowships available.',
            'type': 'Central University',
            'established': '2009',
            'courses_offered': 'Arts, Science, Commerce, Engineering, Management, Research'
        },
        {
            'id': 4,
            'name': 'Central University of Jammu',
            'address': 'Bagla, Rahya-Suchani, Samba, Jammu and Kashmir, India',
            'city': 'Samba',
            'state': 'Jammu and Kashmir',
            'pincode': '181143',
            'website': 'https://www.cujammu.ac.in',
            'latitude': 32.5625,
            'longitude': 75.1194,
            'scholarship_details': 'Central government scholarships, UGC scholarships, Merit scholarships, Research fellowships available.',
            'type': 'Central University',
            'established': '2011',
            'courses_offered': 'Arts, Science, Commerce, Engineering, Management, Research'
        },
        {
            'id': 5,
            'name': 'National Institute of Technology Srinagar',
            'address': 'Hazratbal, Srinagar, Jammu and Kashmir, India',
            'city': 'Srinagar',
            'state': 'Jammu and Kashmir',
            'pincode': '190006',
            'website': 'https://www.nitsri.ac.in',
            'latitude': 34.1269,
            'longitude': 74.8370,
            'scholarship_details': 'Technical education scholarships, Merit scholarships, Industry scholarships, JEE-based scholarships available.',
            'type': 'Engineering Institute',
            'established': '1960',
            'courses_offered': 'Engineering, Technology, Computer Science, Electronics'
        },
        {
            'id': 6,
            'name': 'Government Medical College Srinagar',
            'address': 'Karan Nagar, Srinagar, Jammu and Kashmir, India',
            'city': 'Srinagar',
            'state': 'Jammu and Kashmir',
            'pincode': '190010',
            'website': 'https://www.gmcsrinagar.edu.in',
            'latitude': 34.0837,
            'longitude': 74.7973,
            'scholarship_details': 'Medical education scholarships, NEET-based scholarships, Government medical scholarships available.',
            'type': 'Medical College',
            'established': '1959',
            'courses_offered': 'MBBS, MD, MS, Nursing, Paramedical'
        },
        {
            'id': 7,
            'name': 'Government Medical College Jammu',
            'address': 'Sector 5, Bhagwati Nagar, Jammu, Jammu and Kashmir, India',
            'city': 'Jammu',
            'state': 'Jammu and Kashmir',
            'pincode': '180016',
            'website': 'https://www.gmcjammu.nic.in',
            'latitude': 32.7266,
            'longitude': 74.8570,
            'scholarship_details': 'Medical education scholarships, NEET-based scholarships, Government medical scholarships available.',
            'type': 'Medical College',
            'established': '1973',
            'courses_offered': 'MBBS, MD, MS, Nursing, Paramedical'
        },
        {
            'id': 8,
            'name': 'Government Degree College Srinagar',
            'address': 'M.A. Road, Srinagar, Jammu and Kashmir, India',
            'city': 'Srinagar',
            'state': 'Jammu and Kashmir',
            'pincode': '190001',
            'website': 'https://www.gdcsrinagar.edu.in',
            'latitude': 34.0837,
            'longitude': 74.7973,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1950',
            'courses_offered': 'BA, BSc, BCom, MA, MSc, MCom'
        },
        {
            'id': 9,
            'name': 'Government Degree College Jammu',
            'address': 'Canal Road, Jammu, Jammu and Kashmir, India',
            'city': 'Jammu',
            'state': 'Jammu and Kashmir',
            'pincode': '180001',
            'website': 'https://www.gdcjammu.edu.in',
            'latitude': 32.7266,
            'longitude': 74.8570,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1948',
            'courses_offered': 'BA, BSc, BCom, MA, MSc, MCom'
        },
        {
            'id': 10,
            'name': 'Government College for Women Srinagar',
            'address': 'M.A. Road, Srinagar, Jammu and Kashmir, India',
            'city': 'Srinagar',
            'state': 'Jammu and Kashmir',
            'pincode': '190001',
            'website': 'https://www.gcwsrinagar.edu.in',
            'latitude': 34.0837,
            'longitude': 74.7973,
            'scholarship_details': 'Women empowerment scholarships, Merit scholarships, State government scholarships available.',
            'type': 'Women College',
            'established': '1950',
            'courses_offered': 'BA, BSc, BCom, MA, MSc, MCom, BEd'
        },
        {
            'id': 11,
            'name': 'Government Degree College Anantnag',
            'address': 'Anantnag, Jammu and Kashmir, India',
            'city': 'Anantnag',
            'state': 'Jammu and Kashmir',
            'pincode': '192101',
            'website': 'https://www.gdcanantnag.edu.in',
            'latitude': 33.7311,
            'longitude': 75.1480,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1955',
            'courses_offered': 'BA, BSc, BCom, MA, MSc'
        },
        {
            'id': 12,
            'name': 'Government Degree College Baramulla',
            'address': 'Baramulla, Jammu and Kashmir, India',
            'city': 'Baramulla',
            'state': 'Jammu and Kashmir',
            'pincode': '193101',
            'website': 'https://www.gdcbaramulla.edu.in',
            'latitude': 34.2094,
            'longitude': 74.3428,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1958',
            'courses_offered': 'BA, BSc, BCom, MA, MSc'
        },
        {
            'id': 13,
            'name': 'Government Degree College Kupwara',
            'address': 'Kupwara, Jammu and Kashmir, India',
            'city': 'Kupwara',
            'state': 'Jammu and Kashmir',
            'pincode': '193222',
            'website': 'https://www.gdckupwara.edu.in',
            'latitude': 34.5267,
            'longitude': 74.2467,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1965',
            'courses_offered': 'BA, BSc, BCom'
        },
        {
            'id': 14,
            'name': 'Government Degree College Pulwama',
            'address': 'Pulwama, Jammu and Kashmir, India',
            'city': 'Pulwama',
            'state': 'Jammu and Kashmir',
            'pincode': '192301',
            'website': 'https://www.gdcpulwama.edu.in',
            'latitude': 33.8712,
            'longitude': 74.8947,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1962',
            'courses_offered': 'BA, BSc, BCom'
        },
        {
            'id': 15,
            'name': 'Government Degree College Kathua',
            'address': 'Kathua, Jammu and Kashmir, India',
            'city': 'Kathua',
            'state': 'Jammu and Kashmir',
            'pincode': '184101',
            'website': 'https://www.gdckathua.edu.in',
            'latitude': 32.3705,
            'longitude': 75.5224,
            'scholarship_details': 'State government scholarships, Merit scholarships, Need-based financial assistance available.',
            'type': 'Degree College',
            'established': '1960',
            'courses_offered': 'BA, BSc, BCom, MA, MSc'
        }
    ]
    
    return colleges

def create_aptitude_questions_data():
    """Create comprehensive aptitude questions for ML model"""
    questions = [
        # Mathematics Questions
        {
            'id': 1,
            'question': 'If 2x + 3 = 11, what is the value of x?',
            'options': ['A) 3', 'B) 4', 'C) 5', 'D) 6'],
            'correct_answer': 'B',
            'subject': 'Mathematics',
            'difficulty': 'Easy',
            'topic': 'Algebra',
            'explanation': 'Solving: 2x + 3 = 11, 2x = 8, x = 4',
            'source': 'Educational Database',
            'career_relevance': 'Engineering, Data Science, Finance, Research, Teaching'
        },
        {
            'id': 2,
            'question': 'What is the area of a circle with radius 7 cm?',
            'options': ['A) 154 cm²', 'B) 144 cm²', 'C) 164 cm²', 'D) 174 cm²'],
            'correct_answer': 'A',
            'subject': 'Mathematics',
            'difficulty': 'Medium',
            'topic': 'Geometry',
            'explanation': 'Area = πr² = (22/7) × 7² = 154 cm²',
            'source': 'Educational Database',
            'career_relevance': 'Engineering, Data Science, Finance, Research, Teaching'
        },
        {
            'id': 3,
            'question': 'If log₂(8) = x, what is the value of x?',
            'options': ['A) 2', 'B) 3', 'C) 4', 'D) 8'],
            'correct_answer': 'B',
            'subject': 'Mathematics',
            'difficulty': 'Medium',
            'topic': 'Logarithms',
            'explanation': 'log₂(8) = log₂(2³) = 3',
            'source': 'Educational Database',
            'career_relevance': 'Engineering, Data Science, Finance, Research, Teaching'
        },
        
        # Physics Questions
        {
            'id': 4,
            'question': 'What is the SI unit of force?',
            'options': ['A) Joule', 'B) Newton', 'C) Watt', 'D) Pascal'],
            'correct_answer': 'B',
            'subject': 'Physics',
            'difficulty': 'Easy',
            'topic': 'Mechanics',
            'explanation': 'Newton (N) is the SI unit of force',
            'source': 'Educational Database',
            'career_relevance': 'Engineering, Research, Astronomy, Medical Physics, Teaching'
        },
        {
            'id': 5,
            'question': 'What is the acceleration due to gravity on Earth?',
            'options': ['A) 9.8 m/s²', 'B) 10 m/s²', 'C) 8.9 m/s²', 'D) 11 m/s²'],
            'correct_answer': 'A',
            'subject': 'Physics',
            'difficulty': 'Easy',
            'topic': 'Mechanics',
            'explanation': 'The acceleration due to gravity on Earth is approximately 9.8 m/s²',
            'source': 'Educational Database',
            'career_relevance': 'Engineering, Research, Astronomy, Medical Physics, Teaching'
        },
        
        # Chemistry Questions
        {
            'id': 6,
            'question': 'What is the chemical symbol for Gold?',
            'options': ['A) Go', 'B) Au', 'C) Ag', 'D) Gd'],
            'correct_answer': 'B',
            'subject': 'Chemistry',
            'difficulty': 'Easy',
            'topic': 'Periodic Table',
            'explanation': 'Au is the chemical symbol for Gold (from Latin: Aurum)',
            'source': 'Educational Database',
            'career_relevance': 'Chemical Engineering, Pharmaceuticals, Research, Medicine, Teaching'
        },
        {
            'id': 7,
            'question': 'What is the pH of pure water at 25°C?',
            'options': ['A) 6', 'B) 7', 'C) 8', 'D) 9'],
            'correct_answer': 'B',
            'subject': 'Chemistry',
            'difficulty': 'Easy',
            'topic': 'Acids and Bases',
            'explanation': 'Pure water has a pH of 7, which is neutral',
            'source': 'Educational Database',
            'career_relevance': 'Chemical Engineering, Pharmaceuticals, Research, Medicine, Teaching'
        },
        
        # Biology Questions
        {
            'id': 8,
            'question': 'What is the powerhouse of the cell?',
            'options': ['A) Nucleus', 'B) Mitochondria', 'C) Ribosome', 'D) Chloroplast'],
            'correct_answer': 'B',
            'subject': 'Biology',
            'difficulty': 'Easy',
            'topic': 'Cell Biology',
            'explanation': 'Mitochondria are called the powerhouse of the cell as they produce ATP',
            'source': 'Educational Database',
            'career_relevance': 'Medicine, Biotechnology, Research, Environmental Science, Teaching'
        },
        {
            'id': 9,
            'question': 'How many chambers does a human heart have?',
            'options': ['A) 2', 'B) 3', 'C) 4', 'D) 5'],
            'correct_answer': 'C',
            'subject': 'Biology',
            'difficulty': 'Easy',
            'topic': 'Human Physiology',
            'explanation': 'The human heart has 4 chambers: 2 atria and 2 ventricles',
            'source': 'Educational Database',
            'career_relevance': 'Medicine, Biotechnology, Research, Environmental Science, Teaching'
        },
        
        # Computer Science Questions
        {
            'id': 10,
            'question': 'What does CPU stand for?',
            'options': ['A) Central Processing Unit', 'B) Computer Personal Unit', 'C) Central Program Unit', 'D) Computer Processing Unit'],
            'correct_answer': 'A',
            'subject': 'Computer Science',
            'difficulty': 'Easy',
            'topic': 'Computer Hardware',
            'explanation': 'CPU stands for Central Processing Unit',
            'source': 'Educational Database',
            'career_relevance': 'Software Development, Data Science, Cybersecurity, AI/ML, IT'
        },
        {
            'id': 11,
            'question': 'Which of the following is a programming language?',
            'options': ['A) HTML', 'B) Python', 'C) CSS', 'D) HTTP'],
            'correct_answer': 'B',
            'subject': 'Computer Science',
            'difficulty': 'Easy',
            'topic': 'Programming',
            'explanation': 'Python is a programming language, while HTML and CSS are markup languages, and HTTP is a protocol',
            'source': 'Educational Database',
            'career_relevance': 'Software Development, Data Science, Cybersecurity, AI/ML, IT'
        },
        
        # English Questions
        {
            'id': 12,
            'question': 'What is the synonym of "Happy"?',
            'options': ['A) Sad', 'B) Joyful', 'C) Angry', 'D) Tired'],
            'correct_answer': 'B',
            'subject': 'English',
            'difficulty': 'Easy',
            'topic': 'Vocabulary',
            'explanation': 'Joyful is a synonym of Happy',
            'source': 'Educational Database',
            'career_relevance': 'Literature, Journalism, Content Writing, Teaching, Communications'
        },
        {
            'id': 13,
            'question': 'What is the past tense of "run"?',
            'options': ['A) Runned', 'B) Ran', 'C) Running', 'D) Runs'],
            'correct_answer': 'B',
            'subject': 'English',
            'difficulty': 'Easy',
            'topic': 'Grammar',
            'explanation': 'The past tense of "run" is "ran"',
            'source': 'Educational Database',
            'career_relevance': 'Literature, Journalism, Content Writing, Teaching, Communications'
        },
        
        # Logical Reasoning Questions
        {
            'id': 14,
            'question': 'What comes next in the series: 2, 4, 8, 16, ?',
            'options': ['A) 24', 'B) 32', 'C) 20', 'D) 18'],
            'correct_answer': 'B',
            'subject': 'Logical Reasoning',
            'difficulty': 'Easy',
            'topic': 'Number Series',
            'explanation': 'Each number is doubled: 2×2=4, 4×2=8, 8×2=16, 16×2=32',
            'source': 'Educational Database',
            'career_relevance': 'Management, Law, Consulting, Problem Solving, Analytics'
        },
        {
            'id': 15,
            'question': 'If all roses are flowers and some flowers are red, which statement is correct?',
            'options': ['A) All roses are red', 'B) Some roses may be red', 'C) No roses are red', 'D) All flowers are roses'],
            'correct_answer': 'B',
            'subject': 'Logical Reasoning',
            'difficulty': 'Medium',
            'topic': 'Syllogism',
            'explanation': 'Since some flowers are red and all roses are flowers, some roses may be red',
            'source': 'Educational Database',
            'career_relevance': 'Management, Law, Consulting, Problem Solving, Analytics'
        }
    ]
    
    return questions

def create_ml_dataset(colleges, questions):
    """Create ML training dataset"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Group questions by subject
    questions_by_subject = {}
    for question in questions:
        subject = question['subject']
        if subject not in questions_by_subject:
            questions_by_subject[subject] = []
        questions_by_subject[subject].append(question)
    
    # Group colleges by type
    colleges_by_type = {}
    for college in colleges:
        college_type = college['type']
        if college_type not in colleges_by_type:
            colleges_by_type[college_type] = []
        colleges_by_type[college_type].append(college)
    
    ml_dataset = {
        'metadata': {
            'created_at': timestamp,
            'total_colleges': len(colleges),
            'total_questions': len(questions),
            'subjects': list(questions_by_subject.keys()),
            'college_types': list(colleges_by_type.keys()),
            'purpose': 'J&K Student Career Guidance ML Model Training'
        },
        'colleges': {
            'all_colleges': colleges,
            'by_type': colleges_by_type,
            'by_city': {}
        },
        'aptitude_questions': {
            'all_questions': questions,
            'by_subject': questions_by_subject
        },
        'statistics': {
            'colleges_by_city': {},
            'questions_by_subject': {},
            'questions_by_difficulty': {}
        }
    }
    
    # Calculate statistics
    for college in colleges:
        city = college['city']
        ml_dataset['statistics']['colleges_by_city'][city] = ml_dataset['statistics']['colleges_by_city'].get(city, 0) + 1
        
        if city not in ml_dataset['colleges']['by_city']:
            ml_dataset['colleges']['by_city'][city] = []
        ml_dataset['colleges']['by_city'][city].append(college)
    
    for question in questions:
        subject = question['subject']
        difficulty = question['difficulty']
        ml_dataset['statistics']['questions_by_subject'][subject] = ml_dataset['statistics']['questions_by_subject'].get(subject, 0) + 1
        ml_dataset['statistics']['questions_by_difficulty'][difficulty] = ml_dataset['statistics']['questions_by_difficulty'].get(difficulty, 0) + 1
    
    return ml_dataset

def main():
    """Generate J&K data files"""
    print("🏫 Generating J&K Colleges and Aptitude Questions Data...")
    
    # Create data directory
    os.makedirs('jk_data_generated', exist_ok=True)
    
    # Generate data
    colleges = create_jk_colleges_data()
    questions = create_aptitude_questions_data()
    ml_dataset = create_ml_dataset(colleges, questions)
    
    # Save individual files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save colleges
    colleges_file = f'jk_data_generated/jk_colleges_{timestamp}.json'
    with open(colleges_file, 'w', encoding='utf-8') as f:
        json.dump(colleges, f, indent=2, ensure_ascii=False)
    
    # Save questions
    questions_file = f'jk_data_generated/aptitude_questions_{timestamp}.json'
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    
    # Save ML dataset
    ml_file = f'jk_data_generated/ml_training_dataset_{timestamp}.json'
    with open(ml_file, 'w', encoding='utf-8') as f:
        json.dump(ml_dataset, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("=" * 60)
    print("✅ J&K DATA GENERATION COMPLETE")
    print("=" * 60)
    print(f"📁 Files saved in: jk_data_generated/")
    print(f"🏫 J&K Colleges: {len(colleges)}")
    print(f"🧠 Aptitude Questions: {len(questions)}")
    print(f"📊 ML Dataset: Complete with statistics")
    
    print("\n🏫 COLLEGES BY CITY:")
    for city, count in ml_dataset['statistics']['colleges_by_city'].items():
        print(f"  {city}: {count} colleges")
    
    print("\n🧠 QUESTIONS BY SUBJECT:")
    for subject, count in ml_dataset['statistics']['questions_by_subject'].items():
        print(f"  {subject}: {count} questions")
    
    print("\n📊 QUESTIONS BY DIFFICULTY:")
    for difficulty, count in ml_dataset['statistics']['questions_by_difficulty'].items():
        print(f"  {difficulty}: {count} questions")
    
    print(f"\n📝 Files created:")
    print(f"  - {colleges_file}")
    print(f"  - {questions_file}")
    print(f"  - {ml_file}")
    
    print("\n🎯 Ready for ML model training!")
    print("🔄 You can now use this data to enhance your AI recommendation system.")

if __name__ == "__main__":
    main()
