import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
from pathlib import Path

def create_recommendation_model():
    """Create a simple recommendation model for career guidance"""
    
    # Sample training data for career recommendation
    # This represents user preferences/skills -> career mapping
    training_data = {
        'programming_interest': [5, 4, 3, 5, 2, 4, 3, 5, 1, 2, 4, 5, 3, 2, 4],
        'math_skills': [4, 5, 3, 4, 2, 3, 4, 5, 2, 1, 3, 4, 3, 2, 4],
        'communication_skills': [3, 2, 5, 3, 5, 4, 4, 2, 5, 4, 3, 2, 4, 5, 3],
        'creativity': [2, 3, 4, 2, 5, 4, 3, 2, 4, 5, 3, 2, 4, 5, 4],
        'analytical_thinking': [5, 5, 3, 4, 2, 3, 4, 5, 2, 2, 4, 5, 3, 2, 4],
        'leadership': [3, 2, 4, 3, 4, 5, 4, 2, 4, 3, 3, 2, 4, 4, 3],
        'career_id': [1, 2, 3, 1, 5, 7, 4, 2, 3, 5, 1, 2, 4, 3, 1]  # Career IDs from our sample data
    }
    
    df = pd.DataFrame(training_data)
    
    # Features (user skills/interests)
    X = df[['programming_interest', 'math_skills', 'communication_skills', 
            'creativity', 'analytical_thinking', 'leadership']]
    
    # Target (career recommendations)
    y = df['career_id']
    
    # Create and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Create models directory if it doesn't exist
    models_dir = Path("app/ml/models")
    models_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the model
    model_path = models_dir / "career_recommender.pkl"
    joblib.dump(model, model_path)
    
    print(f"Model saved to {model_path}")
    
    # Create a simple course recommendation model (content-based)
    course_features = {
        'course_id': [1, 2, 3, 4, 5, 6, 7, 8],
        'programming_content': [0.9, 0.8, 0.7, 0.6, 0.1, 0.2, 0.5, 0.6],
        'math_content': [0.3, 0.9, 0.2, 0.8, 0.1, 0.3, 0.4, 0.2],
        'business_content': [0.1, 0.2, 0.3, 0.1, 0.9, 0.1, 0.2, 0.3],
        'design_content': [0.2, 0.1, 0.8, 0.1, 0.7, 0.2, 0.1, 0.9],
        'security_content': [0.1, 0.1, 0.1, 0.2, 0.1, 0.9, 0.3, 0.1]
    }
    
    course_df = pd.DataFrame(course_features)
    course_features_matrix = course_df[['programming_content', 'math_content', 
                                       'business_content', 'design_content', 'security_content']]
    
    # Save course features for similarity calculations
    course_model_path = models_dir / "course_features.pkl"
    joblib.dump(course_features_matrix, course_model_path)
    
    print(f"Course features saved to {course_model_path}")
    
    return model

if __name__ == "__main__":
    create_recommendation_model()
