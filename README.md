Sure! Here's the English version of your `README.md`, translated and polished for GitHub:

---

# Secure Message GUI

A sleek dark-themed graphical interface for encrypting and decrypting messages using SHA-1, custom AES-CTR, and custom RSA encryption.

## 💡 Features

- **SHA-1**: One-way hashing of messages (not decryptable).
- **AES-CTR**: Encryption and decryption using AES-128 in Counter (CTR) mode with a randomly generated session key and 64-bit nonce.
- **RSA**: Asymmetric encryption and decryption using custom-generated RSA keys (~4096 bits) created at program startup.
- **Dark GUI**: User-friendly interface built with Python’s Tkinter library, featuring:
  - A dropdown menu to select the algorithm
  - A text input field for the message
  - A result field for the output
  - Two buttons: “Encrypt” and “Decrypt” (Decrypt button is disabled when SHA-1 is selected)
- **Arabic Comments**: The source code is thoroughly commented in Egyptian Arabic to explain each section clearly.

---

## 🛠️ Requirements

- **Windows 10/11** with **Python 3.8+** pre-installed.
- **Tkinter** library (included by default on most Windows distributions).

> If Tkinter is not available, install it using:
> ```bash
> pip install tk
> ```

- No external dependencies; the entire project relies on Python’s standard library.

---

## 📦 Project Structure

```
project_root/
├─ crypto_gui.py      # Main GUI script and all crypto logic
└─ README.md          # This file
```

---

## 🚀 How to Run

1. Open a terminal in the project directory.
2. Run the following command:
   ```bash
   python3 crypto_gui.py
   ```
3. The application window will appear:
   - Choose an algorithm from the dropdown menu
   - Enter your message in the upper text box
   - Click “Encrypt” to generate the output in the lower box
   - If the algorithm supports decryption (AES-CTR or RSA), click “Decrypt” to reveal the original message

---

## 📝 Notes

- AES and RSA keys are randomly generated at runtime and are **not saved** to disk.
- All encrypted output is Base64 encoded to make it displayable and easy to share.

---

## 📜 License

This project is open-source. Feel free to use or modify it as needed.

---

Let me know if you'd like the GUI code for this as well.
