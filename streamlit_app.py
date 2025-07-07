import streamlit as st
import numpy as np
import pickle
import pandas as pd
import os

# 1. Sayfa ayarları HER ZAMAN ilk Streamlit komutu olmalıdır.
st.set_page_config(page_title="🎗️ Meme Kanseri Tahmini", layout="wide", initial_sidebar_state="expanded")

# Model ve ölçekleyiciyi yüklemek için fonksiyon
@st.cache_resource
def load_model_scaler():
    model_path = 'rf_model_selected.pkl'
    scaler_path = 'scaler_selected.pkl'
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.error(f"Hata: Model veya ölçekleyici dosyaları bulunamadı. Lütfen '{model_path}' ve '{scaler_path}' dosyalarının ana dizinde olduğundan emin olun.")
        return None, None
    try:
        with open(model_path, 'rb') as model_file:
            rf_model = pickle.load(model_file)
        with open(scaler_path, 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)
        return rf_model, scaler
    except Exception as e:
        st.error(f"Model yüklenirken bir hata oluştu: {e}")
        return None, None

# Modeli ve ölçekleyiciyi yükle
rf_model, scaler = load_model_scaler()

# Sekmeleri oluştur
tab1, tab2 = st.tabs(["📊 Tahmin Aracı", "📖 Kullanım Kılavuzu ve Metodoloji"])

# ================= SEKME 1: TAHMİN ARACI =================
with tab1:
    st.header("Tümör Özelliklerini Girerek Tahmin Yapın")
    
    # Kenar çubuğunu girdi almak için kullanalım
    st.sidebar.header("Girdi Değerleri")

    user_inputs = {}
    
    # HELP parametreleri ile zenginleştirilmiş girdiler
    user_inputs["worst area"] = st.sidebar.number_input("Kötü Alan (Worst Area)", min_value=0.0, max_value=5000.0, value=711.2, help="Tümörün en geniş kesitinin alanı ($mm^2$).")
    user_inputs["worst concave points"] = st.sidebar.number_input("Kötü İçbükey Noktalar (Worst Concave Points)", min_value=0.0, max_value=0.5, value=0.1288, format="%.4f", help="Tümör sınırındaki içbükey (girintili) kısımların en ciddileri.")
    user_inputs["mean concave points"] = st.sidebar.number_input("Ortalama İçbükey Noktalar (Mean Concave Points)", min_value=0.0, max_value=0.3, value=0.04781, format="%.5f", help="Tümör sınırındaki içbükey kısımların ortalama ciddiyeti.")
    user_inputs["worst radius"] = st.sidebar.number_input("Kötü Yarıçap (Worst Radius)", min_value=0.0, max_value=50.0, value=15.11, help="Tümörün merkezinden en uzak noktasına olan mesafelerin en büyüğü (mm).")
    user_inputs["mean concavity"] = st.sidebar.number_input("Ortalama İçbükeylik (Mean Concavity)", min_value=0.0, max_value=0.5, value=0.06664, format="%.5f", help="Tümör sınırındaki girintilerin ortalama derinliği.")

    predict_button = st.sidebar.button("🔬 Tahmin Et", type="primary")

    if predict_button:
        if rf_model and scaler:
            input_data = [user_inputs[feature] for feature in user_inputs]
            input_data_np = np.array(input_data).reshape(1, -1)
            input_data_scaled = scaler.transform(input_data_np)
            
            prediction_val = rf_model.predict(input_data_scaled)[0]
            prediction_proba = rf_model.predict_proba(input_data_scaled)[0]
            
            prediction = 'Malignant (Kötü Huylu)' if prediction_val == 0 else 'Benign (İyi Huylu)'
            confidence = prediction_proba[prediction_val] * 100

            st.subheader("📊 Tahmin Sonucu")
            col1, col2 = st.columns(2)
            with col1:
                if prediction == 'Malignant (Kötü Huylu)':
                    st.error(f"**{prediction}**")
                else:
                    st.success(f"**{prediction}**")
            with col2:
                st.metric(label="Güven Skoru", value=f"{confidence:.2f}%")

            st.subheader("📝 Girilen Değerler")
            st.table(pd.DataFrame([user_inputs]))
        else:
            st.error("Model yüklenemediği için tahmin yapılamıyor.")

# ================= SEKME 2: KILAVUZ VE METODOLOJİ =================
with tab2:
    st.header("Model ve Özellikler Hakkında")
    st.markdown("""
    Bu araç, bir meme kitlesinin patoloji görüntülerinden elde edilen sayısal verilere dayanarak, kitlenin **iyi huylu (Benign)** mu yoksa **kötü huylu (Malignant)** mu olduğunu sınıflandırmak için tasarlanmış bir makine öğrenmesi uygulamasıdır.
    """)

    st.subheader("Kullanılan Özelliklerin Açıklamaları")
    st.markdown("""
    - **Radius (Yarıçap):** Tümörün merkezinden çevresindeki noktalara olan mesafelerin ortalamasıdır.
    - **Concavity (İçbükeylik):** Tümör sınırındaki girintilerin (içbükey kısımların) şiddetini ifade eder.
    - **Concave Points (İçbükey Noktalar):** Tümör sınırındaki içbükey kısımların sayısıdır.
    - **Area (Alan):** Tümörün kesit alanıdır.
    
    Modelimiz bu özelliklerin **`mean` (ortalama)**, ve **`worst` (en kötü veya en büyük)** değerlerini kullanır. 'Worst' değeri, tümörün en düzensiz ve muhtemelen en agresif kısmına ait ölçümü temsil ettiği için kritik öneme sahiptir.
    """)

    st.subheader("Görsel Örnek")
    st.markdown("Aşağıda iyi huylu ve kötü huylu tümör dokularının mikroskobik görüntüleri arasındaki farkı görebilirsiniz. Kötü huylu hücreler daha yoğun, düzensiz ve organize olmamış bir yapıya sahiptir.")
    st.image("images/breastcancer.jpg", caption="İyi Huylu (üstte) ve Kötü Huylu (altta) doku örnekleri.")

    st.subheader("Metodoloji")
    st.markdown("""
    - **Model:** `RandomForestClassifier` (Scikit-learn)
    - **Veri Seti:** *Breast Cancer Wisconsin (Diagnostic) Dataset*. Bu veri seti, dijitalleştirilmiş meme kitlesi görüntülerinden elde edilen 30 farklı özelliği içerir.
    - **Performans:** Bu model, en etkili 5 özellik seçilerek eğitilmiştir ve test verileri üzerinde yaklaşık **~%95 doğruluk (Accuracy)** oranına sahiptir.
    """)

    st.subheader("⚠️ Yasal Uyarı")
    st.warning("""
    **Bu araç tıbbi bir teşhis aracı değildir.** Yalnızca eğitim ve araştırma amaçlıdır. 
    Bu uygulamadan elde edilen sonuçlar, profesyonel bir tıbbi görüşün, tanının veya tedavinin yerini **kesinlikle alamaz.** Sağlığınızla ilgili herhangi bir endişeniz varsa lütfen bir tıp doktoruna veya uzman bir sağlık uzmanına danışın.
    """)