import tkinter as tk
from tkinter import messagebox
import random

class SayiTahminOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sayı Tahmin Oyunu")
        self.root.geometry("350x550")
        
        self.max_hak = 5 # Görseldeki gibi tahmini 5 satır/hak tanımlıyoruz
        self.kalan_hak = self.max_hak
        self.hedef_sayi = ""
        self.satir_sayaci = 0
        
        # Arayüz Elemanları
        self.baslik_label = tk.Label(root, text="4 Basamaklı Sayıyı Bul!", font=("Arial", 16, "bold"))
        self.baslik_label.pack(pady=10)
        
        self.hak_label = tk.Label(root, text=f"Kalan Hakkın: {self.kalan_hak}", font=("Arial", 12))
        self.hak_label.pack()
        
        self.entry_tahmin = tk.Entry(root, font=("Arial", 14), width=10, justify="center")
        self.entry_tahmin.pack(pady=10)
        
        self.tahmin_btn = tk.Button(root, text="Tahmin Et", font=("Arial", 12), command=self.tahmin_et)
        self.tahmin_btn.pack()
        
        # Önceki tahminlerin gösterileceği çerçeve (Grid)
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack(pady=20)
        
        # Oyunu ilk kez başlat
        self.oyunu_baslat()
        
    def oyunu_baslat(self):
        self.kalan_hak = self.max_hak
        self.satir_sayaci = 0
        self.hak_label.config(text=f"Kalan Hakkın: {self.kalan_hak}")
        self.entry_tahmin.delete(0, tk.END)
        self.hedef_sayi = self.rastgele_sayi_uret()
        
        # Yeni oyunda ekrandaki eski kutucukları temizle
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
    def rastgele_sayi_uret(self):
        # 1. Revizyon: Rakamları birbirinden farklı sayı üretme
        ilk_rakam = str(random.randint(1, 9))
        havuz = list("0123456789")
        havuz.remove(ilk_rakam)
        kalan_rakamlar = random.sample(havuz, 3)
        return ilk_rakam + "".join(kalan_rakamlar)
        
    def tahmin_et(self):
        if self.kalan_hak <= 0:
            return
            
        tahmin = self.entry_tahmin.get()
        
        # Uzunluk ve sayı olma kontrolü
        if len(tahmin) != 4 or not tahmin.isdigit():
            messagebox.showwarning("Geçersiz Giriş", "Lütfen 4 basamaklı bir sayı girin!")
            return
            
        # 2. Revizyon: Kullanıcının tahmininin rakamları farklı mı kontrolü
        if len(set(tahmin)) != 4:
            messagebox.showwarning("Geçersiz Giriş", "Lütfen rakamları birbirinden farklı bir sayı girin!")
            return
            
        # Renkleri belirle ve ekrana kutucuklar (Label) halinde yazdır
        for sutun, rakam in enumerate(tahmin):
            renk = "black"
            yazi_rengi = "white"
            
            if rakam == self.hedef_sayi[sutun]:
                renk = "green" # Doğru rakam, doğru yer
            elif rakam in self.hedef_sayi:
                renk = "gold"  # Doğru rakam, yanlış yer (Sarı)
                yazi_rengi = "black"
                
            # Görseldeki gibi kare kutular oluşturuyoruz
            lbl = tk.Label(self.grid_frame, text=rakam, bg=renk, fg=yazi_rengi,
                           font=("Arial", 16, "bold"), width=4, height=2, relief="solid")
            lbl.grid(row=self.satir_sayaci, column=sutun, padx=5, pady=5)
            
        # Değerleri güncelle
        self.satir_sayaci += 1
        self.kalan_hak -= 1
        self.hak_label.config(text=f"Kalan Hakkın: {self.kalan_hak}")
        self.entry_tahmin.delete(0, tk.END)
        
        # Oyun bitiş durumları
        if tahmin == self.hedef_sayi:
            messagebox.showinfo("Tebrikler!", f"Kazandınız! Doğru sayı {self.hedef_sayi} idi.")
            self.oyunu_baslat()
        elif self.kalan_hak == 0:
            messagebox.showerror("Oyun Bitti", f"Maalesef tüm haklarınız bitti.\nDoğru sayı: {self.hedef_sayi}")
            self.oyunu_baslat()

# Programı çalıştıran ana döngü
if __name__ == "__main__":
    root = tk.Tk()
    oyun = SayiTahminOyunu(root)
    # İmleci direkt giriş kutusuna odakla
    oyun.entry_tahmin.focus_set()
    # Enter tuşuna basıldığında da tahmin et butonunu tetikle
    root.bind('<Return>', lambda event: oyun.tahmin_et())
    root.mainloop()
