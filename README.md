# 🎗️ Meme Kanseri Tahmin Uygulaması (Streamlit)

Makine öğrenmesi ile geliştirilmiş, bir tümörün özelliklerine dayanarak **iyi huylu (Benign)** veya **kötü huylu (Malignant)** olduğunu tahmin eden interaktif bir web uygulaması.

<p align="center">
  <img src="images/breastcancer.jpg" width="700" />
</p>

## 📋 Genel Bakış

[cite_start]Bu proje, Wisconsin Meme Kanseri veri setiyle eğitilmiş, yüksek performanslı bir Random Forest modelini kullanır. [cite: 1] Geliştirilen interaktif Streamlit arayüzü sayesinde, araştırmacılar ve öğrenciler, 5 temel tümör özelliğini girerek anında tahmin ve güven skoru alabilirler.

## 🛠️ Teknolojiler

| Teknoloji      | Amaç                  |
|----------------|-----------------------|
| Streamlit 🎈   | İnteraktif Web Arayüzü |
| Scikit-learn 🧠| Makine Öğrenmesi Modeli|
| Pandas 🐼     | Veri Yönetimi         |
| Python 🐍     | Backend               |

## ✨ Uygulama Özellikleri

- **📊 İnteraktif Arayüz:** Kenar çubuğundan değerleri girerek anında tahmin alın.
- **📖 Dahili Kılavuz:** Kullanılan özelliklerin ve modelin metodolojisinin açıklandığı bir sekme.
- [cite_start]**📈 Yüksek Doğruluk:** %95 civarında test doğruluğuna sahip, 5 özellikli optimize edilmiş Random Forest modeli. [cite: 1]
- **⚠️ Yasal Uyarı:** Uygulamanın tıbbi teşhis amaçlı olmadığını belirten net bir uyarı.

## 🚀 Uygulamayı Yerel Ortamda Çalıştırma

1.  **Depoyu Klonlayın:**
    ```bash
    git clone [https://github.com/BlackRazor34/Breast_Cancer_RandomForestML.git](https://github.com/BlackRazor34/Breast_Cancer_RandomForestML.git)
    cd Breast_Cancer_RandomForestML
    ```

2.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Streamlit Uygulamasını Başlatın:**
    ```bash
    streamlit run streamlit_app.py
    ```
    Uygulama tarayıcınızda `http://localhost:8501` adresinde otomatik olarak açılacaktır.

---

## 📊 Model Performansı ve Detaylar

[cite_start]Modelimiz, UCI Breast Cancer Wisconsin veri seti kullanılarak eğitilmiş ve test setinde mükemmel bir performans göstermiştir. [cite: 1]

<p align="center"><img src="images/random.png" width="600" /></p>


### Sonuçlar

| Metrik | Skor |
|--------|-------|
| **Accuracy** | 96.49% |
| **Precision (Weighted Avg)** | 95.89% |
| **Recall (Weighted Avg)** | 96.49% |
| **F1-Score (Weighted Avg)** | 96.05% |
| **AUC-ROC** | 0.981 |

[cite_start]*(Bu metrikler, orijinal modelin 30 özelliğin tamamı kullanılarak eğitilmiş haline aittir.)* [cite: 1]

### Özellik Önem Düzeyleri
[cite_start]Modelin tahmin yaparken en çok dikkate aldığı 5 özellik aşağıda gösterilmiştir. [cite: 1] İnteraktif uygulama, bu en önemli özellikler kullanılarak eğitilmiş bir alt model kullanmaktadır.

<p align="center"><img src="images/Özellik_Önem.png" width="600" /></p>

1.  [cite_start]Worst perimeter (0.211) [cite: 1]
2.  [cite_start]Mean concavity (0.189) [cite: 1]
3.  [cite_start]Worst radius (0.162) [cite: 1]
4.  [cite_start]Mean radius (0.143) [cite: 1]
5.  [cite_start]Worst area (0.128) [cite: 1]

### Hata Matrisi (Confusion Matrix)
<p align="center"><img src="images/confmatrix.png" width="300" /></p>

- [cite_start]**Doğru Pozitif (TP):** 40 (Kötü huylu olarak doğru tahmin edilen) [cite: 1]
- [cite_start]**Yanlış Negatif (FN):** 3 (Kötü huylu iken iyi huylu olarak tahmin edilen) [cite: 1]
- [cite_start]**Yanlış Pozitif (FP):** 1 (İyi huylu iken kötü huylu olarak tahmin edilen) [cite: 1]
- [cite_start]**Doğru Negatif (TN):** 70 (İyi huylu olarak doğru tahmin edilen) [cite: 1]

---

## 🔮 Gelecek Çalışmalar

- [cite_start]Farklı algoritmalarla (SVM, XGBoost, Sinir Ağları) denemeler yapmak. [cite: 1]
- [cite_start]Gelişmiş özellik mühendisliği teknikleri uygulamak. [cite: 1]
- [cite_start]Modelin yeniden eğitimi için otomatik bir pipeline oluşturmak. [cite: 1]

## 📜 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.