❤️ Heart Disease Prediction using Machine Learning
📌 Overview

This project builds a complete machine learning pipeline to predict the presence of heart disease using structured clinical data. The workflow includes exploratory data analysis, feature engineering, model comparison, cross-validation, hyperparameter tuning, and deployment.

📊 Dataset

918 patient records

11 clinical features

Binary target (HeartDisease: 0 or 1)

🔍 Key Insights

ST_Slope, ExerciseAngina, ChestPainType, Oldpeak, and MaxHR are strong predictors.

Invalid cholesterol values (0) were handled using feature engineering.

🧠 Models Evaluated

Logistic Regression

Decision Tree

Random Forest

Gradient Boosting

📈 Best Model Performance

Tuned Random Forest

Cross-validated ROC-AUC ≈ 0.93

🚀 Deployment

Backend: FastAPI (Render)

Frontend: Streamlit (Streamlit Cloud)

📂 Project Structure
backend/
frontend/
notebooks/
⚠️ Disclaimer

This project is for educational purposes only and is not a medical diagnosis tool.