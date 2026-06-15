import json
import os

# Verilerin kaydedileceği JSON dosyası
DOSYA_ADI = "butce.json"

def veri_yukle():
    """Varsa eski verileri yükler, yoksa boş bir şablon döndürür."""
    if os.path.exists(DOSYA_ADI):
        with open(DOSYA_ADI, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    # İlk defa çalışıyorsa varsayılan yapı
    return {"gelir": 0.0, "kategoriler": [], "harcamalar": []}

def veri_kaydet(veri):
    """Verileri JSON dosyasına düzenli (indent=4) bir şekilde kaydeder."""
    with open(DOSYA_ADI, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, indent=4, ensure_ascii=False)

def main():
    # Program başlarken verileri belleğe al
    bakiye_verisi = veri_yukle()
    
    while True:
        print("\n" + "="*45)
        print("💰 KİŞİSEL BÜTÇE VE YATIRIM TAKİPÇİSİ 💰")
        print("="*45)
        print("1. Gelir Ekle / Güncelle")
        print("2. Yeni Harcama Kategorisi Ekle")
        print("3. Harcama Ekle")
        print("4. 📊 Bütçe Raporunu Gör (Gider & Yatırım)")
        print("5. Çıkış")
        
        secim = input("\nNe yapmak istersin? (1/2/3/4/5): ")
        
        if secim == '1':
            try:
                miktar = float(input("Aylık toplam gelirini gir (TL): "))
                bakiye_verisi["gelir"] = miktar
                veri_kaydet(bakiye_verisi)
                print(f"✅ Gelirin {miktar:.2f} TL olarak güncellendi.")
            except ValueError:
                print("❌ Lütfen geçerli bir sayı girin! (Örn: 5000 veya 5000.50)")
                
        elif secim == '2':
            kategori = input("Eklemek istediğin kategorinin adı (Örn: Market, Kıyafet, Eğitim): ").strip().capitalize()
            if kategori and kategori not in bakiye_verisi["kategoriler"]:
                bakiye_verisi["kategoriler"].append(kategori)
                veri_kaydet(bakiye_verisi)
                print(f"✅ '{kategori}' kategorisi başarıyla eklendi.")
            elif kategori in bakiye_verisi["kategoriler"]:
                print("⚠️ Bu kategori zaten var!")
            else:
                print("❌ Geçersiz kategori adı!")
                
        elif secim == '3':
            if not bakiye_verisi["kategoriler"]:
                print("⚠️ Önce bir kategori eklemelisin! (Menüden 2'yi seç)")
                continue
                
            print("\n--- Mevcut Kategoriler ---")
            for i, kat in enumerate(bakiye_verisi["kategoriler"], 1):
                print(f"{i}. {kat}")
                
            try:
                kat_secim = int(input("\nHangi kategoriye harcama ekleyeceksin? (Numara gir): ")) - 1
                
                if 0 <= kat_secim < len(bakiye_verisi["kategoriler"]):
                    secilen_kategori = bakiye_verisi["kategoriler"][kat_secim]
                    aciklama = input("Ne aldın veya neye ödedin? (Örn: Kahve, Ayakkabı): ")
                    tutar = float(input("Ne kadar ödedin? (TL): "))
                    
                    # Harcamayı listeye sözlük olarak ekliyoruz
                    bakiye_verisi["harcamalar"].append({
                        "kategori": secilen_kategori,
                        "aciklama": aciklama,
                        "tutar": tutar
                    })
                    veri_kaydet(bakiye_verisi)
                    print(f"✅ {tutar:.2f} TL tutarındaki '{aciklama}' eklendi.")
                else:
                    print("❌ Hatalı kategori numarası!")
            except ValueError:
                print("❌ Lütfen geçerli bir sayı girin!")
                
        elif secim == '4':
            # List comprehension ile tüm harcamaların tutarlarını topluyoruz
            toplam_harcama = sum(harcama["tutar"] for harcama in bakiye_verisi["harcamalar"])
            yatirima_kalan = bakiye_verisi["gelir"] - toplam_harcama
            
            print("\n" + "*"*45)
            print("📊 AYLIK BÜTÇE VE YATIRIM ÖZETİ")
            print("*"*45)
            print(f"💵 Toplam Gelir:  {bakiye_verisi['gelir']:.2f} TL")
            print(f"💸 Toplam Gider: -{toplam_harcama:.2f} TL")
            print("-" * 45)
            
            if bakiye_verisi["harcamalar"]:
                print("Kategori Bazlı Harcama Dağılımı:")
                # Kategorilere göre gruplama yapıyoruz
                kategori_toplamlari = {}
                for h in bakiye_verisi["harcamalar"]:
                    kat = h["kategori"]
                    kategori_toplamlari[kat] = kategori_toplamlari.get(kat, 0) + h["tutar"]
                    
                for kat, tutar in kategori_toplamlari.items():
                    print(f"  👉 {kat}: {tutar:.2f} TL")
            
            print("-" * 45)
            if yatirima_kalan > 0:
                print(f"📈 YATIRIMA KALAN: {yatirima_kalan:.2f} TL")
                print("Tebrikler! Bu tutarı hisse senedi, fon veya birikim için kullanabilirsin. 🚀")
            elif yatirima_kalan == 0:
                print("⚖️ YATIRIMA KALAN: 0.00 TL (Gelir ve gider başa baş, dikkatli ol!)")
            else:
                # Eksi bütçeyi pozitif yazdırıp uyarı veriyoruz
                print(f"🚨 DİKKAT! Bütçeyi {abs(yatirima_kalan):.2f} TL aştın. Borçlanıyorsun!")
            print("*"*45)
            
        elif secim == '5':
            print("Finansal özgürlük yolunda başarılar! Çıkış yapıldı. 👋")
            break
            
        else:
            print("❌ Geçersiz seçim. Lütfen 1-5 arası bir rakam girin.")

if __name__ == "__main__":
    main()