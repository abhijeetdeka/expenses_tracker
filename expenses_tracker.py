import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import datetime, date
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ----------------- MySQL Database Connection -----------------
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  # Change to your MySQL username
        password="manjeetdeka@123",  # Change to your MySQL password
        database="expenses_db"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    messagebox.showerror("Database Error", f"Error connecting to MySQL: {err}")
    exit()

# ----------------- Create Tables -----------------
cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INT AUTO_INCREMENT PRIMARY KEY,
        date DATE,
        category VARCHAR(100),
        description VARCHAR(255),
        amount DECIMAL(10,2)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin_password (
        id INT AUTO_INCREMENT PRIMARY KEY,
        password VARCHAR(255) NOT NULL
    )
""")

# ----------------- Insert Default Password -----------------
cursor.execute("SELECT COUNT(*) FROM admin_password")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO admin_password (password) VALUES ('admin123')")
    conn.commit()

# ----------------- Verify Password -----------------
def verify_password():
    cursor.execute("SELECT password FROM admin_password LIMIT 1")
    saved_password = cursor.fetchone()[0]
    entered_password = simpledialog.askstring("Password Required", "Enter Admin Password:", show='*')

    if entered_password == saved_password:
        return True
    else:
        messagebox.showerror("Access Denied", "Incorrect Password!")
        return False

# ----------------- Add Expense -----------------
def add_expense():
    if not verify_password():
        return

    date_val = date_entry.get()
    category = category_var.get()
    description = description_entry.get()
    amount = amount_entry.get()

    if not (date_val and category and description and amount):
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        cursor.execute("""
            INSERT INTO expenses (date, category, description, amount)
            VALUES (%s, %s, %s, %s)
        """, (date_val, category, description, amount))
        conn.commit()
        messagebox.showinfo("Success", "Expense Added Successfully!")
        fetch_expenses()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# ----------------- Fetch Expenses -----------------
def fetch_expenses():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM expenses ORDER BY date DESC")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", END, values=row)

# ----------------- Delete Expense -----------------
def delete_expense():
    if not verify_password():
        return

    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Please select an expense to delete!")
        return

    expense_id = tree.item(selected_item)['values'][0]
    cursor.execute("DELETE FROM expenses WHERE id=%s", (expense_id,))
    conn.commit()
    messagebox.showinfo("Deleted", "Expense Deleted Successfully!")
    fetch_expenses()

# ----------------- Show Monthly Summary -----------------
def show_monthly_summary():
    try:
        today = date.today()
        current_month = today.month
        current_year = today.year

        # Get total expenses for the current month
        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM expenses
            WHERE MONTH(date) = %s AND YEAR(date) = %s
        """, (current_month, current_year))
        current_month_total = cursor.fetchone()[0]

        # Get total expenses for the previous month
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_year = current_year if current_month > 1 else current_year - 1
        cursor.execute("""
            SELECT IFNULL(SUM(amount), 0) FROM expenses
            WHERE MONTH(date) = %s AND YEAR(date) = %s
        """, (previous_month, previous_year))
        previous_month_total = cursor.fetchone()[0]

        # Show totals in a messagebox
        messagebox.showinfo("Monthly Expense Summary",
                            f"📅 {today.strftime('%B %Y')} Total: ₹{current_month_total}\n"
                            f"📅 {date(previous_year, previous_month, 1).strftime('%B %Y')} Total: ₹{previous_month_total}")

        # Show pie chart for current month
        cursor.execute("""
            SELECT category, SUM(amount) FROM expenses
            WHERE MONTH(date) = %s AND YEAR(date) = %s
            GROUP BY category
        """, (current_month, current_year))
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("No Data", "No expenses found for this month!")
            return

        categories = [row[0] for row in data]
        amounts = [row[1] for row in data]

        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title(f"Category-wise Expenses ({today.strftime('%B %Y')})")
        plt.show()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ----------------- GUI Setup -----------------
root = Tk()
root.title("Expense Tracker - MySQL")
root.geometry("1000x650")
root.resizable(False, False)

# ----------------- Date -----------------
Label(root, text="Date:").grid(row=0, column=0, padx=10, pady=10)
date_entry = DateEntry(root, width=15, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
date_entry.grid(row=0, column=1)

# ----------------- Category -----------------
Label(root, text="Category:").grid(row=0, column=2, padx=10)
category_var = StringVar()
category_combobox = ttk.Combobox(root, textvariable=category_var,
                                 values=("Food", "Travel", "Shopping", "Bills", "Other"))
category_combobox.grid(row=0, column=3)

# ----------------- Description -----------------
Label(root, text="Description:").grid(row=1, column=0, padx=10)
description_entry = Entry(root, width=30)
description_entry.grid(row=1, column=1)

# ----------------- Amount -----------------
Label(root, text="Amount:").grid(row=1, column=2, padx=10)
amount_entry = Entry(root, width=15)
amount_entry.grid(row=1, column=3)

# ----------------- Buttons -----------------
Button(root, text="Add Expense", command=add_expense, bg="green", fg="white", width=15).grid(row=2, column=1, pady=10)
Button(root, text="Delete Expense", command=delete_expense, bg="red", fg="white", width=15).grid(row=2, column=2)
Button(root, text="Show Summary", command=show_monthly_summary, bg="blue", fg="white", width=15).grid(row=2, column=3)

# ----------------- Expense Table -----------------
columns = ("ID", "Date", "Category", "Description", "Amount")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
tree.grid(row=3, column=0, columnspan=5, padx=10, pady=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150 if col != "Description" else 250)

# ----------------- Scrollbar -----------------
scrollbar = ttk.Scrollbar(root, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=3, column=5, sticky='ns')

# ----------------- Load Initial Data -----------------
fetch_expenses()

# ----------------- Run Application -----------------
root.mainloop()


