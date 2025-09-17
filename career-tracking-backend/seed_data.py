import asyncio
from app.models import Course, Career, College, CourseCareer
from app.database import AsyncSessionLocal
from sqlalchemy import text
import json

# Sample data
SAMPLE_COURSES = [
    {
        "title": "Introduction to Python Programming",
        "description": "Learn Python fundamentals including variables, functions, loops, and object-oriented programming.",
        "duration": "8 weeks",
        "provider": "Coursera",
        "category": "Programming",
        "difficulty_level": "Beginner"
    },
    {
        "title": "Data Science with Python",
        "description": "Master data analysis, visualization, and machine learning using Python libraries like pandas, matplotlib, and scikit-learn.",
        "duration": "12 weeks",
        "provider": "edX",
        "category": "Data Science",
        "difficulty_level": "Intermediate"
    },
    {
        "title": "Web Development Bootcamp",
        "description": "Full-stack web development using HTML, CSS, JavaScript, React, Node.js, and MongoDB.",
        "duration": "16 weeks",
        "provider": "Udemy",
        "category": "Web Development",
        "difficulty_level": "Beginner"
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "Learn supervised and unsupervised learning algorithms, neural networks, and deep learning basics.",
        "duration": "10 weeks",
        "provider": "Coursera",
        "category": "Machine Learning",
        "difficulty_level": "Intermediate"
    },
    {
        "title": "Digital Marketing Mastery",
        "description": "Comprehensive course covering SEO, social media marketing, content marketing, and analytics.",
        "duration": "6 weeks",
        "provider": "Udacity",
        "category": "Marketing",
        "difficulty_level": "Beginner"
    },
    {
        "title": "Cybersecurity Essentials",
        "description": "Learn network security, ethical hacking, risk management, and security protocols.",
        "duration": "14 weeks",
        "provider": "Cisco",
        "category": "Cybersecurity",
        "difficulty_level": "Intermediate"
    },
    {
        "title": "Cloud Computing with AWS",
        "description": "Master Amazon Web Services including EC2, S3, Lambda, and cloud architecture.",
        "duration": "12 weeks",
        "provider": "AWS",
        "category": "Cloud Computing",
        "difficulty_level": "Advanced"
    },
    {
        "title": "Mobile App Development",
        "description": "Build native mobile apps for iOS and Android using React Native and Flutter.",
        "duration": "10 weeks",
        "provider": "Google",
        "category": "Mobile Development",
        "difficulty_level": "Intermediate"
    }
]

SAMPLE_CAREERS = [
    {
        "title": "Software Engineer",
        "description": "Design, develop, and maintain software applications and systems.",
        "field": "Technology",
        "median_salary": "$85,000 - $120,000",
        "job_outlook": "Growing (22% growth expected)",
        "required_skills": json.dumps(["Programming", "Problem Solving", "Software Design", "Testing", "Version Control"])
    },
    {
        "title": "Data Scientist",
        "description": "Analyze complex data to help organizations make informed business decisions.",
        "field": "Technology",
        "median_salary": "$95,000 - $140,000",
        "job_outlook": "Very High Growth (35% growth expected)",
        "required_skills": json.dumps(["Python/R", "Statistics", "Machine Learning", "Data Visualization", "SQL"])
    },
    {
        "title": "Digital Marketing Manager",
        "description": "Plan and execute digital marketing campaigns across various online platforms.",
        "field": "Marketing",
        "median_salary": "$65,000 - $95,000",
        "job_outlook": "Growing (10% growth expected)",
        "required_skills": json.dumps(["SEO/SEM", "Social Media", "Analytics", "Content Strategy", "PPC Advertising"])
    },
    {
        "title": "Cybersecurity Analyst",
        "description": "Protect organizations from cyber threats and security breaches.",
        "field": "Technology",
        "median_salary": "$80,000 - $115,000",
        "job_outlook": "Very High Growth (33% growth expected)",
        "required_skills": json.dumps(["Network Security", "Risk Assessment", "Incident Response", "Ethical Hacking", "Compliance"])
    },
    {
        "title": "UX/UI Designer",
        "description": "Design user interfaces and experiences for websites and mobile applications.",
        "field": "Design",
        "median_salary": "$70,000 - $105,000",
        "job_outlook": "Growing (13% growth expected)",
        "required_skills": json.dumps(["Design Tools", "User Research", "Prototyping", "Wireframing", "Usability Testing"])
    },
    {
        "title": "Cloud Solutions Architect",
        "description": "Design and implement cloud computing strategies for organizations.",
        "field": "Technology",
        "median_salary": "$120,000 - $180,000",
        "job_outlook": "Very High Growth (30% growth expected)",
        "required_skills": json.dumps(["Cloud Platforms", "System Architecture", "DevOps", "Security", "Cost Optimization"])
    },
    {
        "title": "Product Manager",
        "description": "Guide the development and strategy of products from conception to launch.",
        "field": "Business",
        "median_salary": "$90,000 - $140,000",
        "job_outlook": "Growing (15% growth expected)",
        "required_skills": json.dumps(["Product Strategy", "Market Research", "Project Management", "Analytics", "Communication"])
    },
    {
        "title": "DevOps Engineer",
        "description": "Bridge development and operations to improve software deployment and infrastructure.",
        "field": "Technology",
        "median_salary": "$95,000 - $135,000",
        "job_outlook": "Very High Growth (25% growth expected)",
        "required_skills": json.dumps(["CI/CD", "Containerization", "Infrastructure as Code", "Monitoring", "Automation"])
    }
]

