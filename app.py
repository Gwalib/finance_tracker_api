from flask import Flask, request, jsonify
from services.finance_services import FinanceService
import os
import pandas as pd

app = Flask(__name__)

# Initialize FinanceService with the CSV file path
finance_service = FinanceService('C:/Users/dell/OneDrive/Documents/finance_tracker_api/data/transactions.csv')

@app.route('/finance/transactions', methods=['GET'])
def get_transactions():
    file_path = os.path.join('data', 'transactions.csv')
    if not os.path.exists(file_path):
        return jsonify({"error": "transactions.csv not found"}), 404

    try:
        transactions_df = pd.read_csv(file_path)
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 500

    # Get query parameter (e.g., category)
    category = request.args.get('Category')
   # print(f"Received category: {category}") 
    if category:
        print(f"Filtering transactions for category: {category}")
        transactions_df = transactions_df[transactions_df['Category'] == category]
    
    transactions = transactions_df.to_dict(orient='records')
    return jsonify(transactions)


@app.route('/finance/addtransaction', methods=['POST'])
def add_transaction():
    transaction_data = request.json
    finance_service.add_transaction(transaction_data)
    return jsonify({"message": "Transaction added successfully!"})

@app.route('/finance/summary', methods=['GET'])
def get_summary():
    summary = finance_service.calculate_summary()
    return jsonify(summary)

@app.route('/finance/report', methods=['GET'])
def get_report():
    month = request.args.get('month')
    category = request.args.get('category')
    report = finance_service.get_report(month, category)
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)
