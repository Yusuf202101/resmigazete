import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Resmi Gazete Takip", page_icon="📰", layout="centered")

st.title("📰 Bloomberg HT - Resmi Gazete Haberleri")
st.write("Bu uygulama, Bloomberg HT RSS akışını anlık olarak tarayarak **'Resmi Gazete'** ile ilgili son dakika haberlerini ve içeriklerini getirir. Başlıklara tıklayarak orijinal PDF'e gidebilirsiniz.")

# --- Tarama Butonu ---
if st.button("Haberleri Tara"):
    
    rss_url = "https://www.bloomberght.com/rss"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Kullanıcıya bekleme animasyonu gösterelim
    with st.spinner("RSS verisi çekiliyor ve taranıyor... Lütfen bekleyin."):
        try:
            feed = feedparser.parse(rss_url)
            st.info(f"📡 Toplam **{len(feed.entries)}** adet güncel haber tarandı.")

            resmi_gazete_haberleri = []

            # Haberleri filtrele
            for entry in feed.entries:
                title = entry.title.lower()
                description = entry.description.lower() if 'description' in entry else ""
                
                if "resmi gazete" in title or "resmi gazete" in description:
                    resmi_gazete_haberleri.append(entry)

            # --- Sonuçları Ekrana Yazdırma ---
            if not resmi_gazete_haberleri:
                st.warning("Şu anki RSS akışında 'Resmi Gazete' ile ilgili bir haber bulunamadı.")
            else:
                st.success(f"🎉 {len(resmi_gazete_haberleri)} Adet Resmi Gazete Haberi Bulundu!")
                
                for i, haber in enumerate(resmi_gazete_haberleri, 1):
                    tarih = haber.published if 'published' in haber else 'Tarih belirtilmemiş'
                    
                    # 1. Başlığı doğrudan PDF'e (habere) giden tıklanabilir link yapıyoruz
                    st.markdown(f"### {i}. [{haber.title}]({haber.link})")
                    
                    # 2. Tasarımı koruyarak metni okumak isteyenler için açılır kutuyu ekliyoruz
                    with st.expander(f"📅 {tarih} | Haberin İçeriğini Oku"):
                        
                        # İçerik çekme kısmı (Orijinal kodundaki gibi)
                        try:
                            response = requests.get(haber.link, headers=headers)
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            paragraflar = soup.find_all('p')
                            icerik_metni = "\n\n".join([p.text.strip() for p in paragraflar if len(p.text.strip()) > 30])
                            
                            if icerik_metni:
                                st.write(icerik_metni)
                            else:
                                st.info("Haber içeriği tam çekilemedi, özet aşağıdadır:")
                                st.write(haber.description)
                                
                        except Exception as e:
                            st.error(f"İçerik çekilemedi - Hata: {e}")
                            
                    st.divider() # Haberler arasına orijinalindeki gibi çizgi çekiyoruz
                    
        except Exception as e:
            st.error(f"RSS sistemine bağlanırken bir hata oluştu: {e}")