SAMPLE_COLLEGES = [
    {
        "name": "Indian Institute of Technology Delhi",
        "address": "Hauz Khas, New Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110016",
        "website": "https://home.iitd.ac.in/",
        "latitude": 28.5449,
        "longitude": 77.1928
    },
    {
        "name": "Indian Institute of Technology Bombay",
        "address": "Powai, Mumbai",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400076",
        "website": "https://www.iitb.ac.in/",
        "latitude": 19.1334,
        "longitude": 72.9133
    },
    {
        "name": "Indian Institute of Science Bangalore",
        "address": "CV Raman Avenue, Bangalore",
        "city": "Bangalore",
        "state": "Karnataka",
        "pincode": "560012",
        "website": "https://www.iisc.ac.in/",
        "latitude": 13.0218,
        "longitude": 77.5671
    },
    {
        "name": "Delhi University",
        "address": "University Enclave, Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110007",
        "website": "https://www.du.ac.in/",
        "latitude": 28.6869,
        "longitude": 77.2090
    },
    {
        "name": "Jawaharlal Nehru University",
        "address": "New Mehrauli Road, New Delhi",
        "city": "New Delhi",
        "state": "Delhi",
        "pincode": "110067",
        "website": "https://www.jnu.ac.in/",
        "latitude": 28.5383,
        "longitude": 77.1641
    },
    {
        "name": "Anna University",
        "address": "Sardar Patel Road, Chennai",
        "city": "Chennai",
        "state": "Tamil Nadu",
        "pincode": "600025",
        "website": "https://www.annauniv.edu/",
        "latitude": 13.0067,
        "longitude": 80.2206
    },
    {
        "name": "Pune University",
        "address": "Ganeshkhind, Pune",
        "city": "Pune",
        "state": "Maharashtra",
        "pincode": "411007",
        "website": "http://www.unipune.ac.in/",
        "latitude": 18.5441,
        "longitude": 73.8250
    },
    {
        "name": "Jadavpur University",
        "address": "Raja S.C. Mallick Road, Kolkata",
        "city": "Kolkata",
        "state": "West Bengal",
        "pincode": "700032",
        "website": "http://www.jaduniv.edu.in/",
        "latitude": 22.4991,
        "longitude": 88.3705
    }
]

async def seed_database():
    """Seed the database with sample data"""
    # Use the existing AsyncSessionLocal from database module
    from app.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        try:
            # Clear existing data (optional - comment out if you want to keep existing data)
            await session.execute(text("DELETE FROM course_career"))
            await session.execute(text("DELETE FROM courses"))
            await session.execute(text("DELETE FROM careers"))
            await session.execute(text("DELETE FROM colleges"))
            await session.commit()
            
            # Add courses
            print("Adding courses...")
            for course_data in SAMPLE_COURSES:
                course = Course(**course_data)
                session.add(course)
            
            # Add careers
            print("Adding careers...")
            for career_data in SAMPLE_CAREERS:
                career = Career(**career_data)
                session.add(career)
            
            # Add colleges
            print("Adding colleges...")
            for college_data in SAMPLE_COLLEGES:
                college = College(**college_data)
                session.add(college)
            
            await session.commit()
            
            # Create course-career relationships
            print("Creating course-career relationships...")
            # Get all courses and careers
            courses = await session.execute(text("SELECT id FROM courses"))
            careers = await session.execute(text("SELECT id FROM careers"))
            
            course_ids = [row[0] for row in courses.fetchall()]
            career_ids = [row[0] for row in careers.fetchall()]
            
            # Create some logical relationships
            relationships = [
                (1, 1),  # Python Programming -> Software Engineer
                (1, 2),  # Python Programming -> Data Scientist
                (2, 2),  # Data Science -> Data Scientist
                (3, 1),  # Web Development -> Software Engineer
                (3, 5),  # Web Development -> UX/UI Designer
                (4, 2),  # Machine Learning -> Data Scientist
                (5, 3),  # Digital Marketing -> Digital Marketing Manager
                (6, 4),  # Cybersecurity -> Cybersecurity Analyst
                (7, 6),  # Cloud Computing -> Cloud Solutions Architect
                (7, 8),  # Cloud Computing -> DevOps Engineer
                (8, 1),  # Mobile Development -> Software Engineer
            ]
            
            for course_id, career_id in relationships:
                if course_id <= len(course_ids) and career_id <= len(career_ids):
                    relationship = CourseCareer(course_id=course_id, career_id=career_id)
                    session.add(relationship)
            
            await session.commit()
            print("Database seeded successfully!")
            
        except Exception as e:
            print(f"Error seeding database: {e}")
            await session.rollback()
        finally:
            await session.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
