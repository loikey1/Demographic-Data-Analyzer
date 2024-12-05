import pandas as pd

def calculate_demographic_data(print_data=True):
    # Read the dataset
    column_names = [
        "age", "workclass", "fnlwgt", "education", "education-num", 
        "marital-status", "occupation", "relationship", "race", 
        "sex", "capital-gain", "capital-loss", "hours-per-week", 
        "native-country", "salary"
    ]
    df = pd.read_csv("adult.data.csv", header=None, names=column_names)
   
    # Convert columns to numeric and coerce errors to NaN for columns that should be numeric
    df['age'] = pd.to_numeric(df['age'], errors='coerce')
    df['hours-per-week'] = pd.to_numeric(df['hours-per-week'], errors='coerce')
    df['fnlwgt'] = pd.to_numeric(df['fnlwgt'], errors='coerce')

    # Drop rows with NaN values in important columns (age, hours-per-week, fnlwgt) to avoid incorrect calculations
    df = df.dropna(subset=['age', 'hours-per-week', 'fnlwgt'])
    
    # 1. How many people of each race are represented in this dataset?
    race_count = df['race'].value_counts()

    # 2. What is the average age of men?
    average_age_men = round(df[df['sex'] == 'Male']['age'].mean(), 1)

    # 3. What is the percentage of people who have a Bachelor's degree?
    total_people = len(df)
    percentage_bachelors = round((df['education'] == 'Bachelors').sum() / total_people * 100, 1)

    # 4. What percentage of people with advanced education (Bachelors, Masters, Doctorate) make more than 50K?
    advanced_education = df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])
    higher_education_rich = round(
        (df[advanced_education & (df['salary'] == '>50K')].shape[0] / df[advanced_education].shape[0]) * 100, 1)

    # 5. What percentage of people without advanced education make more than 50K?
    non_advanced_education = ~advanced_education
    lower_education_rich = round(
        (df[non_advanced_education & (df['salary'] == '>50K')].shape[0] / df[non_advanced_education].shape[0]) * 100, 1)

    # 6. What is the minimum number of hours a person works per week?
    min_work_hours = df['hours-per-week'].min()

    # 7. What percentage of the people who work the minimum number of hours per week have a salary of more than 50K?
    min_workers = df['hours-per-week'] == min_work_hours
    rich_percentage = round(
        (df[min_workers & (df['salary'] == '>50K')].shape[0] / df[min_workers].shape[0]) * 100, 1)

    # 8. What country has the highest percentage of people that earn >50K and what is that percentage?
    country_rich_percentage = (
        df[df['salary'] == '>50K']['native-country'].value_counts() / df['native-country'].value_counts() * 100).dropna()
    highest_earning_country = country_rich_percentage.idxmax()
    highest_earning_country_percentage = round(country_rich_percentage.max(), 1)

    # 9. Identify the most popular occupation for those who earn >50K in India.
    india_high_earners = df[
        (df['native-country'] == 'India') & (df['salary'] == '>50K')
    ]
    top_IN_occupation = india_high_earners['occupation'].value_counts().idxmax()

    results = {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage': highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
    
    if print_data:
        for key, value in results.items():
            print(f"{key}: {value}")
    
    return results