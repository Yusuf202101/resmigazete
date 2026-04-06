import streamlit as st
import feedparser
import requests
from bs4 import BeautifulSoup

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Resmi Gazete Takip", page_icon="📰", layout="centered")

st.title("📰 Bloomberg HT - Resmi Gazete Haberleri")
st.write("Bu uygulama, Bloomberg HT RSS akışını tarar. Haberin içerisindeki başlıklara tıklayarak **doğrudan Resmi Gazete PDF'lerine** ulaşabilirsiniz.")

# --- Tarama Butonu ---
if st.button("Haberleri Tara"):
    
    rss_url = "https://www.bloomberght.com/rss"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

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
                    
                    # Ana haber başlığı (Bloomberg'e gider)
                    st.markdown(f"### {i}. [{haber.title}]({haber.link})")
                    
                    with st.expander(f"📅 {tarih} | Kararları ve PDF'leri Gör"):
                        try:
                            response = requests.get(haber.link, headers=headers)
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            paragraflar = soup.find_all('p')
                            
                            # YENİ EKLENEN KISIM: Linkleri kaybetmemek için HTML'i Markdown'a çeviriyoruz
                            for p in paragraflar:
                                for a_tag in p.find_all('a', href=True):
                                    # Eğer link bir web adresi içeriyorsa onu tıklanabilir formata dönüştür
                                    if a_tag['href'].startswith('http'):
                                        markdown_link = f"[{a_tag.text}]({a_tag['href']})"
                                        a_tag.replace_with(markdown_link)
                            
                            # Artık paragrafları birleştirirken linkler (Markdown olarak) korunmuş olacak
                            icerik_metni = "\n\n".join([p.text.strip() for p in paragraflar if len(p.text.strip()) > 30])
                            
                            if icerik_metni:
                                # Linklerin çalışması için st.write yerine st.markdown kullanıyoruz
                                st.markdown(icerik_metni)
                            else:
                                st.info("Haber içeriği tam çekilemedi, özet aşağıdadır:")
                                st.write(haber.description)
                                
                        except Exception as e:
                            st.error(f"İçerik çekilemedi - Hata: {e}")
                            
                    st.divider()
                    
        except Exception as e:
            st.error(f"RSS sistemine bağlanırken bir hata oluştu: {e}")
