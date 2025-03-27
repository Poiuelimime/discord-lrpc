import tkinter as tk
from tkinter import filedialog, messagebox
from pypresence import Presence
import os

def load_image():
    file_path = filedialog.askopenfilename(
        title="Выберите изображение",
        filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
    )
    if file_path:
        return file_path
    return None


def update_rpc():
    try:
        state = state_entry.get()
        details = details_entry.get()
        client_id = client_id_entry.get()

        if not state or not details:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все обязательные поля!")
            return

        if not client_id.isdigit() or len(client_id) != 18:
            messagebox.showwarning("Ошибка", "CLIENT_ID должен быть числовым значением из 18 цифр!")
            return

        large_image = large_image_path.get()
        small_image = small_image_path.get()

        if large_image and not os.path.exists(large_image):
            messagebox.showwarning("Ошибка", "Не удалось найти выбранное большое изображение!")
            return
        if small_image and not os.path.exists(small_image):
            messagebox.showwarning("Ошибка", "Не удалось найти выбранное маленькое изображение!")
            return

        large_image_key = os.path.basename(large_image).split('.')[0] if large_image else None
        small_image_key = os.path.basename(small_image).split('.')[0] if small_image else None
        rpc = Presence(client_id)
        rpc.connect()
        rpc.update(
            state=state,
            details=details,
            large_image=large_image_key,
            small_image=small_image_key,
            large_text="Большое изображение",  # Текст, который появится при наведении на большое изображение
            small_text="Маленькое изображение",  # Текст для маленького изображения
        )

        messagebox.showinfo("Успех", "RPC обновлен успешно!")

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")

root = tk.Tk()
root.title("Custom DiscordRPC By Lalka")
root.geometry("500x700")
root.configure(bg="#2e2e2e")
label_style = {"font": ("Helvetica", 12), "bg": "#2e2e2e", "fg": "#ffffff"}
entry_style = {"font": ("Helvetica", 12), "bg": "#383838", "fg": "#ffffff", "relief": "flat", "bd": 0, "insertbackground": "white"}
button_style = {"font": ("Helvetica", 12), "bg": "#4CAF50", "fg": "#ffffff", "activebackground": "#45a049", "relief": "flat", "bd": 0}
title_label = tk.Label(root, text="Настройка Discord RPC", font=("Helvetica", 16), bg="#2e2e2e", fg="#ffffff")
title_label.pack(pady=20)
tk.Label(root, text="Введите CLIENT_ID (18 цифр):", **label_style).pack(pady=5)
client_id_entry = tk.Entry(root, width=40, **entry_style)
client_id_entry.pack(pady=10)
tk.Label(root, text="Введите состояние (State):", **label_style).pack(pady=5)
state_entry = tk.Entry(root, width=40, **entry_style)
state_entry.pack(pady=10)
tk.Label(root, text="Введите подробности (Details):", **label_style).pack(pady=5)
details_entry = tk.Entry(root, width=40, **entry_style)
details_entry.pack(pady=10)
tk.Label(root, text="Выберите большое изображение:", **label_style).pack(pady=5)
large_image_button = tk.Button(root, text="Загрузить изображение", command=lambda: large_image_path.set(load_image()), **button_style)
large_image_button.pack(pady=10)
large_image_path = tk.StringVar()
large_image_label = tk.Label(root, textvariable=large_image_path, **label_style)
large_image_label.pack(pady=5)
tk.Label(root, text="Выберите маленькое изображение:", **label_style).pack(pady=5)
small_image_button = tk.Button(root, text="Загрузить изображение", command=lambda: small_image_path.set(load_image()), **button_style)
small_image_button.pack(pady=10)
small_image_path = tk.StringVar()
small_image_label = tk.Label(root, textvariable=small_image_path, **label_style)
small_image_label.pack(pady=5)
update_button = tk.Button(root, text="Обновить RPC", command=update_rpc, **button_style)
update_button.pack(pady=30)
def on_close():
    if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
        root.quit()
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
