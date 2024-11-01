import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os

# Updated function to generate vaccination and medicine recommendations based on age
def generate_recommendation(age, city):
    if age < 1:
        vaccines = "Hepatitis B, Rotavirus, DTaP, Hib, PCV13, IPV"
        medicines = "Vitamin D supplements, Iron supplements"
    elif age >= 1 and age <= 4:
        vaccines = "MMR, Varicella, Hepatitis A, Influenza, DTaP"
        medicines = "Children's multivitamin, Fever reducers (e.g., Ibuprofen)"
    elif age >= 5 and age <= 12:
        vaccines = "MMR, Varicella, DTaP, Influenza, HPV (for older children)"
        medicines = "Fever reducers, Allergy medication (if needed)"
    else:
        vaccines = "Tdap, Influenza, HPV"
        medicines = "General OTC medicines as needed (fever, cold, etc.)"
    
    return f"Vaccines: {vaccines}\nMedicines: {medicines}"

# Function to save data to CSV
def save_to_csv(name, age, city, recommendation):
    data = {'Name': [name], 'Age': [age], 'City': [city], 'Recommendation': [recommendation]}
    df = pd.DataFrame(data)
    
    if os.path.exists('data.csv'):
        df.to_csv('data.csv', mode='a', header=False, index=False)
    else:
        df.to_csv('data.csv', index=False)
    messagebox.showinfo("Saved", "Your vaccination and medicine recommendation has been saved.")

# Submit button action
def submit():
    name = name_entry.get()
    city = city_entry.get()
    
    try:
        age = int(age_entry.get())
        if age < 0:
            messagebox.showwarning("Input Error", "Please enter a valid age!")
            return
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid age as a number!")
        return
    
    if not name or not city:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return
    
    recommendation = generate_recommendation(age, city)
    
    result_label.config(text=f"Recommendation for {name}:\n{recommendation}")
    save_to_csv(name, age, city, recommendation)

# Function to display history from CSV
def show_history():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        history_window = tk.Toplevel(root)
        history_window.title("Vaccination and Medicine History")
        
        text_widget = tk.Text(history_window, wrap='word', font=('Arial', 10))
        text_widget.insert(tk.END, df.to_string())
        text_widget.config(state='disabled')
        text_widget.pack(expand=True, fill='both')
    else:
        messagebox.showinfo("No Data", "No history found.")

# Initialize Tkinter window
root = tk.Tk()
root.title("Automated Student Vaccination & Medicine System")
root.geometry("400x500")

# Title label
title_label = tk.Label(root, text="Vaccination & Medicine Recommendation for Children", font=('Arial', 14))
title_label.pack(pady=10)

# Name input
name_label = tk.Label(root, text="Name:", font=('Arial', 12))
name_label.pack(pady=5)
name_entry = tk.Entry(root, width=30)
name_entry.pack(pady=5)

# Age input
age_label = tk.Label(root, text="Age (years):", font=('Arial', 12))
age_label.pack(pady=5)
age_entry = tk.Entry(root, width=30)
age_entry.pack(pady=5)

# City input
city_label = tk.Label(root, text="City:", font=('Arial', 12))
city_label.pack(pady=5)
city_entry = tk.Entry(root, width=30)
city_entry.pack(pady=5)

# Submit button
submit_button = tk.Button(root, text="Get Recommendation", command=submit, bg="lightblue", font=('Arial', 12))
submit_button.pack(pady=10)

# Label to show the result
result_label = tk.Label(root, text="", font=('Arial', 12), fg="green")
result_label.pack(pady=10)

# Button to show vaccination and medicine history
history_button = tk.Button(root, text="Show Vaccination/Medicine History", command=show_history, bg="lightgrey", font=('Arial', 12))
history_button.pack(pady=10)

# Run the Tkinter window loop
root.mainloop()
