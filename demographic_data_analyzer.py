import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset?
    # This should be a Pandas series with race names as the index labels.
    race_count = (df["race"].value_counts()).sort_values(ascending=False)

    # What is the average age of men?
    age_men = (df.loc[:, ["sex", "age"]]).groupby("sex").agg({"age": "mean"})
    average_age_men = ((age_men.loc["Male"]).round(decimals=1))["age"]

    # What is the percentage of people who have a Bachelor's degree?
    education = (df["education"].value_counts())
    percentage_bachelors = (100 * education.loc["Bachelors"] / education.sum()).round(decimals=1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?

    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df[(df["education"] == "Bachelors") | (df["education"] == "Masters") | (df["education"] == "Doctorate")]
    lower_education = df[(df["education"] != "Bachelors") & (df["education"] != "Masters") & (df["education"] != "Doctorate")]

    higher_ed_M50 = higher_education[higher_education["salary"] == ">50K"]
    lower_ed_M50 = lower_education[lower_education["salary"] == ">50K"]

    # percentage with salary >50K
    higher_education_rich = (100 * higher_ed_M50["salary"].count() / higher_education["salary"].count()).round(decimals=1)
    lower_education_rich = (100 * lower_ed_M50["salary"].count() / lower_education["salary"].count()).round(decimals=1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df["hours-per-week"].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min = df[(df["hours-per-week"] == min_work_hours)]
    num_min_workers = num_min["hours-per-week"].count()
    rich_num_min_workers = num_min[(num_min["salary"] == ">50K")]
    rich_percentage = (100 * rich_num_min_workers["hours-per-week"].count() / num_min_workers).round(decimals=1)

    # What country has the highest percentage of people that earn >50K?
    country_salary = df.loc[:, ["native-country", "salary"]]
    highest_earning = (country_salary[country_salary["salary"] == ">50K"]).groupby("native-country").count()

    earning = country_salary.groupby("native-country").count()
    earning[">50K"] = highest_earning["salary"]

    def ratio_salary(row):
        return row[">50K"] / row["salary"]

    earning["ratio"] = earning.apply(ratio_salary, axis=1)

    highest_earning_country = (earning[earning['ratio'] == (earning["ratio"].max())]).index[0]
    highest_earning_country_percentage = (100*earning["ratio"].max()).round(decimals=1)

    # Identify the most popular occupation for those who earn >50K in India.
    indiaM50Kocc = (df[(df["salary"] == ">50K") & (df["native-country"] == "India")])
    indiaM50Kocc = indiaM50Kocc.groupby("occupation").count()

    top_IN_occupation = (indiaM50Kocc[indiaM50Kocc['salary'] == (indiaM50Kocc["salary"].max())]).index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
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
