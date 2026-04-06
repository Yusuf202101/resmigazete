import streamlit as st
import feedparser

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Resmi Gazete Takip", page_icon="📰", layout="centered")

st.title("📰 Bloomberg HT - Resmi Gazete Haberleri")
st.write("Bu uygulama, Bloomberg HT RSS akışını tarayarak **'Resmi Gazete'** ile ilgili son dakika haberlerini bulur. Haberin detayını veya PDF dosyasını görmek için linklere tıklayabilirsiniz.")

# --- Tarama Butonu ---
if st.button("Haberleri Tara"):
    
    rss_url = "https://www.bloomberght.com/rss"

    with st.spinner("RSS verisi çekiliyor... Lütfen bekleyin."):
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
                
                # Listeyi ekrana basıyoruz
                for i, haber in enumerate(resmi_gazete_haberleri, 1):
                    tarih = haber.published if 'published' in haber else 'Tarih belirtilmemiş'
                    ozet = haber.description if 'description' in haber else "Özet bulunmuyor."
                    
                    # Her haber için görsel bir kutu (Container) oluşturuyoruz
                    with st.container():
                        # Başlığı tıklanabilir bir link haline getiriyoruz
                        st.markdown(f"### {i}. [{haber.title}]({haber.link})")
                        st.caption(f"📅 Yayınlanma Tarihi: {tarih}")
                        
                        # Haberin kısa özetini gösteriyoruz
                        st.write(ozet)
                        
                        # Doğrudan PDF'e veya habere gitmek için şık bir buton ekliyoruz
                        # Bu buton tıklandığında otomatik olarak yeni sekmede açılır
                        st.link_button("📄 Haberin Tamamına / PDF'e Git", haber.link)
                        
                        st.divider() # Haberler arasına çizgi çekiyoruz
                            
        except Exception as e:
            st.error(f"RSS sistemine bağlanırken bir hata oluştu: {e}")
