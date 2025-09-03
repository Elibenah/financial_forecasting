import pandas as pd
import numpy as np

# Load the expense percentages data. The years are already columns, so we don't need to transpose.
df_expenses_percentages = pd.read_csv("Expense composition percentage.csv", header=2, index_col=0, encoding='utf-8')
df_expenses_percentages.index = df_expenses_percentages.index.str.strip()
df_expenses_percentages.columns = df_expenses_percentages.columns.str.strip()

# Load the income and expenses data. The years are in the first column, so it's already in the right format.
df_income_expenses = pd.read_csv("Income and expenses in shekels.csv", header=2, index_col=0, encoding='utf-8')
df_income_expenses.index = df_income_expenses.index.str.strip()
df_income_expenses.columns = df_income_expenses.columns.str.strip()

# Extract the relevant data for the year 2022
try:
    expense_proportions_2022 = df_expenses_percentages['2022'].to_dict()

    # Accessing the exact columns by their full, cleaned names
    avg_net_income_2022_raw = df_income_expenses.loc['2022', 'הכנסה כספית נטו למשק בית']
    avg_expense_2022_raw = df_income_expenses.loc['2022', 'הוצאה לתצרוכת*']

    # Clean the raw string data and convert to float
    avg_net_income_2022 = float(str(avg_net_income_2022_raw).replace(',', '').strip())
    avg_expense_2022 = float(str(avg_expense_2022_raw).replace(',', '').strip())

    print("הנתונים עבור 2022 נטענו בהצלחה!")

except KeyError as e:
    print(f"שגיאה: המפתח {e} לא נמצא. אנא ודא/י ששמות הקבצים והשורות תואמים בדיוק.")
    # Exit the program if the keys are not found
    exit()

# Define the user profiles based on the statistical data from the files
profiles = {
    'משפחה צעירה (עד 3 ילדים)': {
        'income_multiplier': 1.1, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 1.05,
        'deviations': {'דיור': 1.2, 'חינוך, תרבות ובידור': 1.3, 'מזון': 1.25}
    },
    'משפחה מרובת ילדים (4+ ילדים)': {
        'income_multiplier': 1.5, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 1.4,
        'deviations': {'מזון': 1.5, 'חינוך, תרבות ובידור': 1.8, 'הלבשה והנעלה': 1.5, 'דיור': 1.3}
    },
    'סטודנטים': {
        'income_multiplier': 0.4, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 0.8,
        'deviations': {'דיור': 1.3, 'תחבורה ותקשורת': 0.8, 'בילויים': 1.5}
    },
    'רווקים': {
        'income_multiplier': 0.8, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 0.9,
        'deviations': {'דיור': 0.9, 'בילויים': 1.2}
    },
    'זוגות צעירים ללא ילדים': {
        'income_multiplier': 1.2, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 1.0,
        'deviations': {'חיסכון': 1.5, 'בילויים': 1.1}
    },
    'זוגות מבוגרים': {
        'income_multiplier': 1.5, 'expense_dist': expense_proportions_2022, 'expense_multiplier': 1.2,
        'deviations': {'בריאות': 1.3, 'תרבות ופנאי': 1.5}
    }
}


def generate_financial_data(num_records):
    data = []

    for i in range(num_records):
        profile_type = np.random.choice(list(profiles.keys()))
        profile_data = profiles[profile_type]

        income = np.random.normal(avg_net_income_2022 * profile_data['income_multiplier'], 1000)
        total_expense = np.random.normal(avg_expense_2022 * profile_data['expense_multiplier'], 800)

        expenses = {}
        for category, proportion in profile_data['expense_dist'].items():
            multiplier = profile_data['deviations'].get(category, 1.0)
            expense = total_expense * proportion / 100 * multiplier * np.random.uniform(0.9, 1.1)
            expenses[category] = expense

        data.append({
            'user_id': i,
            'profile_type': profile_type,
            'income': income,
            'total_expense': total_expense,
            **expenses
        })

    df = pd.DataFrame(data)
    return df


# Generate and save the data
num_records_to_generate = 30000
df = generate_financial_data(num_records_to_generate)
df.to_csv('financial_data_il_detailed.csv', index=False, encoding='utf-8-sig')

print("\nמערך הנתונים הפיקטיבי נוצר בהצלחה בקובץ financial_data_il_detailed.csv")