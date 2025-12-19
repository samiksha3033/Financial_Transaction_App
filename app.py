""" This is a web flask application for financial transaction recording system """
#import all the necessary libraries
from flask import Flask, render_template, url_for, request, redirect

#Initiate Flask Application
app = Flask(__name__)

# Sample data storage
transactions = [
    {"id": 1, "date": "2024-01-01", "amount": 1000},
    {"id": 2, "date": "2024-01-05", "amount": 2500}
]

#Read operation
@app.route("/")
def index():
    """ Displays all transactions """
    balance = sum(t["amount"] for t in transactions)
    return render_template("transactions.html",
                           transactions=transactions,
                           balance=balance,
                           is_search = False)

#Create Operation
@app.route("/add", methods = ["GET", "POST"])
def add_transactions():
    """ Function to Add a new transaction """
    if request.method == "POST":
        #step 1: Form se values lena
        date = request.form["date"]
        amount = float(request.form["amount"])

        #step 2: to generate new id
        if len(transactions)== 0:
            new_id = 1
        else :
            new_id = transactions[-1]["id"] + 1

        #step 3: new transaction dictionary banana
        new_transaction = {
            "id" : new_id,
            "date": date,
            "amount": amount
        }

        #step 4: new ko old append krna
        transactions.append(new_transaction)

        #step 5: home page pe vapis bhejna
        return redirect(url_for("index"))

    #GET request ke liye form dikhao
    return render_template("form.html")

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):

    # STEP 1: Agar user ne form submit kiya hai (POST request)
    if request.method == "POST":

        # STEP 2: Form ke andar jo values bhari hain woh Flask ko milti hain
        date = request.form["date"]
        amount = float(request.form["amount"])

        # STEP 3: Transactions list me jaake same ID wali entry dhundhna
        for transaction in transactions:
            if transaction["id"] == transaction_id:

                # STEP 4: Us transaction ko update kar dena
                transaction["date"] = date
                transaction["amount"] = amount

                break  # kaam ho gaya, loop band

        # STEP 5: Update ke baad user ko list page pe bhejna
        return redirect(url_for("index"))

    # STEP 6: Agar POST nahi hai, matlab GET request hai
    # → Sirf form dikhana hai
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    """
    Function to delete a transaction
    """

    # Step 1: Transactions list me jaakar matching ID dhundhna
    for transaction in transactions:
        if transaction["id"] == transaction_id:

            # Step 2: Us transaction ko list se remove kar dena
            transactions.remove(transaction)
            break

    # Step 3: Delete ke baad home page pe redirect
    return redirect(url_for("index"))

@app.route("/search", methods = ["GET", "POST"])
def search_transaction():
    if request.method == "POST":
        min_amount = float(request.form["min_amount"])
        max_amount = float(request.form["max_amount"])

        filtered_transactions = [
            t for t in transactions
            if min_amount <= t["amount"] <= max_amount
            ]

        return render_template("transactions.html",
                               transactions=filtered_transactions,
                               is_search=True )

    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
