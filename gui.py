import tkinter as tk
from tkinter import filedialog, messagebox
from steg import embed_data, extract_data
from crypto import generate_key, encrypt_message, decrypt_message
import pyperclip  # To copy the key to clipboard

def embed():
    """Handles embedding data into an image."""
    input_image = filedialog.askopenfilename(
        title="Select Image", 
        filetypes=[("PNG Files", "*.png")]
    )
    if not input_image:
        return

    output_image = filedialog.asksaveasfilename(
        defaultextension=".png", 
        title="Save Stego Image", 
        filetypes=[("PNG Files", "*.png")]
    )
    if not output_image:
        return

    message = text_entry.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Error", "Please enter a message.")
        return

    # Encrypt the message before embedding.
    key = generate_key()
    encrypted = encrypt_message(message, key)
    try:
        embed_data(input_image, output_image, encrypted)
        
        # Display the key in a label that the user can copy
        key_label.config(text=f"Encryption Key: {key.decode()}")
        
        # Inform user the data was embedded successfully
        messagebox.showinfo("Success", "Data embedded successfully!\nEncryption Key displayed below.")
        
    except Exception as e:
        messagebox.showerror("Error", str(e))

def extract():
    """Handles extraction of data from a stego image."""
    stego_image = filedialog.askopenfilename(
        title="Select Stego Image", 
        filetypes=[("PNG Files", "*.png")]
    )
    if not stego_image:
        return

    key = key_entry.get().strip()
    if not key:
        messagebox.showerror("Error", "Please enter the encryption key.")
        return

    try:
        encrypted = extract_data(stego_image)
        decrypted = decrypt_message(encrypted, key.encode())
        text_entry.delete("1.0", tk.END)
        text_entry.insert(tk.END, decrypted)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def copy_key():
    """Copies the encryption key to the clipboard."""
    key = key_label.cget("text").replace("Encryption Key: ", "")
    if key:
        pyperclip.copy(key)
        messagebox.showinfo("Key Copied", "Encryption key has been copied to clipboard!")

def main():
    global text_entry, key_entry, key_label
    root = tk.Tk()
    root.title("Steganography Tool")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Label(frame, text="Message:").grid(row=0, column=0, sticky="nw")
    text_entry = tk.Text(frame, width=40, height=10)
    text_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

    tk.Label(frame, text="Encryption Key (for extraction):").grid(row=1, column=0, sticky="w")
    key_entry = tk.Entry(frame, width=40)
    key_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Button(frame, text="Embed", command=embed).grid(row=2, column=1, pady=5)
    tk.Button(frame, text="Extract", command=extract).grid(row=2, column=2, pady=5)

    # Label to display encryption key after embedding
    key_label = tk.Label(frame, text="Encryption Key: ", fg="blue", font=("Helvetica", 10, "italic"))
    key_label.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

    # Button to copy the key to clipboard
    copy_button = tk.Button(frame, text="Copy Key to Clipboard", command=copy_key)
    copy_button.grid(row=4, column=1, columnspan=2, pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
