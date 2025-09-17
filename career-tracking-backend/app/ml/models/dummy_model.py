# Simple fallback for ML models until we create the actual ones
import joblib
import numpy as np
from pathlib import Path

def create_dummy_models():
    """Create dummy models for MVP functionality"""
    models_dir = Path(__file__).parent
    models_dir.mkdir(exist_ok=True)
    
    # Create a simple dummy career recommender
    class DummyCareerModel:
        def predict_proba(self, X):
            # Return dummy probabilities for 8 careers
            return np.array([[0.1, 0.15, 0.12, 0.08, 0.2, 0.1, 0.15, 0.1]])
        
        @property
        def classes_(self):
            return np.array([1, 2, 3, 4, 5, 6, 7, 8])
    
    # Save dummy career model
    joblib.dump(DummyCareerModel(), models_dir / "career_recommender.pkl")
    
    # Create dummy course features (8 courses x 5 features)
    course_features = np.array([
        [0.9, 0.3, 0.1, 0.2, 0.1],  # Course 1: Programming heavy
        [0.8, 0.9, 0.2, 0.1, 0.1],  # Course 2: Math heavy
        [0.7, 0.2, 0.3, 0.8, 0.1],  # Course 3: Design heavy
        [0.6, 0.8, 0.1, 0.1, 0.2],  # Course 4: ML/Math
        [0.1, 0.1, 0.9, 0.7, 0.1],  # Course 5: Business/Marketing
        [0.2, 0.3, 0.1, 0.2, 0.9],  # Course 6: Security
        [0.5, 0.4, 0.2, 0.1, 0.3],  # Course 7: Cloud
        [0.6, 0.2, 0.3, 0.9, 0.1]   # Course 8: Mobile/Design
    ])
    
    joblib.dump(course_features, models_dir / "course_features.pkl")
    
    print("✅ Dummy ML models created successfully!")

if __name__ == "__main__":
    create_dummy_models()
