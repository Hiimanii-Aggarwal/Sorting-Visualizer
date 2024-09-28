import tkinter as tk
import random
import time
from tkinter import messagebox

# Initialize the main window
root = tk.Tk()
root.title("Sorting Visualizer")
root.maxsize(900, 600)
root.config(bg='black')

# Variables
data = []
canvas_height = 400
canvas_width = 800
bar_width = 20
speed = 0.001  # Minimum time for faster sorting

# Create a Canvas
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack(pady=20)

# Function to draw the data (bars) on canvas
def draw_data(data, color_array):
    canvas.delete("all")
    for i, val in enumerate(data):
        x0 = i * bar_width
        y0 = canvas_height - val
        x1 = (i + 1) * bar_width
        y1 = canvas_height

        canvas.create_rectangle(x0, y0, x1, y1, fill=color_array[i])
    root.update_idletasks()

# Generate random data
def generate_random_data():
    global data
    data = [random.randint(10, canvas_height) for _ in range(int(canvas_width / bar_width))]
    draw_data(data, ['blue' for _ in range(len(data))])

# Function to generate array from user input
def generate_user_input_data():
    global data
    input_data = input_entry.get()
    try:
        data = list(map(int, input_data.split(',')))  # Convert input string to list of integers
        if len(data) > int(canvas_width / bar_width):
            messagebox.showerror("Error", "Too many elements! Please enter fewer values.")
        else:
            draw_data(data, ['blue' for _ in range(len(data))])
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid list of integers separated by commas.")

# Bubble Sort Algorithm
def bubble_sort():
    for i in range(len(data)-1):
        for j in range(len(data)-i-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                draw_data(data, ['green' if x == j or x == j+1 else 'blue' for x in range(len(data))])
                time.sleep(speed)
    draw_data(data, ['green' for x in range(len(data))])

# Insertion Sort Algorithm
def insertion_sort():
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            draw_data(data, ['green' if x == j or x == j+1 else 'blue' for x in range(len(data))])
            time.sleep(speed)
        data[j + 1] = key
    draw_data(data, ['green' for x in range(len(data))])

# Selection Sort Algorithm
def selection_sort():
    for i in range(len(data)):
        min_idx = i
        for j in range(i+1, len(data)):
            if data[j] < data[min_idx]:
                min_idx = j
            draw_data(data, ['yellow' if x == j else 'blue' for x in range(len(data))])
            time.sleep(speed)
        data[i], data[min_idx] = data[min_idx], data[i]
        draw_data(data, ['green' if x <= i else 'blue' for x in range(len(data))])

# Quick Sort Algorithm
def quick_sort(low, high):
    if low < high:
        pi = partition(low, high)
        quick_sort(low, pi - 1)
        quick_sort(pi + 1, high)
        draw_data(data, ['green' if x >= low and x <= high else 'blue' for x in range(len(data))])
        time.sleep(speed)

def partition(low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
            draw_data(data, ['yellow' if x == j or x == i else 'blue' for x in range(len(data))])
            time.sleep(speed)
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

# Merge Sort Algorithm
def merge_sort(low, high):
    if low < high:
        mid = (low + high) // 2
        merge_sort(low, mid)
        merge_sort(mid + 1, high)
        merge(low, mid, high)
        draw_data(data, ['green' if x >= low and x <= high else 'blue' for x in range(len(data))])
        time.sleep(speed)

def merge(low, mid, high):
    left = data[low:mid+1]
    right = data[mid+1:high+1]
    i = j = 0
    k = low
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        data[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        data[k] = right[j]
        j += 1
        k += 1

# Speed scale adjustment
def set_speed(val):
    global speed
    speed = float(val)

# UI Setup: buttons, dropdowns, etc.
UI_frame = tk.Frame(root, width=600, height=200, bg='grey')
UI_frame.pack(padx=10, pady=5)

tk.Label(UI_frame, text="Sorting Algorithm", bg='grey').grid(row=0, column=0, padx=10, pady=5)
alg_menu = tk.StringVar()
alg_menu.set("Bubble Sort")
alg_dropdown = tk.OptionMenu(UI_frame, alg_menu, "Bubble Sort", "Insertion Sort", "Selection Sort", "Quick Sort", "Merge Sort")
alg_dropdown.grid(row=0, column=1, padx=5, pady=5)

tk.Label(UI_frame, text="Speed (sec)", bg='grey').grid(row=1, column=0, padx=10, pady=5)
speed_scale = tk.Scale(UI_frame, from_=0.001, to=2.0, length=200, digits=3, resolution=0.001, orient=tk.HORIZONTAL, command=set_speed)
speed_scale.grid(row=1, column=1, padx=5, pady=5)
speed_scale.set(0.001)  # Default minimum speed

# Text entry for user input array
tk.Label(UI_frame, text="Enter Array (comma separated)", bg='grey').grid(row=2, column=0, padx=10, pady=5)
input_entry = tk.Entry(UI_frame)
input_entry.grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(UI_frame, text="Generate Random Array", command=generate_random_data).grid(row=0, column=2, padx=5, pady=5)
tk.Button(UI_frame, text="Generate User Array", command=generate_user_input_data).grid(row=2, column=2, padx=5, pady=5)

# Start button
tk.Button(UI_frame, text="Start Sorting", command=lambda: start_sorting(alg_menu.get())).grid(row=1, column=2, padx=5, pady=5)

# Start Sorting
def start_sorting(algorithm):
    if algorithm == "Bubble Sort":
        bubble_sort()
    elif algorithm == "Insertion Sort":
        insertion_sort()
    elif algorithm == "Selection Sort":
        selection_sort()
    elif algorithm == "Quick Sort":
        quick_sort(0, len(data) - 1)
    elif algorithm == "Merge Sort":
        merge_sort(0, len(data) - 1)

# Run the GUI
root.mainloop()
