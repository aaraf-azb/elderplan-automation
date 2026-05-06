import tkinter as tk
from tkinter import filedialog
import threading

from main import run


# --- GLOBAL ---
stop_flag = {"stop": False}


# --- FUNCTIONS ---
def browse_csv():
    file = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file:
        collection_var.set(file)


def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_var.set(folder)


def log_to_gui(msg):

    def append():
        log_box.insert(tk.END, msg + "\n")
        log_box.see(tk.END)

    root.after(0, append)


def update_progress(current, total):

    root.after(
        0,
        lambda: progress_label.config(
            text=f"{current}/{total}"
        )
    )


def run_wrapper(
    csv_file,
    output_folder,
    entry_size
):

    try:

        run(
            csv_file,
            output_folder,
            entry_size,
            stop_flag,
            update_progress,
            log_to_gui
        )

        log_to_gui("✅ Automation completed")

    except Exception as e:

        log_to_gui(f"❌ ERROR: {str(e)}")

        log_to_gui("⛔ Automation stopped due to error")

def start_process():
    csv_file = collection_var.get()
    output_folder = output_var.get()
    entry_text = entry_size_var.get().strip()

    # Validation
    if not csv_file:
        log_to_gui("❌ Select CSV file")
        return

    if not output_folder:
        log_to_gui("❌ Select output folder")
        return

    # Entry size (optional)
    if entry_text == "":
        entry_size = None
    else:
        try:
            entry_size = int(entry_text)
        except ValueError:
            log_to_gui("❌ Entry size must be a number")
            return

    stop_flag["stop"] = False
    log_box.delete("1.0", tk.END)

    thread = threading.Thread(
    target=run_wrapper,
        args=(
            csv_file,
            output_folder,
            entry_size
        ),
        daemon=True
    )
    thread.start()


def stop_process():
    stop_flag["stop"] = True
    log_to_gui("⚠ Stop requested")


# --- UI ---
root = tk.Tk()
root.title("Claim Automation")
root.geometry("600x400")


# Variables
collection_var = tk.StringVar()
output_var = tk.StringVar()
entry_size_var = tk.StringVar(value="")


# ===== ROW 1: Collection File =====
tk.Label(root, text="Collection File").grid(row=0, column=0, padx=10, pady=10, sticky="w")

tk.Entry(root, textvariable=collection_var, width=50).grid(row=0, column=1)

tk.Button(root, text="Browse", command=browse_csv).grid(row=0, column=2, padx=5)


# ===== ROW 2: Output Folder =====
tk.Label(root, text="Output Folder").grid(row=1, column=0, padx=10, pady=10, sticky="w")

tk.Entry(root, textvariable=output_var, width=50).grid(row=1, column=1)

tk.Button(root, text="Browse", command=browse_folder).grid(row=1, column=2, padx=5)


# ===== ROW 3: Entry Size =====
tk.Label(root, text="Entry Size").grid(row=2, column=0, padx=10, pady=10, sticky="w")

tk.Entry(root, textvariable=entry_size_var, width=10).grid(row=2, column=1, sticky="w")


# ===== BUTTONS =====
button_frame = tk.Frame(root)
button_frame.grid(row=3, column=0, columnspan=3, pady=15)

tk.Button(button_frame, text="Start", bg="green", fg="white", width=10,
          command=start_process).pack(side="left", padx=10)

tk.Button(button_frame, text="Stop", bg="red", fg="white", width=10,
          command=stop_process).pack(side="left", padx=10)


# ===== PROGRESS =====
progress_label = tk.Label(root, text="Idle")
progress_label.grid(row=4, column=0, columnspan=3)


# ===== LOG =====
tk.Label(root, text="Log").grid(row=5, column=0, padx=10, sticky="w")

log_box = tk.Text(root, height=12)
log_box.grid(row=6, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

scrollbar = tk.Scrollbar(log_box)
scrollbar.pack(side="right", fill="y")
log_box.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=log_box.yview)


# Resize behavior
root.grid_rowconfigure(6, weight=1)
root.grid_columnconfigure(1, weight=1)


root.mainloop()
