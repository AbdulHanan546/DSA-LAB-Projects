class CashFlowMinimizer:
    def __init__(self, group_size):
        self.group_size = group_size
        self.balance_sheet = [0] * group_size

    def add_transaction(self, lender, borrower, amount):
       
        self.balance_sheet[lender] -= amount
        self.balance_sheet[borrower] += amount

    def get_minimized_cash_flow(self):

        def minimize_cash_flow_util(balance):
            
            max_credit = max(balance)
            max_debit = min(balance)

            if max_credit == 0 and max_debit == 0:
                return []  

            creditor = balance.index(max_credit)
            debtor = balance.index(max_debit)

            
            settlement_amount = min(-max_debit, max_credit)

            
            balance[creditor] -= settlement_amount
            balance[debtor] += settlement_amount

            
            transaction = (debtor, creditor, settlement_amount)

            return [transaction] + minimize_cash_flow_util(balance)

        return minimize_cash_flow_util(self.balance_sheet[:])

    def display_transactions(self, transactions):
       
        if not transactions:
            print("No transactions needed. All debts are settled.")
            return

        print("Minimized Transactions:")
        for debtor, creditor, amount in transactions:
            print(f"Person {debtor} pays Person {creditor} an amount of {amount:.2f}")


# Example usage
if __name__ == "__main__":
    group_size = int(input("Enter the number of people in the group: "))
    minimizer = CashFlowMinimizer(group_size)

    num_transactions = int(input("Enter the number of transactions: "))
    print("Enter transactions in the format: lender borrower amount")

    for _ in range(num_transactions):
        lender, borrower, amount = map(str, input().split())
        minimizer.add_transaction(int(lender), int(borrower), float(amount))

    minimized_transactions = minimizer.get_minimized_cash_flow()
    minimizer.display_transactions(minimized_transactions)
