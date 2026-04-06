import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Resmi Gazete Takip", page_icon="📰", layout="centered")

st.title("📰 Bloomberg HT - Resmi Gazete Haberleri")
st.write("Bu uygulama, Bloomberg HT RSS akışını anlık olarak tarayarak **'Resmi Gazete'** ile ilgili son dakika haberlerini ve içeriklerini getirir.")

# --- Tarama Butonu ---
# Uygulamanın her sayfa yenilenmesinde baştan çalışmaması için bir butona bağlıyoruz
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
                    
                    # Açılır/Kapanır kutu (Expander) ile şık bir görünüm
                    with st.expander(f"📌 {haber.title} | {tarih}"):
                        st.markdown(f"🔗 **Haberin Orijinal Linki:** [Buraya Tıklayın]({haber.link})")
                        st.divider() # Araya ince bir çizgi çeker
                        
                        # İçerik çekme kısmı
                        try:
                            response = requests.get(haber.link, headers=headers)
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            paragraflar = soup.find_all('p')
                            # Streamlit'te paragraflar arası boşluk bırakmak için "\n\n" kullanıyoruz
                            icerik_metni = "\n\n".join([p.text.strip() for p in paragraflar if len(p.text.strip()) > 30])
                            
                            if icerik_metni:
                                st.write(icerik_metni)
                            else:
                                st.info("Haber içeriği tam çekilemedi, özet aşağıdadır:")
                                st.write(haber.description)
                                
                        except Exception as e:
                            st.error(f"İçerik çekilemedi - Hata: {e}")
                            
        except Exception as e:
            st.error(f"RSS sistemine bağlanırken bir hata oluştu: {e}")
