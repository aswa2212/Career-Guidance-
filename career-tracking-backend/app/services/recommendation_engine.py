import json
import os
from typing import List, Dict, Any, Optional
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Try to import ML dependencies, fall back to basic functionality if not available
try:
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    ML_AVAILABLE = True
except ImportError as e:
    logging.warning(f"ML dependencies not available: {e}. Using fallback recommendations.")
    ML_AVAILABLE = False
    # Create dummy classes for type hints
    pd = None
    np = None

logger = logging.getLogger(__name__)

class RecommendationEngine:
    def __init__(self):
        self.courses_df = None
        self.user_aptitude_df = None
        self.user_interests = None
        self.tfidf_vectorizer = None
        self.course_vectors = None
        self.data_loaded = False
        
    async def load_data_from_db(self, db: AsyncSession):
        """Load data from database for recommendation engine"""
        try:
            if not ML_AVAILABLE:
                logger.warning("ML dependencies not available, using basic fallback")
                self.data_loaded = True
                return True
            
            # Import services
            from app.services.course_service import CourseService
            
            # Load courses from database
            courses = await CourseService.get_all_courses(db, limit=1000)
            
            if not courses:
                logger.warning("No courses found in database, using fallback")
                return False
            
            # Convert to DataFrame format for ML processing
            courses_data = []
            for course in courses:
                courses_data.append({
                    'course_id': course.id,
                    'course_name': course.title,
                    'description': course.description or '',
                    'required_skills': course.category or '',  # Using category as skills for now
                    'career_paths': course.provider or '',     # Using provider as career paths for now
                    'duration': course.duration or '',
                    'level': course.difficulty_level or 'Beginner',
                    'relevant_aptitude_areas': course.category or ''  # Using category for aptitude mapping
                })
            
            self.courses_df = pd.DataFrame(courses_data)
            logger.info(f"Loaded {len(self.courses_df)} courses from database")
            
            # Prepare TF-IDF vectors for courses
            self._prepare_course_vectors()
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading data from database: {str(e)}")
            return False

    def load_data(self):
        """Load mock datasets for recommendation engine (fallback method)"""
        try:
            if not ML_AVAILABLE:
                logger.warning("ML dependencies not available, using basic fallback")
                self.data_loaded = True
                return True
            
            # Get the data directory path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            data_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'data')
            
            # Load courses data
            courses_path = os.path.join(data_dir, 'courses.csv')
            if os.path.exists(courses_path):
                self.courses_df = pd.read_csv(courses_path)
                logger.info(f"Loaded {len(self.courses_df)} courses from CSV")
            else:
                logger.warning(f"Courses file not found at {courses_path}")
                return False
            
            # Load user aptitude data
            aptitude_path = os.path.join(data_dir, 'user_aptitude.csv')
            if os.path.exists(aptitude_path):
                self.user_aptitude_df = pd.read_csv(aptitude_path)
                logger.info(f"Loaded aptitude data for {len(self.user_aptitude_df['user_id'].unique())} users")
            else:
                logger.warning(f"Aptitude file not found at {aptitude_path}")
                # Create mock aptitude data
                self.user_aptitude_df = None
            
            # Load user interests data
            interests_path = os.path.join(data_dir, 'user_interests.json')
            if os.path.exists(interests_path):
                with open(interests_path, 'r') as f:
                    self.user_interests = json.load(f)
                logger.info(f"Loaded interests for {len(self.user_interests)} users")
            else:
                logger.warning(f"Interests file not found at {interests_path}")
                self.user_interests = {}
            
            # Prepare TF-IDF vectors for courses
            self._prepare_course_vectors()
            
            self.data_loaded = True
            return True
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            return False
    
    def _prepare_course_vectors(self):
        """Prepare TF-IDF vectors for course descriptions and skills"""
        try:
            # Combine course description, required skills, and career paths for better matching
            course_texts = []
            for _, course in self.courses_df.iterrows():
                text = f"{course['description']} {course['required_skills']} {course['career_paths']}"
                course_texts.append(text.lower())
            
            # Create TF-IDF vectors
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            self.course_vectors = self.tfidf_vectorizer.fit_transform(course_texts)
            logger.info("Course TF-IDF vectors prepared successfully")
            
        except Exception as e:
            logger.error(f"Error preparing course vectors: {str(e)}")
            raise
    
    def get_user_profile_vector(self, user_interests: List[str], user_aptitude: Dict[str, float]) -> np.ndarray:
        """Create a user profile vector based on interests and top aptitude areas"""
        try:
            # Get top aptitude areas (scores above 80)
            top_aptitudes = [area for area, score in user_aptitude.items() if score >= 80]
            
            # Combine interests and top aptitudes
            user_profile_text = " ".join(user_interests + top_aptitudes).lower()
            
            # Transform using the same vectorizer
            user_vector = self.tfidf_vectorizer.transform([user_profile_text])
            
            return user_vector
            
        except Exception as e:
            logger.error(f"Error creating user profile vector: {str(e)}")
            raise
    
    def calculate_aptitude_bonus(self, course_aptitudes: str, user_aptitude: Dict[str, float]) -> float:
        """Calculate bonus score based on user's aptitude alignment with course requirements"""
        try:
            if pd.isna(course_aptitudes):
                return 0.0
            
            # Parse course required aptitudes
            required_aptitudes = [apt.strip() for apt in course_aptitudes.split(',')]
            
            # Calculate average score for required aptitudes
            relevant_scores = []
            for apt in required_aptitudes:
                if apt in user_aptitude:
                    relevant_scores.append(user_aptitude[apt])
            
            if relevant_scores:
                # Normalize to 0-1 scale and apply as bonus
                avg_score = np.mean(relevant_scores)
                return (avg_score / 100.0) * 0.3  # 30% weight for aptitude alignment
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating aptitude bonus: {str(e)}")
            return 0.0
    
    async def get_user_interests_from_db(self, user_id: int, db: AsyncSession) -> List[str]:
        """Get user interests from database"""
        try:
            from app.models.user import User
            result = await db.execute(select(User).filter(User.id == user_id))
            user = result.scalars().first()
            
            if user and user.interests:
                return user.interests
            return []
        except Exception as e:
            logger.error(f"Error fetching user interests from database: {str(e)}")
            return []

    async def get_recommendations(self, user_interests: List[str], user_id: Optional[int] = None, top_k: int = 10, db: Optional[AsyncSession] = None) -> List[Dict[str, Any]]:
        """Get personalized course recommendations for a user"""
        try:
            # Try to load data from database first
            if db and not self.data_loaded:
                if not await self.load_data_from_db(db):
                    # Fallback to CSV data
                    if not self.load_data():
                        return self._get_fallback_recommendations(top_k)
            elif not self.data_loaded:
                if not self.load_data():
                    return self._get_fallback_recommendations(top_k)
            
            # If ML dependencies are not available, return fallback recommendations
            if not ML_AVAILABLE:
                return self._get_fallback_recommendations(top_k)
            
            # Get user aptitude data (use mock data if user_id not found)
            user_aptitude = {}
            if user_id and self.user_aptitude_df is not None:
                user_apt_data = self.user_aptitude_df[self.user_aptitude_df['user_id'] == user_id]
                if not user_apt_data.empty:
                    user_aptitude = dict(zip(user_apt_data['aptitude_area'], user_apt_data['score']))
            
            # Use default aptitude scores if no data found
            if not user_aptitude:
                user_aptitude = {
                    'Logical Reasoning': 75,
                    'Quantitative': 70,
                    'Verbal': 72,
                    'Technical': 78,
                    'Creative': 68,
                    'Analytical': 76,
                    'Communication': 74,
                    'Leadership': 70,
                    'Problem Solving': 77,
                    'Spatial': 73
                }
            
            # Create user profile vector
            user_vector = self.get_user_profile_vector(user_interests, user_aptitude)
            
            # Calculate cosine similarity with all courses
            similarities = cosine_similarity(user_vector, self.course_vectors).flatten()
            
            # Calculate final scores with aptitude bonus
            final_scores = []
            for idx, similarity in enumerate(similarities):
                course = self.courses_df.iloc[idx]
                aptitude_bonus = self.calculate_aptitude_bonus(
                    course['relevant_aptitude_areas'], 
                    user_aptitude
                )
                final_score = similarity + aptitude_bonus
                final_scores.append((idx, final_score))
            
            # Sort by final score and get top recommendations
            final_scores.sort(key=lambda x: x[1], reverse=True)
            top_recommendations = final_scores[:top_k]
            
            # Format recommendations
            recommendations = []
            for idx, final_score in top_recommendations:
                course = self.courses_df.iloc[idx]
                similarity_score = similarities[idx]
                
                # Calculate match percentage properly
                # Handle edge cases where final_score might be very close to 1.0
                match_percentage = round(final_score * 100)
                match_percentage = max(0, min(match_percentage, 100))  # Ensure it's between 0-100
                
                # Debug logging for high scores
                if final_score > 0.95:
                    logger.info(f"High match found: {course['course_name']} - Final Score: {final_score:.4f}, Match %: {match_percentage}%")
                
                recommendation = {
                    'course_id': int(course['course_id']),
                    'course_name': course['course_name'],
                    'description': course['description'],
                    'required_skills': course['required_skills'].split(',') if pd.notna(course['required_skills']) else [],
                    'career_paths': course['career_paths'].split(',') if pd.notna(course['career_paths']) else [],
                    'duration': course['duration'],
                    'level': course['level'],
                    'similarity_score': float(similarity_score),
                    'final_score': float(final_score),
                    'match_percentage': match_percentage
                }
                recommendations.append(recommendation)
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations(top_k)
    
    def get_course_by_id(self, course_id: int) -> Optional[Dict[str, Any]]:
        """Get course details by ID"""
        try:
            if not self.data_loaded:
                if not self.load_data():
                    return None
            
            course_data = self.courses_df[self.courses_df['course_id'] == course_id]
            if course_data.empty:
                return None
            
            course = course_data.iloc[0]
            return {
                'course_id': int(course['course_id']),
                'course_name': course['course_name'],
                'description': course['description'],
                'required_skills': course['required_skills'].split(',') if pd.notna(course['required_skills']) else [],
                'career_paths': course['career_paths'].split(',') if pd.notna(course['career_paths']) else [],
                'duration': course['duration'],
                'level': course['level']
            }
            
        except Exception as e:
            logger.error(f"Error getting course by ID: {str(e)}")
            return None
    
    def _get_fallback_recommendations(self, top_k: int = 10) -> List[Dict[str, Any]]:
        """Provide fallback recommendations when ML engine is not available"""
        fallback_courses = [
            {
                "course_id": 1,
                "course_name": "Computer Science Engineering",
                "description": "Comprehensive program covering programming, algorithms, data structures, and software engineering",
                "required_skills": ["Programming", "Algorithms", "Data Structures", "Software Engineering"],
                "career_paths": ["Software Developer", "Data Scientist", "System Architect", "Tech Lead"],
                "duration": "4 years",
                "level": "Undergraduate",
                "similarity_score": 0.85,
                "final_score": 0.90,
                "match_percentage": 90
            },
            {
                "course_id": 2,
                "course_name": "Data Science",
                "description": "Master data analysis, machine learning, statistics, and big data technologies",
                "required_skills": ["Python", "Statistics", "Machine Learning", "Data Analysis"],
                "career_paths": ["Data Scientist", "ML Engineer", "Business Analyst", "Research Scientist"],
                "duration": "2 years",
                "level": "Postgraduate",
                "similarity_score": 0.82,
                "final_score": 0.87,
                "match_percentage": 87
            },
            {
                "course_id": 4,
                "course_name": "Web Development",
                "description": "Full-stack web development with modern frameworks and technologies",
                "required_skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
                "career_paths": ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Web Designer"],
                "duration": "6 months",
                "level": "Certificate",
                "similarity_score": 0.78,
                "final_score": 0.83,
                "match_percentage": 83
            },
            {
                "course_id": 3,
                "course_name": "Artificial Intelligence",
                "description": "Advanced AI concepts including neural networks, deep learning, and cognitive computing",
                "required_skills": ["Python", "Mathematics", "Neural Networks", "Deep Learning"],
                "career_paths": ["AI Engineer", "ML Researcher", "Robotics Engineer", "AI Consultant"],
                "duration": "2 years",
                "level": "Postgraduate",
                "similarity_score": 0.80,
                "final_score": 0.82,
                "match_percentage": 82
            },
            {
                "course_id": 5,
                "course_name": "Mobile App Development",
                "description": "Native and cross-platform mobile application development",
                "required_skills": ["Java", "Kotlin", "Swift", "React Native"],
                "career_paths": ["Mobile Developer", "App Designer", "iOS Developer", "Android Developer"],
                "duration": "8 months",
                "level": "Certificate",
                "similarity_score": 0.75,
                "final_score": 0.80,
                "match_percentage": 80
            },
            {
                "course_id": 6,
                "course_name": "Cybersecurity",
                "description": "Information security, ethical hacking, and network security fundamentals",
                "required_skills": ["Network Security", "Ethical Hacking", "Cryptography"],
                "career_paths": ["Security Analyst", "Ethical Hacker", "Security Consultant", "CISO"],
                "duration": "1 year",
                "level": "Certificate",
                "similarity_score": 0.73,
                "final_score": 0.78,
                "match_percentage": 78
            }
        ]
        
        return fallback_courses[:top_k]

# Global instance
recommendation_engine = RecommendationEngine()
