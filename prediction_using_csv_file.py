import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load career data from a CSV file
career_data = pd.read_csv('career_data.csv')

# Get user input for student's skills and education level
print("Please enter your information:")
technical_skills = int(input("Technical Skills (1-5): "))
soft_skills = int(input("Soft Skills (1-5): "))
education_level = input("Education Level (Bachelor, Master, PhD, Associate): ")

# Ensure education level labels match (case-sensitive)
education_level = education_level.capitalize()  # Capitalize the first letter

# Check if the education level is in the career data
if education_level not in career_data['Education Level'].unique():
    print("Invalid education level. Please enter a valid education level.")
else:
    # Create a student data frame with user input
    student_data = pd.DataFrame({
        'Technical Skills': [technical_skills],
        'Soft Skills': [soft_skills],
        'Education Level': [education_level]
    })

    # Encode categorical features using one-hot encoding for both career and student data
    career_data_encoded = pd.get_dummies(career_data, columns=['Education Level'], drop_first=True)
    student_data_encoded = pd.get_dummies(student_data, columns=['Education Level'], drop_first=True)

    # Ensure the encoded student data has the same columns as career data
    missing_columns = set(career_data_encoded.columns) - set(student_data_encoded.columns)
    for col in missing_columns:
        student_data_encoded[col] = 0  # Add missing columns with default value 0

    # Separate features and labels
    X = career_data_encoded.drop('Career', axis=1)
    y = career_data_encoded['Career']

    # Train a machine learning model (Random Forest in this example)
    clf = RandomForestClassifier()
    clf.fit(X, y)

    # Make predictions on student data
    student_data_encoded = student_data_encoded[X.columns]  # Ensure column order is the same
    predictions = clf.predict(student_data_encoded)

    # Print recommended career(s)
    print("Recommended Career(s):", predictions)
