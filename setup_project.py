"""
Script untuk setup struktur project secara otomatis
"""

import os


def create_directories():
    """Buat semua direktori yang diperlukan"""
    directories = [
        "app",
        "app/api",
        "app/api/v1",
        "app/api/v1/endpoints",
        "app/core",
        "app/db",
        "app/models",
        "app/schemas",
        "app/special_cases",
        "app/utils",
        "tests",
        "alembic",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        
        # Create __init__.py for Python packages
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file) and directory.startswith("app"):
            with open(init_file, "w") as f:
                f.write(f'"""{directory.split("/")[-1]} package"""\n')
    
    print("✅ Directories created successfully!")


def create_empty_files():
    """Buat file-file kosong yang diperlukan"""
    files = [
        ".env",
        ".gitignore",
        "README.md",
        "requirements.txt",
    ]
    
    for file in files:
        if not os.path.exists(file):
            open(file, "a").close()
    
    print("✅ Empty files created successfully!")


if __name__ == "__main__":
    print("🔧 Setting up Kalkulator Faroid project...")
    print()
    
    create_directories()
    create_empty_files()
    
    print()
    print("="*60)
    print("✅ Project setup completed!")
    print("="*60)
    print()
    print("Next steps:")
    print("1. Copy all code files to respective directories")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Setup database: python -m app.db.init_db")
    print("4. Run server: python run.py")
    print("5. Test API: python test_simple.py")
