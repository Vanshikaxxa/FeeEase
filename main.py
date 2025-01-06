import tkinter as tk
from tkinter import messagebox
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user="root",
        password="Tannu@123",
        database="FeeManagementDB"
    )

# Add student to the database
def add_student():
    name = name_entry.get()
    student_class = class_entry.get()
    try:
        total_fee = float(total_fee_entry.get())
        paid_amount = float(paid_amount_entry.get())
        
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO Students (name, class, total_fee, paid_amount) VALUES (%s, %s, %s, %s)",
            (name, student_class, total_fee, paid_amount)
        )
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", "Student record added successfully.")
        clear_entries()  # Clear input fields after successful add
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers for fees.")

# View all student records
def view_students():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Students")
    records = cursor.fetchall()
    cursor.close()

    listbox.delete(0, tk.END)  # Clear existing records in listbox
    for record in records:
        listbox.insert(tk.END, f"{record[0]} | {record[1]} | {record[2]} | {record[3]} | {record[4]} | {record[5]}")

# Update fee details for a student
def update_fee():
    student_id = student_id_entry.get()
    try:
        paid_amount = float(new_paid_amount_entry.get())
        cursor = db.cursor()
        cursor.execute("UPDATE Students SET paid_amount = %s WHERE id = %s", (paid_amount, student_id))
        db.commit()
        cursor.close()
        messagebox.showinfo("Success", "Fee details updated successfully.")
        clear_entries()
    except ValueError:
        messagebox.showerror("Error", "Please enter valid fee values.")

# Delete a student record
def delete_student():
    student_id = delete_student_id_entry.get()
    cursor = db.cursor()
    cursor.execute("DELETE FROM Students WHERE id = %s", (student_id,))
    db.commit()
    cursor.close()
    messagebox.showinfo("Success", "Student record deleted successfully.")
    clear_entries()

# Clear all input fields
def clear_entries():
    name_entry.delete(0, tk.END)
    class_entry.delete(0, tk.END)
    total_fee_entry.delete(0, tk.END)
    paid_amount_entry.delete(0, tk.END)
    student_id_entry.delete(0, tk.END)
    new_paid_amount_entry.delete(0, tk.END)
    delete_student_id_entry.delete(0, tk.END)

# Main GUI window setup
root = tk.Tk()
root.title("Fee Management System")

# Database connection
db = connect_db()

# Add Student Section
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Class:").grid(row=1, column=0)
class_entry = tk.Entry(root)
class_entry.grid(row=1, column=1)

tk.Label(root, text="Total Fee:").grid(row=2, column=0)
total_fee_entry = tk.Entry(root)
total_fee_entry.grid(row=2, column=1)

tk.Label(root, text="Paid Amount:").grid(row=3, column=0)
paid_amount_entry = tk.Entry(root)
paid_amount_entry.grid(row=3, column=1)

add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.grid(row=4, column=0, columnspan=2)

# View Students Section
view_button = tk.Button(root, text="View Students", command=view_students)
view_button.grid(row=5, column=0, columnspan=2)

listbox = tk.Listbox(root, width=80, height=10)
listbox.grid(row=6, column=0, columnspan=2)

# Update Fee Section
tk.Label(root, text="Student ID (update):").grid(row=7, column=0)
student_id_entry = tk.Entry(root)
student_id_entry.grid(row=7, column=1)

tk.Label(root, text="New Paid Amount:").grid(row=8, column=0)
new_paid_amount_entry = tk.Entry(root)
new_paid_amount_entry.grid(row=8, column=1)

update_button = tk.Button(root, text="Update Fee", command=update_fee)
update_button.grid(row=9, column=0, columnspan=2)

# Delete Student Section
tk.Label(root, text="Student ID (delete):").grid(row=10, column=0)
delete_student_id_entry = tk.Entry(root)
delete_student_id_entry.grid(row=10, column=1)

delete_button = tk.Button(root, text="Delete Student", command=delete_student)
delete_button.grid(row=11, column=0, columnspan=2)

# Run the GUI loop
root.mainloop()
