# 🕌 Kalkulator Faroid

API untuk Kalkulator Faraid (Warisan Islam) berdasarkan **Kitab Zahrotul Faridhah**.

## 📚 Fitur

### Perhitungan Normal
- ✅ Furudh Muqaddarah (bagian tetap)
- ✅ Ashobah (sisa)
- ✅ 'Aul (kelebihan)
- ✅ Radd (kekurangan)

### Kasus Khusus
- ✅ **Akdariyyah** (Zawj + Umm + Jadd + Ukht)
- ✅ **Jadd ma'al-Ikhwah** (Kakek bersama saudara)
- ✅ **Al-Musytarakah** (Saudara berserikat)
- ✅ **Gharrawin** (Dua nenek)
- ✅ **Haml** (Janin dalam kandungan)
- ✅ **Khuntsa** (Hermafrodit)
- ✅ **Gharqa/Hadm** (Meninggal bersamaan)

## 🚀 Quick Start

### 1. Clone & Setup

Clone repository
git clone <repo-url>
cd kalkulator_faroid

Create virtual environment
python3 -m venv venv
source venv/bin/activate # Linux/Mac

atau
venv\Scripts\activate # Windows

Install dependencies
pip install -r requirements.txt

### 2. Setup Database

Edit file `.env`:

PostgreSQL
psql -U postgres
CREATE DATABASE faroid_db;
\q

Initialize tables
python -m app.db.init_db


### 3. Run Server


Server akan berjalan di: [**http://localhost:8000**](http://localhost:8000)

## 📖 API Documentation

Buka browser dan akses:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 💡 Contoh Penggunaan

### Perhitungan Normal

curl -X POST "http://localhost:8000/api/v1/calculation/calculate"
-H "Content-Type: application/json"
-d '{
"heirs": [
{"id": 3, "quantity": 1},
{"id": 18, "quantity": 1},
{"id": 16, "quantity": 2}
],
"tirkah": 100000000
}'


### Kasus Haml (Janin)

curl -X POST "http://localhost:8000/api/v1/calculation/calculate/haml"
-H "Content-Type: application/json"
-d '{
"heirs": [
{"id": 4, "quantity": 1},
{"id": 16, "quantity": 1}
],
"tirkah": 200000000
}'


## 📊 ID Ahli Waris

| ID | Nama Indonesia | Nama Arab |
|----|----------------|-----------|
| 1  | Anak Laki-laki | ابن |
| 2  | Ayah | أب |
| 3  | Suami | زوج |
| 4  | Istri | زوجة |
| 6  | Kakek | جد |
| 16 | Anak Perempuan | بنت |
| 18 | Ibu | أم |
| 21 | Saudari Kandung | أخت لأبوين |

[Lihat daftar lengkap di dokumentasi]

## 🏗️ Struktur Project

kalkulator_faroid/
├── app/
│ ├── api/ # API endpoints
│ ├── core/ # Core calculator logic
│ ├── special_cases/ # Kasus-kasus khusus
│ ├── models/ # Database models
│ ├── schemas/ # Pydantic schemas
│ ├── db/ # Database setup
│ └── utils/ # Utilities & constants
├── tests/ # Unit tests
├── .env # Environment variables
├── requirements.txt # Dependencies
└── run.py # Entry point

## 🧪 Testing


## 📝 Referensi

- **Kitab Zahrotul Faridhah**
- QS. An-Nisa ayat 11-12, 176
- Hadits-hadits tentang faraid

## 📄 License

MIT License

## 👨‍💻 Developer

Developed with ❤️ for Islamic inheritance calculation

