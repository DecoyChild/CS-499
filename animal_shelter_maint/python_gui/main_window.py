# GUI for users to maintain and view the Animal Shelter Database
# Using Tkinter library 
# Use the DEBUG option to print to the console

import tkinter as tk
from tkinter import ttk, messagebox
from animal_shelter_crud import AnimalShelter

#
# Fill the field with the search results 
#
def fill_results():

    # Clear the text field 
    text_box.delete("1.0","end")

    # Setup the search set
    search_set = {combo.get(): search_entry.get()} 

    if DEBUG:
        print(search_set)

    # Get the results from the database object
    search_results = aac.read(search_set)
    
    if DEBUG:
        print(len(search_results))

    # Display the data if any results were found
    text_box.insert(tk.END, f"Found {len(search_results)} Record(s)\n")
    text_box.insert(tk.END, f"******************************************\n")
    if len(search_results) > 0:
        for animal in search_results:
            for key, value in animal.items():
                text_box.insert(tk.END, f"{key}: {value}\n")
            text_box.insert(tk.END, "\n")

#
# CREATE RECORD WINDOW
#
def open_create_window():

    # insert the record from a dictionary
    def insert_record():
        # Disable the button to avoid double clicks
        create_rec_button.config(state=tk.DISABLED)
        print("Inserting record...")

        # Creating a dictionary by parsing through the entries
        # This will use the input labels as the database fields
        insert_data = {field:entry.get() for field, entry in entries.items()}
        
        if DEBUG:
            print(insert_data)       

        # Will return True if the insert was a success
        record_created = aac.create(insert_data)

        # Display the status of the insert
        if record_created:
            messagebox.showinfo("Insert Record", "Record was added!")
        else:
            messagebox.showinfo("Insert Record", "Record was not added!")                

        # Clear the input fiels to avoid accidental duplicates
        for entry in entries.items():
            entry[1].delete(0, tk.END)

        # Activate the button again 
        create_rec_button.config(state=tk.NORMAL)
    global create_record_window

    # If the window hasn't already been created then create one
    if create_record_window is None or not create_record_window.winfo_exists():
        create_record_window = tk.Toplevel(main_window)
        create_record_window.title("Add Record")
        create_record_window.geometry("400x325")

        # Dynamically add fields for the insert / create records
        # The fields added here will be the fields used in the database
        text_fields = ['breed','animal_type','name','color','age_upon_outcome','date_of_birth',
                       'outcome_type','sex_upon_outcome','animal_id']
        
        # Dictionary for the entry inputs
        entries = {}

        # Creating the text and input fields  
        for i, field in enumerate(text_fields):
            # Creating the labels 
            label = tk.Label(create_record_window, text=field + ':')
            label.grid(row=i, column=0,sticky='e', padx=10, pady=5)

            # Creating the entries
            entry = tk.Entry(create_record_window)
            entry.grid(row=i, column=1, padx=10, pady=5)
            
            entries[field] = entry

        # Adding the button at the end at the index after the last set
        create_rec_button = ttk.Button(create_record_window, text="Create Record", command=insert_record)
        create_rec_button.grid(row=len(text_fields), column=1,padx=10, pady=10)

    else:
        # If the window is already open bring it to focus 
        create_record_window.lift()
        create_record_window.focus_force()


DEBUG = 1

# create the animal shelter object (need a mongo DB to )
aac = AnimalShelter('aacuser','Rt$&9012!@','localhost',27017,'aac','animals')

# Initialize the main window
main_window = tk.Tk()
main_window.title('Animal Shelter Database Maintenance Window')
main_window.geometry("800x950")

create_record_window = None

# Frame from the main window
frame = tk.Frame(main_window)
frame.pack()

message_label = tk.Label(frame, 
                         text='Maintain the Animal Shelter Database',
                         font=('Arial', 16, 'bold'), 
                         fg='green')
message_label.grid(row=0, column = 0, pady=5)

# Frame for the results text box
results_frame = tk.Frame(main_window)
results_frame.pack()

# Frame for the search options 
database_query_frame = tk.LabelFrame(frame, text="Search...")
database_query_frame.grid(row=1, column=0, pady=30)

# Can add more chooices and the query will find the field
# Only searching by one field at a time for now
choices = ["breed", "animal_type", "name", "animal_id"]

combo = ttk.Combobox(database_query_frame, values=choices, state="readonly")
combo.set("Search Options")  # Set placeholder text
combo.grid(row=0, column=0, padx=10, pady=5)
search_entry = tk.Entry(database_query_frame)
search_entry.grid(row=0, column=1, padx=10, pady=5)

# Button that runs the search
search_button = ttk.Button(database_query_frame, text="Search", command=fill_results)
search_button.grid(row=0, column=3,padx=10, pady=5)

# the text box that displays the results
text_box = tk.Text(results_frame, wrap=tk.WORD, height=40, width=60)
text_box.grid(row=1, column = 0)

# Button to open the insert a single record
create_button = ttk.Button(results_frame, text="Insert New Record", command=open_create_window)
create_button.grid(row=0, column=0,padx=10, pady=5)

## Message for upcoming features
message_label = tk.Label(results_frame, 
                         text="Update and Delete Record Coming Soon",
                         font=("Arial", 16), 
                         fg="red")
message_label.grid(row=2, column = 0, pady=30)

# Start the event loop
main_window.mainloop()