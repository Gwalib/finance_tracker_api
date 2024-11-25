import pandas as pd

class FinanceService:
    def __init__(self, file_path):
        """
        Initialize the FinanceService with the path to the CSV file.
        Load the data into a Pandas DataFrame.
        """
        self.file_path = file_path
        self.df = pd.read_csv(file_path)

    def add_transaction(self, transaction_data):
        """
        Add a new transaction to the dataset.
        """
        new_transaction = pd.DataFrame([transaction_data])
        self.df = pd.concat([self.df, new_transaction], ignore_index=True)
        self.df.to_csv(self.file_path, index=False)

    def calculate_summary(self):
        """
        Calculate and return the total income, total expenses, and net savings.
        """
        total_income = self.df[self.df['Type'] == 'Income']['Amount'].sum()
        total_expenses = self.df[self.df['Type'] == 'Expense']['Amount'].sum()
        net_savings = total_income - total_expenses

        return {
            "Total Income": total_income,
            "Total Expense": total_expenses,
            "Net Savings": net_savings
        }

    def get_report(self, month=None, category=None):
        """
        Generate a filtered report based on the month and/or category.
        """
        filtered_df = self.df.copy()

        if month:
            filtered_df = filtered_df[filtered_df['Date'].str.startswith(month)]

        if category:
            filtered_df = filtered_df[filtered_df['Category'] == category]

        return filtered_df.to_dict(orient="records")
