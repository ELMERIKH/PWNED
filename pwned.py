import tkinter as tk
import threading
import time
import random
import string
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
def send_message():
    message = entry.get()
    if message.lower() == "yesmylord":
        root.destroy()  # Exit the program if the user types "yesmylord"
    elif message:
        # Write the user message to the ss.txt file
        with open("ss.txt", "a") as user_file:
            user_file.write(message + "\n")

        chat_display.insert(tk.END, "You: " + message + "\n", "You")
        entry.delete(0, tk.END)

        # Send the user message to the command line and get the response
        response = get_cmd_response(message)

        # Write the response to the kk.txt file
        with open("kk.txt", "a") as response_file:
            response_file.write(response + "\n")

        show_response("Anonymous: " + response + "\n")

def show_response(response, delay=0.04):
    anonymous_part = response.split(":")[0]  # Extract "Anonymous" part
    message_part = response.split(":")[1] if ":" in response else ""  # Extract message part

    # Display "Anonymous:" immediately
    chat_display.insert(tk.END, f"{anonymous_part}:", "Anonymous")
    chat_display.yview(tk.END)  # Auto-scroll to show the latest message
    root.update_idletasks()  # Update the window immediately

    # Display the message part slowly
    for char in f" {message_part}":
        chat_display.insert(tk.END, char, "Anonymous")
        chat_display.yview(tk.END)  # Auto-scroll to show the latest message
        root.update_idletasks()  # Update the window immediately
        time.sleep(delay)  # Delay between each character

def bring_to_front():
    while True:
        root.lift()
        root.attributes('-topmost', 1)
        time.sleep(0.1)

def get_cmd_response(user_message):
    # Pass the user message to the command line and get the response
    print(user_message)  # Print the user message to the console

    cmd = input("Enter response in the command line: ")  # Type the response in the command line
    return cmd.strip()

def matrix_effect():
    min_matrix_lines = 20
    initial_lines = 45  # Adjust this value as needed
    matrix_lines = [
        "".join(random.choice(string.ascii_letters + string.punctuation) for _ in range(screen_width))
        for _ in range(initial_lines)
    ]
    matrix_speed = 0.05
    clear_interval = 70  # Number of iterations before clearing the matrix_lines list

    iteration_count = 0

    def update_matrix():
        nonlocal iteration_count, matrix_lines

        matrix_line = [random.choice(string.ascii_letters + string.punctuation) for _ in range(screen_width)]
        matrix_lines.append("".join(matrix_line))

        # Ensure a minimum number of lines
        while len(matrix_lines) < min_matrix_lines:
            matrix_lines.append("".join([random.choice(string.ascii_letters + string.punctuation) for _ in range(screen_width)]))

        matrix_lines = matrix_lines[-screen_height:]  # Limit the number of lines

        matrix_text = "\n".join(matrix_lines)
        matrix_label.config(text=matrix_text)
        root.update_idletasks()  # Update the window immediately

        iteration_count += 1

        # Clear the matrix_lines list periodically to prevent lag
        if iteration_count % clear_interval == 0:
            initial_lines = 45  # Adjust this value as needed
            matrix_lines = [
                "".join(random.choice(string.ascii_letters + string.punctuation) for _ in range(screen_width))
                for _ in range(initial_lines)
            ]

        root.after(int(matrix_speed * 1000), update_matrix)

    update_matrix()
kk_file_path = "kk.txt"
if not os.path.exists(kk_file_path):
    with open(kk_file_path, "w") as kk_file:
        pass  # Create an empty file
# File system event handler for monitoring changes in files
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("ss.txt"):
            # Handle changes in ss.txt (user messages)
            with open("ss.txt", "r") as user_file:
                lines = user_file.readlines()
                if lines:
                    user_message = lines[-1].strip()
                   

        elif event.src_path.endswith("kk.txt"):
            # Handle changes in kk.txt (responses)
            with open("kk.txt", "r") as response_file:
                lines = response_file.readlines()
                if lines:
                    response = lines[-1].strip()
                    show_response("Anonymous: " + response + "\n")

# Create the main window
root = tk.Tk()
root.title("the Box")

bring_to_front_thread = threading.Thread(target=bring_to_front)
bring_to_front_thread.start()

# Set the background color to black
root.configure(bg='black')

# Get the screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the window position to cover the whole screen
x_position = 0
y_position = 0

root.geometry(f"{screen_width}x{screen_height}+{x_position}+{y_position}")

# Make the window borderless
root.overrideredirect(True)

# Create a frame for the matrix labels
matrix_frame = tk.Frame(root, bg='black')
matrix_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

# Create a label for the matrix effect
matrix_label = tk.Label(matrix_frame, text="", font=("Courier", 12), bg='black', fg='green', justify='left')
matrix_label.pack(fill='both', expand=True)  # Expand the label to fill all available space

# Create a Text widget for displaying the chat
chat_display = tk.Text(root, height=20, width=50, bg='black', fg='green', bd=2, insertbackground='green', selectbackground='green')
chat_display.tag_configure("You", foreground="green")
chat_display.tag_configure("Anonymous", foreground="green")
chat_display.pack(pady=10)

# Add a default message from the chat bot at the start after a delay
default_bot_message = "Anonymous: Hello you have been hacked!\n"
root.after(2000, lambda: show_response(default_bot_message, delay=0.1))  # Delayed display

# Create an Entry widget for typing messages
entry = tk.Entry(root, width=50, bg='black', fg='green', bd=2, insertbackground='green')
entry.pack(pady=10)

# Create a button for sending messages
send_button = tk.Button(root, text="Send", command=send_message, bg='black', fg='green')
send_button.pack()

# Create a label for the input box
input_label = tk.Label(root, text="Type your message:", bg='black', fg='green')
input_label.pack()

# Bind the Enter key to the send_message function
root.bind("<Return>", lambda event: send_message())

# Set up the file system event handler and observer
file_change_handler = FileChangeHandler()
observer = Observer()
observer.schedule(file_change_handler, path=".", recursive=False)
observer.start()

# Run the Tkinter event loop
# Ensure the window appears above others initially

# Run the matrix effect in a separate thread
matrix_effect_thread = threading.Thread(target=matrix_effect)
matrix_effect_thread.start()

root.mainloop()

# Stop the observer when the Tkinter window is closed
observer.stop()
observer.join()
