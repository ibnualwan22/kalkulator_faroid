#!/usr/bin/env python3
"""
Auto-fix untuk menambahkan __future__ annotations
"""

import os
import glob

def fix_file(filepath):
    """Add __future__ annotations to file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already has it
    if 'from __future__ import annotations' in content:
        return False
    
    # Check if file needs it (has type hints)
    if ('->' in content or 'List[' in content or 'Dict[' in content or 
        'Tuple[' in content or 'Optional[' in content):
        
        # Add at the very beginning
        new_content = 'from __future__ import annotations\n\n' + content
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    return False

def main():
    print("🔧 Adding __future__ annotations to all Python files...")
    print()
    
    count = 0
    for pattern in ['app/**/*.py', 'app/*.py']:
        for filepath in glob.glob(pattern, recursive=True):
            if '__pycache__' in filepath:
                continue
            
            if fix_file(filepath):
                print(f"✅ Fixed: {filepath}")
                count += 1
    
    print()
    print(f"🎉 Fixed {count} files!")
    print()
    print("Now run: python run.py")

if __name__ == "__main__":
    main()
