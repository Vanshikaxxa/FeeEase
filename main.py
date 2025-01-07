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

# Function to authenticate staff login
def staff_login():
    username = username_entry.get()
    password = password_entry.get()
    
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Staff WHERE username = %s AND password = %s", (username, password))
    staff = cursor.fetchone()
    cursor.close()
    
    if staff:
        messagebox.showinfo("Success", "Login Successful!")
        login_window.destroy()  # Close the login window
        show_main_window()  # Show the main fee management window
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# Show the main fee management window
def show_main_window():
    global root
    root = tk.Tk()
    root.title("Fee Management System")
    root.geometry("600x500")
    root.config(bg="#f2f2f2")

    frame = tk.Frame(root, bg="#f2f2f2")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    # Add Student Section
    add_student_frame = tk.LabelFrame(frame, text="Add Student", font=("Arial", 14), bg="#f2f2f2", bd=2, relief="sunken")
    add_student_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    tk.Label(add_student_frame, text="Name:", bg="#f2f2f2").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    name_entry = tk.Entry(add_student_frame, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(add_student_frame, text="Class:", bg="#f2f2f2").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    class_entry = tk.Entry(add_student_frame, width=30)
    class_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(add_student_frame, text="Total Fee:", bg="#f2f2f2").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    total_fee_entry = tk.Entry(add_student_frame, width=30)
    total_fee_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(add_student_frame, text="Paid Amount:", bg="#f2f2f2").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    paid_amount_entry = tk.Entry(add_student_frame, width=30)
    paid_amount_entry.grid(row=3, column=1, padx=10, pady=5)

    add_button = tk.Button(add_student_frame, text="Add Student", command=add_student, bg="#4CAF50", fg="white", width=20)
    add_button.grid(row=4, column=0, columnspan=2, pady=10)

    # View Students Section
    view_button = tk.Button(frame, text="View Students", command=view_students, bg="#2196F3", fg="white", width=20)
    view_button.grid(row=1, column=0, pady=10)

    listbox = tk.Listbox(frame, width=70, height=10)
    listbox.grid(row=2, column=0, columnspan=2, pady=10)

    # Update Fee Section
    update_fee_frame = tk.LabelFrame(frame, text="Update Fee", font=("Arial", 14), bg="#f2f2f2", bd=2, relief="sunken")
    update_fee_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    tk.Label(update_fee_frame, text="Student ID (update):", bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=5)
    student_id_entry = tk.Entry(update_fee_frame, width=30)
    student_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(update_fee_frame, text="New Paid Amount:", bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=5)
    new_paid_amount_entry = tk.Entry(update_fee_frame, width=30)
    new_paid_amount_entry.grid(row=1, column=1, padx=10, pady=5)

    update_button = tk.Button(update_fee_frame, text="Update Fee", command=update_fee, bg="#FFC107", fg="black", width=20)
    update_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Delete Student Section
    delete_fee_frame = tk.LabelFrame(frame, text="Delete Student", font=("Arial", 14), bg="#f2f2f2", bd=2, relief="sunken")
    delete_fee_frame.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    tk.Label(delete_fee_frame, text="Student ID (delete):", bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=5)
    delete_student_id_entry = tk.Entry(delete_fee_frame, width=30)
    delete_student_id_entry.grid(row=0, column=1, padx=10, pady=5)

    delete_button = tk.Button(delete_fee_frame, text="Delete Student", command=delete_student, bg="#F44336", fg="white", width=20)
    delete_button.grid(row=1, column=0, columnspan=2, pady=10)

    root.mainloop()

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

# Main Login Window for Staff
def show_login_window():
    global login_window
    login_window = tk.Tk()
    login_window.title("Staff Login")
    login_window.geometry("400x300")
    login_window.config(bg="#f2f2f2")

    frame = tk.Frame(login_window, bg="#f2f2f2")
    frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

    tk.Label(frame, text="Username:", bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=10)
    global username_entry
    username_entry = tk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(frame, text="Password:", bg="#f2f2f2").grid(row=1, column=0, padx=10, pady=10)
    global password_entry
    password_entry = tk.Entry(frame, show="*", width=30)
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    login_button = tk.Button(frame, text="Login", command=staff_login, bg="#4CAF50", fg="white", width=20)
    login_button.grid(row=2, column=0, columnspan=2, pady=20)

    login_window.mainloop()

# Database connection
db = connect_db()

# Show login window
show_login_window()
