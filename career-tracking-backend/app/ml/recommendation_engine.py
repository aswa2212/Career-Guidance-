import joblib
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
import os

class RecommendationEngine:
    def __init__(self):
        # Get the current directory and build model paths
        current_dir = Path(__file__).parent
        model_path = current_dir / "models" / "career_recommender.pkl"
        course_features_path = current_dir / "models" / "course_features.pkl"
        
        # Load models if they exist, otherwise use fallback
        try:
            if model_path.exists():
                self.career_data = joblib.load(model_path)
            else:
                self.career_data = None
                
            if course_features_path.exists():
                self.course_features = joblib.load(course_features_path)
            else:
                self.course_features = None
        except Exception as e:
            print(f"Error loading models: {e}")
            self.career_data = None
            self.course_features = None

    def get_career_recommendations(self, user_skills):
        """
        Get career recommendations based on user skills
        user_skills: dict with keys like 'programming_interest', 'math_skills', etc.
        """
        if not self.career_data:
            # Fallback recommendations
            return [1, 2, 3]  # Return career IDs
        
        try:
            # Convert user skills to feature vector
            features = [
                user_skills.get('programming_interest', 3),
                user_skills.get('math_skills', 3),
                user_skills.get('communication_skills', 3),
                user_skills.get('creativity', 3),
                user_skills.get('analytical_thinking', 3),
                user_skills.get('leadership', 3)
            ]
            
            # Use simple data structure
            probabilities = self.career_data['probabilities']
            career_classes = self.career_data['classes']
            
            # Get top 3 career recommendations
            top_indices = np.argsort(probabilities)[-3:][::-1]
            
            return [int(career_classes[i]) for i in top_indices]
        except Exception as e:
            print(f"Error in career recommendation: {e}")
            return [1, 2, 3]  # Fallback

    def get_course_recommendations(self, user_preferences, career_id=None):
        """
        Get course recommendations based on user preferences and optionally career
        """
        if self.course_features is None:
            # Fallback recommendations
            return [1, 2, 3]  # Return course IDs
        
        try:
            # Create user preference vector
            user_vector = np.array([
                user_preferences.get('programming_interest', 0.5),
                user_preferences.get('math_interest', 0.5),
                user_preferences.get('business_interest', 0.5),
                user_preferences.get('design_interest', 0.5),
                user_preferences.get('security_interest', 0.5)
            ]).reshape(1, -1)
            
            # Calculate similarity with all courses
            similarities = cosine_similarity(user_vector, self.course_features)[0]
            
            # Get top 3 course recommendations
            top_indices = np.argsort(similarities)[-3:][::-1]
            
            return [int(i + 1) for i in top_indices]  # Course IDs (1-indexed)
        except Exception as e:
            print(f"Error in course recommendation: {e}")
            return [1, 2, 3]  # Fallback