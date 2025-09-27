from fastapi import APIRouter, HTTPException
from schemas import MLPredictionRequest, MLPredictionResponse
from ml_service import predictor

router = APIRouter(prefix="/api/ml", tags=["machine learning"])

@router.post("/predict", response_model=MLPredictionResponse)
async def predict_burnout(request: MLPredictionRequest):
    """Predict burnout risk based on student features"""
    try:
        result = predictor.predict_burnout(
            attendance=request.attendance,
            gpa=request.gpa,
            sentiment_score=request.sentiment_score
        )
        
        return MLPredictionResponse(
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            color=result["color"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@router.post("/train")
async def train_model():
    """Train/retrain the burnout prediction model"""
    try:
        results = predictor.train_model()
        return {
            "message": "Model training completed successfully",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")