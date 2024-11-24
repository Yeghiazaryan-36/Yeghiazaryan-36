import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import requests
from bs4 import BeautifulSoup
import urllib.parse  # Նոր գրադարան URL-ների կոդավորման համար

def search_wikipedia(term):
    """Որոնում է Wikipedia-ում և վերադարձնում է ամփոփագիրը՝ աջակցելով հայերենին։"""
    try:
        # Կոդավորում ենք որոնման տերմինը URL-ի համար
        encoded_term = urllib.parse.quote(term)
        url = f"https://hy.wikipedia.org/wiki/{encoded_term}"  # hy.wikipedia.org՝ հայերեն Wikipedia
        response = requests.get(url)
        
        # Ստուգում ենք՝ էջը կա՞
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Փորձում ենք գտնել առաջին պարագրաֆը բովանդակությամբ
            paragraphs = soup.find_all('p')
            for para in paragraphs:
                if para.text.strip():  # Խուսափում ենք դատարկ պարագրաֆներից
                    return para.text.strip()
            
            return "Էջում նշանակալի բովանդակություն չկա։"
        elif response.status_code == 404:
            return "Wikipedia-ի էջը չի գտնվել։"
        else:
            return f"Սխալ՝ ստացվեց {response.status_code} կոդ։"
    except Exception as e:
        return f"Տվյալների ներբեռնման սխալ՝ {e}"

def on_double_click():
    """Բացում է նոր պատուհան՝ որոնման համար։"""
    search_window = tk.Toplevel(root)
    search_window.title("Wikipedia Որոնում")
    search_window.geometry("600x400")
    search_window.configure(bg="#f9f9f9")

    # Մուտքի դաշտ
    label = tk.Label(search_window, text="Մուտքագրեք որոնման բառը:", font=("Arial", 14), bg="#f9f9f9")
    label.pack(pady=10)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(search_window, textvariable=search_var, font=("Arial", 12), width=40)
    search_entry.pack(pady=10)

    # Արդյունքների դաշտ
    result_box = tk.Text(search_window, wrap="word", font=("Arial", 12), height=15, width=60)
    result_box.pack(pady=10)

    def perform_search():
        term = search_var.get()
        if term.strip():
            result_box.delete("1.0", tk.END)
            result = search_wikipedia(term)
            result_box.insert(tk.END, result)
        else:
            messagebox.showwarning("Սխալ մուտքագրում", "Խնդրում ենք մուտքագրել որոնման բառ։")

    search_button = ttk.Button(search_window, text="Որոնել", command=perform_search)
    search_button.pack(pady=5)

# Հիմնական պատուհան
root = tk.Tk()
root.title("Google Կոնֆիգուրատոր")
root.geometry("800x600")
root.configure(bg="#add8e6")  # Բաց կապույտ ֆոն

# Google պատկեր
try:
    icon_image = Image.open("google_icon.png")  # Փոխարինեք ձեր պատկերով
    icon_image = icon_image.resize((64, 64), Image.Resampling.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_image)
    
    icon_button = tk.Label(root, image=icon_photo, bg="#add8e6", cursor="hand2")
    icon_button.pack(pady=50)

    icon_button.bind("<Double-1>", lambda e: on_double_click())

except FileNotFoundError:
    messagebox.showerror("Սխալ", "Google-ի պատկերն չի գտնվել։ Խնդրում ենք ավելացնել 'google_icon.png'-ը նույն պանակում։")

root.mainloop()
