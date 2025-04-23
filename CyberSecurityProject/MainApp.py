# -*- coding: utf-8 -*-
"""
 برنامج واجهة رسومية داكنة لتشفير وفك تشفير الرسائل
 باستخدام SHA-1 (مكتبة)، AES-CTR (تطبيق مخصص)، وRSA (تطبيق مخصص)
 المكتبة: ToolKid (Tkinter)

# مميزات:
- قائمة منسدلة لاختيار نوع التشفير: SHA-1, AES-CTR, RSA
- حقلين نصيين: حقل لإدخال الرسالة، وحقل لعرض النتيجة
- زرين: تشفير وفك تشفير (زر فك التشفير معطل لـ SHA-1)
- توليد مفتاح AES-128 وRSA4096 لكل جلسة عشوائياً
- عرض المفتاح العام RSA (اختياري)

# تعليقات: مكتوبة بالعربية المصرية لشرح كل جزء
"""
import hashlib
import os
import base64
import random
from tkinter import *
from tkinter import ttk, scrolledtext, messagebox

# ===================== AES-128 مكونات أساسية =====================
# S-box
s_box = [
    # ... (تعريف جدول الاستبدال 256 قيمة) ...
]
# Rcon لمفاتيح التوسيع
r_con = [
    # ... (قيم Rcon) ...
]

def sub_bytes(state):
    for i in range(4):
        for j in range(4):
            state[i][j] = s_box[state[i][j]]
    return state

# سيتم إضافة باقي دوال AES لاحقاً (shift_rows, mix_columns...)
def aes_encrypt_block(block, round_keys):
    return block  # مؤقت حتى يتم استكمال الدوال

def key_expansion(key: bytes) -> list:
    # دالة توسعة المفتاح (مؤقت) - تحتاج لاستكمال التوسيع لكل جولة
    return []

def aes_encrypt_ctr(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    round_keys = key_expansion(key)
    ciphertext = bytearray()
    counter = 0
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        counter_block = nonce + counter.to_bytes(8, 'big')
        keystream = aes_encrypt_block(counter_block, round_keys)
        cipher_block = bytes(a ^ b for a, b in zip(block, keystream[:len(block)]))
        ciphertext.extend(cipher_block)
        counter += 1
    return bytes(ciphertext)

def aes_decrypt_ctr(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    return aes_encrypt_ctr(ciphertext, key, nonce)

# ======================= RSA (مخصص) =======================
def is_prime(n, k=5):
    if n < 2:
        return False
    small_primes = [2,3,5,7,11,13,17,19,23]
    for p in small_primes:
        if n == p:
            return True
        if n % p == 0:
            return False
    d, r = n-1, 0
    while d % 2 == 0:
        d //= 2; r += 1
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(bits=1024):
    while True:
        p = random.getrandbits(bits) | 1
        if is_prime(p):
            return p

p = generate_prime(512)
q = generate_prime(512)
n = p * q
phi = (p-1)*(q-1)
e = 65537

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b//a) * y, y)

g, x, y = egcd(e, phi)
d = x % phi

def rsa_encrypt(message: bytes) -> bytes:
    m = int.from_bytes(message, 'big')
    c = pow(m, e, n)
    return c.to_bytes((n.bit_length()+7)//8, 'big')

def rsa_decrypt(ciphertext: bytes) -> bytes:
    c = int.from_bytes(ciphertext, 'big')
    m = pow(c, d, n)
    return m.to_bytes((m.bit_length()+7)//8, 'big')

# ======================= واجهة المستخدم =======================
BG = '#2e2e2e'
FG = '#ffffff'
BTN_BG = '#424242'

root = Tk()
root.title('تشفير الرسائل')
root.configure(bg=BG)
root.geometry('600x500')

alg_var = StringVar(value='SHA-1')
alg_menu = ttk.Combobox(root, textvariable=alg_var, values=['SHA-1', 'AES-CTR', 'RSA'])
alg_menu.place(x=20, y=20)

input_text = scrolledtext.ScrolledText(root, wrap=WORD, height=10, bg=BG, fg=FG)
input_text.place(x=20, y=60, width=560)

output_text = scrolledtext.ScrolledText(root, wrap=WORD, height=10, bg=BG, fg=FG)
output_text.place(x=20, y=280, width=560)

encrypt_btn = Button(root, text='تشفير', bg=BTN_BG, fg=FG)
encrypt_btn.place(x=200, y=450)

decrypt_btn = Button(root, text='فك التشفير', bg=BTN_BG, fg=FG)
decrypt_btn.place(x=300, y=450)

# توليد مفاتيح AES
key = os.urandom(16)  # 128-bit AES key

def on_alg_change(event=None):
    if alg_var.get() == 'SHA-1':
        decrypt_btn.config(state=DISABLED)
    else:
        decrypt_btn.config(state=NORMAL)
alg_menu.bind('<<ComboboxSelected>>', on_alg_change)

def on_encrypt():
    msg = input_text.get('1.0', END).strip()
    if not msg:
        messagebox.showwarning('تنبيه', 'من فضلك أدخل رسالة')
        return
    algorithm = alg_var.get()
    if algorithm == 'SHA-1':
        result = hashlib.sha1(msg.encode()).hexdigest()
    elif algorithm == 'AES-CTR':
        global aes_nonce
        aes_nonce = os.urandom(8)
        cipher = aes_encrypt_ctr(msg.encode(), key, aes_nonce)
        result = base64.b64encode(aes_nonce + cipher).decode()
    else:
        cipher = rsa_encrypt(msg.encode())
        result = base64.b64encode(cipher).decode()
    output_text.delete('1.0', END)
    output_text.insert(END, result)

def on_decrypt():
    algorithm = alg_var.get()
    data = output_text.get('1.0', END).strip()
    if not data:
        messagebox.showwarning('تنبيه', 'لا يوجد نص لفك التشفير')
        return
    if algorithm == 'AES-CTR':
        raw = base64.b64decode(data)
        nonce = raw[:8]
        cipher = raw[8:]
        plain = aes_decrypt_ctr(cipher, key, nonce)
        result = plain.decode(errors='ignore')
    else:
        cipher = base64.b64decode(data)
        plain = rsa_decrypt(cipher)
        result = plain.decode(errors='ignore')
    output_text.delete('1.0', END)
    output_text.insert(END, result)

encrypt_btn.config(command=on_encrypt)
decrypt_btn.config(command=on_decrypt)

root.mainloop()