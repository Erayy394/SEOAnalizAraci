import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup


# Pencere oluştur
pencere = tk.Tk()
pencere.title("SEO Uyum Kontrol Aracı")
pencere.geometry("400x250")
pencere.resizable(False, False)

# Başlık
etiket = tk.Label(pencere, text="SEO Uyum Kontrolü", font=("Arial", 16, "bold"))
etiket.pack(pady=20)

# URL ile analiz butonu
def url_analiz():
    url_pencere = tk.Toplevel()
    url_pencere.title("URL Gir")
    url_pencere.geometry("400x150")

    tk.Label(url_pencere, text="URL girin:").pack(pady=5)
    url_entry = tk.Entry(url_pencere, width=50)
    url_entry.pack(pady=5)

    def analiz_et():
        url = url_entry.get()
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            title = soup.title.string.strip() if soup.title else "Yok"
            title_len = len(title) if title != "Yok" else 0

            desc_tag = soup.find("meta", attrs={"name": "description"})
            description = desc_tag["content"].strip() if desc_tag and "content" in desc_tag.attrs else "Yok"
            desc_len = len(description) if description != "Yok" else 0

            h1 = soup.find("h1")
            h1_var = "Var" if h1 else "Yok"

            imgs = soup.find_all("img")
            img_alt_eksik = sum(1 for img in imgs if not img.get("alt"))

            sonuç = f"""
📄 Title: {title} ({title_len} karakter)
📝 Meta Description: {description} ({desc_len} karakter)
🔠 H1 Etiketi: {h1_var}
🖼️ Alt etiketi olmayan görsel sayısı: {img_alt_eksik} / {len(imgs)}
"""
            messagebox.showinfo("SEO Analiz Sonucu", sonuç)
        except Exception as e:
            messagebox.showerror("Hata", f"Sayfa analiz edilemedi: {str(e)}")

    tk.Button(url_pencere, text="Analiz Et", command=analiz_et).pack(pady=10)


url_buton = tk.Button(pencere, text="URL Girerek Analiz Et", width=30, command=url_analiz)
url_buton.pack(pady=10)

# HTML dosyası ile analiz butonu
def html_dosya_analiz():
    dosya_yolu = filedialog.askopenfilename(filetypes=[("HTML Dosyaları", "*.html *.htm")])
    if not dosya_yolu:
        return

    try:
        with open(dosya_yolu, "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string.strip() if soup.title else "Yok"
        title_len = len(title) if title != "Yok" else 0

        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and "content" in desc_tag.attrs else "Yok"
        desc_len = len(description) if description != "Yok" else 0

        h1 = soup.find("h1")
        h1_var = "Var" if h1 else "Yok"

        imgs = soup.find_all("img")
        img_alt_eksik = sum(1 for img in imgs if not img.get("alt"))

        sonuç = f"""
📄 Title: {title} ({title_len} karakter)
📝 Meta Description: {description} ({desc_len} karakter)
🔠 H1 Etiketi: {h1_var}
🖼️ Alt etiketi olmayan görsel sayısı: {img_alt_eksik} / {len(imgs)}
"""
        messagebox.showinfo("SEO Analiz Sonucu", sonuç)
    except Exception as e:
        messagebox.showerror("Hata", f"Dosya okunamadı: {str(e)}")


html_buton = tk.Button(pencere, text="HTML Dosyası Seçerek Analiz Et", width=30, command=html_dosya_analiz)
html_buton.pack(pady=10)

# Ana döngü
pencere.mainloop()
