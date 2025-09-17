import joblib
import numpy as np
from pathlib import Path

# Create models directory
models_dir = Path("app/ml/models")
models_dir.mkdir(parents=True, exist_ok=True)

# Create simple arrays instead of complex objects
career_probabilities = np.array([0.1, 0.15, 0.12, 0.08, 0.2, 0.1, 0.15, 0.1])
career_classes = np.array([1, 2, 3, 4, 5, 6, 7, 8])

# Save as simple data
joblib.dump({'probabilities': career_probabilities, 'classes': career_classes}, 
           models_dir / "career_recommender.pkl")

# Course features matrix
course_features = np.array([
    [0.9, 0.3, 0.1, 0.2, 0.1],
    [0.8, 0.9, 0.2, 0.1, 0.1],
    [0.7, 0.2, 0.3, 0.8, 0.1],
    [0.6, 0.8, 0.1, 0.1, 0.2],
    [0.1, 0.1, 0.9, 0.7, 0.1],
    [0.2, 0.3, 0.1, 0.2, 0.9],
    [0.5, 0.4, 0.2, 0.1, 0.3],
    [0.6, 0.2, 0.3, 0.9, 0.1]
])

joblib.dump(course_features, models_dir / "course_features.pkl")

print("✅ Simple ML models created successfully!")
