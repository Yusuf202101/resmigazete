import streamlit as st
import feedparser

# --- Sayfa Ayarları ---
st.set_page_config(page_title="Resmi Gazete", page_icon="📰")

st.markdown("### 📰 Resmi Gazete Duyuruları")
st.write("") # Biraz boşluk bırakalım

rss_url = "https://www.bloomberght.com/rss"

with st.spinner("Kararlar yükleniyor..."):
    try:
        feed = feedparser.parse(rss_url)
        resmi_gazete_haberleri = []

        # Haberleri filtrele
        for entry in feed.entries:
            title = entry.title.lower()
            description = entry.description.lower() if 'description' in entry else ""
            
            if "resmi gazete" in title or "resmi gazete" in description:
                resmi_gazete_haberleri.append(entry)

        # --- Sonuçları Ekrana Yazdırma ---
        if not resmi_gazete_haberleri:
            st.warning("Şu anki RSS akışında 'Resmi Gazete' ile ilgili bir duyuru bulunamadı.")
        else:
            # Tam olarak attığın görseldeki gibi listeleme
            for haber in resmi_gazete_haberleri:
                # Çift tire ve doğrudan PDF'e giden tıklanabilir Markdown metni
                st.markdown(f"—— [{haber.title}]({haber.link})")
                st.write("") # Satırlar arası hafif esneklik için ufak boşluk
                
    except Exception as e:
        st.error(f"Sisteme bağlanırken bir hata oluştu: {e}")
