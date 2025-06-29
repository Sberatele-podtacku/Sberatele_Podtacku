import os
from rembg import remove
from PIL import Image

source_folder = r'C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\new_coaster'
destination_folder = r'C:\Users\ASUS GAMING\Documents\GitHub\Sberatele_Podtacku\recenter_nobg'
os.makedirs(destination_folder, exist_ok=True)

# Get list of JPG files
files = [f for f in os.listdir(source_folder) if f.lower().endswith('.jpg')]
total = len(files)

# Loop with progress
for index, filename in enumerate(files, start=1):
    input_path = os.path.join(source_folder, filename)
    output_path = os.path.join(destination_folder, os.path.splitext(filename)[0] + '.png')
    
    try:
        with open(input_path, 'rb') as i:
            with open(output_path, 'wb') as o:
                o.write(remove(i.read()))
        percent = (index / total) * 100
        print(f"✅ {index}/{total} - {filename} ({percent:.1f}%)")
    except Exception as e:
        print(f"❌ Error with {filename}: {e}")

print("🎉 Background removal complete.")
