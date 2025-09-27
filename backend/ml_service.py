import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
from typing import Dict, Tuple

class BurnoutPredictor:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_path = "burnout_model.pkl"
        self.scaler_path = "scaler.pkl"
        
    def generate_synthetic_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for burnout prediction"""
        np.random.seed(42)
        
        # Generate features: attendance, gpa, sentiment_score
        attendance = np.random.normal(80, 15, n_samples)  # Mean 80%, std 15%
        attendance = np.clip(attendance, 0, 100)
        
        gpa = np.random.normal(3.0, 0.8, n_samples)  # Mean 3.0, std 0.8
        gpa = np.clip(gpa, 0.0, 4.0)
        
        sentiment_score = np.random.normal(0.2, 0.6, n_samples)  # Slightly positive bias
        sentiment_score = np.clip(sentiment_score, -1.0, 1.0)
        
        # Create target based on logical rules
        # Higher burnout risk when:
        # - Low attendance (< 70%)
        # - Low GPA (< 2.5)
        # - Negative sentiment (< -0.2)
        
        burnout_risk = np.zeros(n_samples)
        for i in range(n_samples):
            risk_score = 0
            
            # Attendance factor
            if attendance[i] < 70:
                risk_score += 0.4
            elif attendance[i] < 80:
                risk_score += 0.2
                
            # GPA factor  
            if gpa[i] < 2.5:
                risk_score += 0.4
            elif gpa[i] < 3.0:
                risk_score += 0.2
                
            # Sentiment factor
            if sentiment_score[i] < -0.2:
                risk_score += 0.3
            elif sentiment_score[i] < 0.1:
                risk_score += 0.1
                
            # Add some noise
            risk_score += np.random.normal(0, 0.1)
            
            # Convert to binary (high risk if score > 0.5)
            burnout_risk[i] = 1 if risk_score > 0.5 else 0
        
        features = np.column_stack([attendance, gpa, sentiment_score])
        return features, burnout_risk
    
    def train_model(self) -> Dict[str, float]:
        """Train the burnout prediction model"""
        print("Generating synthetic training data...")
        X, y = self.generate_synthetic_data(1000)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale the features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train the model
        print("Training Random Forest model...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate the model
        train_accuracy = accuracy_score(y_train, self.model.predict(X_train_scaled))
        test_accuracy = accuracy_score(y_test, self.model.predict(X_test_scaled))
        
        # Save the model and scaler
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
        
        print(f"Model training completed!")
        print(f"Train accuracy: {train_accuracy:.3f}")
        print(f"Test accuracy: {test_accuracy:.3f}")
        
        return {
            "train_accuracy": train_accuracy,
            "test_accuracy": test_accuracy,
            "feature_importance": {
                "attendance": float(self.model.feature_importances_[0]),
                "gpa": float(self.model.feature_importances_[1]),
                "sentiment_score": float(self.model.feature_importances_[2])
            }
        }
    
    def load_model(self) -> bool:
        """Load the trained model and scaler"""
        try:
            if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                print("Model and scaler loaded successfully!")
                return True
            else:
                print("Model files not found. Training new model...")
                self.train_model()
                return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict_burnout(self, attendance: float, gpa: float, sentiment_score: float) -> Dict[str, any]:
        """Predict burnout risk for given features"""
        if self.model is None or self.scaler is None:
            if not self.load_model():
                raise Exception("Failed to load model")
        
        # Prepare the input
        features = np.array([[attendance, gpa, sentiment_score]])
        features_scaled = self.scaler.transform(features)
        
        # Get probability predictions
        probabilities = self.model.predict_proba(features_scaled)[0]
        risk_probability = probabilities[1]  # Probability of high risk (class 1)
        
        # Determine risk level and color
        if risk_probability < 0.3:
            risk_level = "Low"
            color = "green"
        elif risk_probability < 0.7:
            risk_level = "Medium" 
            color = "yellow"
        else:
            risk_level = "High"
            color = "red"
        
        # Convert to BRI score (0-100 scale)
        bri_score = int((1 - risk_probability) * 100)
        
        return {
            "risk_score": float(risk_probability),
            "risk_level": risk_level,
            "color": color,
            "bri_score": bri_score,
            "confidence": float(max(probabilities))
        }

# Global predictor instance
predictor = BurnoutPredictor()