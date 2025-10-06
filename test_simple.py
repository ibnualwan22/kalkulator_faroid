import requests
import json


def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_get_heirs():
    """Test get all heirs"""
    print("🔍 Testing get all heirs...")
    response = requests.get("http://localhost:8000/api/v1/heirs/")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total Heirs: {len(data['data'])}")
    print(f"First 3 heirs:")
    for heir in data['data'][:3]:
        print(f"  - {heir['name_id']} ({heir['name_ar']})")
    print()


def test_calculate_simple():
    """Test simple calculation"""
    print("🔍 Testing simple calculation...")
    print("Kasus: Suami, Ibu, 2 Anak Perempuan")
    print("Tirkah: Rp 100.000.000")
    
    payload = {
        "heirs": [
            {"id": 3, "quantity": 1},   # Suami
            {"id": 18, "quantity": 1},  # Ibu
            {"id": 16, "quantity": 2}   # Anak Perempuan
        ],
        "tirkah": 100000000
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/calculation/calculate",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()['data']
        print(f"\n📊 Hasil Perhitungan:")
        print(f"  Ashl Awal : {data['ashlul_masalah_awal']}")
        print(f"  Ashl Akhir: {data['ashlul_masalah_akhir']}")
        print(f"  Status    : {data['status']}")
        print(f"\n💰 Pembagian:")
        for share in data['shares']:
            heir = share['heir']
            print(f"  • {heir['name_id']}: Rp {share['share_amount']:,.0f} ({share['percentage']})")
    else:
        print(f"Error: {response.text}")
    print()


def test_calculate_aul():
    """Test calculation with 'Aul"""
    print("🔍 Testing 'Aul case...")
    print("Kasus: Suami, 2 Saudari Kandung, 2 Saudari Seibu")
    print("Tirkah: Rp 60.000.000")
    
    payload = {
        "heirs": [
            {"id": 3, "quantity": 1},   # Suami
            {"id": 21, "quantity": 2},  # Saudari Kandung
            {"id": 23, "quantity": 2}   # Saudari Seibu
        ],
        "tirkah": 60000000
    }
    
    response = requests.post(
        "http://localhost:8000/api/v1/calculation/calculate",
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()['data']
        print(f"\n📊 Hasil Perhitungan:")
        print(f"  Ashl Awal : {data['ashlul_masalah_awal']}")
        print(f"  Ashl Akhir: {data['ashlul_masalah_akhir']}")
        print(f"  Status    : {data['status']}")
        print(f"  'Aul?     : {data['is_aul']}")
        print(f"\n💰 Pembagian:")
        for share in data['shares']:
            heir = share['heir']
            print(f"  • {heir['name_id']}: Rp {share['share_amount']:,.0f} ({share['percentage']})")
    else:
        print(f"Error: {response.text}")
    print()


if __name__ == "__main__":
    print("="*60)
    print("🧪 TESTING KALKULATOR FAROID API")
    print("="*60)
    print()
    
    try:
        test_health()
        test_get_heirs()
        test_calculate_simple()
        test_calculate_aul()
        
        print("="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server!")
        print("   Make sure the server is running:")
        print("   python run.py")
    except Exception as e:
        print(f"❌ Error: {e}")
