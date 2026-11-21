# Valorant AI Agent Draft Recommender
> **Sistem Rekomendasi Komposisi Agent Valorant Berbasis Machine Learning (VCT 2023–2026)**

Aplikasi analitik dan sistem rekomendasi pemilihan agent Valorant pro-level berbasis Streamlit dan model Random Forest Classifier. Model dilatih dari 8.192 komposisi match turnamen resmi Valorant Champions Tour (VCT) tahun 2023 hingga 2026.

---

## 📌 Ringkasan Proyek
- **Dataset**: 8.192 pertandingan resmi VCT (2023–2026), diekspansi menjadi 500.000+ skenario draft parsial (1 sampai 4 agent terpilih).
- **Fitur Model (46 Dimensi)**:
  - One-hot encoding Map (11 peta kompetitif).
  - One-hot binary representation agent yang sudah dipilih tim.
  - Role count aggregation (Duelist, Initiator, Controller, Sentinel).
- **Performa Model**:
  - **Top-3 Accuracy**: **85.0%**
  - **Top-1 Accuracy**: **65.3%**
  - **Macro-F1**: **0.261**
- **Bayesian Smoothing**: Digunakan untuk menghitung win rate map dengan Laplace correction pada data jarang (sparse).

---

## ⚙️ Persyaratan Sistem & Instalasi

### 1. Prasyarat
- Python 3.10 atau versi lebih baru (direkomendasikan Python 3.11 / 3.12).
- Pip (Python Package Manager).

### 2. Instalasi Dependensi
Jalankan perintah berikut di terminal:
```bash
pip install -r requirements.txt
```

Isi dari [requirements.txt](file:///c:/Folder_Kuliah/Machine%20Learning/Project_Valorant_Agent/requirements.txt):
- `streamlit`
- `scikit-learn`
- `pandas`
- `numpy`
- `joblib`
- `matplotlib`
- `Pillow`

---

## 🚀 Cara Menjalankan Aplikasi

Jalankan perintah berikut di direktori proyek:
```bash
streamlit run app.py
```
Aplikasi dashboard interaktif akan terbuka di browser Anda (default: `http://localhost:8501`).

---

## 📂 Struktur Direktori Proyek

```text
Project_Valorant_Agent/
├── assets/
│   ├── images/               # Aset gambar agent (format .webp lokal)
│   └── maps/                 # Cuplikan visual map kompetitif
├── hasil/
│   ├── model_final_2023_2026.joblib  # Bobot model Random Forest terlatih
│   ├── meta_feature_2023_2026.joblib # Kamus fitur & mapping
│   ├── vct_wr_map.csv                # Data win rate & jumlah match per agent-map
│   └── df_exp_2023_2026.parquet      # Dataset training hasil ekspansi
├── 02_praproses_fitur.ipynb  # Pipeline ekstraksi fitur 46 dimensi & ekspansi data
├── 03_model.ipynb            # Eksperimen, pelatihan, & evaluasi multi-model
├── app.py                    # Aplikasi frontend Streamlit (Tracker.gg UI style)
├── requirements.txt          # Daftar package python untuk pip
└── README.md                 # Dokumentasi proyek
```
