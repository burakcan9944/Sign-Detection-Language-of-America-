import os
import shutil

# Kaynak klasör ve hedef klasör yolları
source_folder = 'C:\\Users\\bccf\\Desktop\\images'
destination_folder = 'C:\\Users\\bccf\\Desktop\\labels'

# Hedef klasör yoksa oluştur
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)

# Kaynak klasördeki dosyaları kontrol et
for file_name in os.listdir(source_folder):
    # Dosya yolu
    file_path = os.path.join(source_folder, file_name)

    # Eğer dosya bir .txt dosyasıysa
    if file_name.endswith('.txt'):
        # Dosyayı hedef klasöre taşı
        shutil.move(file_path, destination_folder)
        print(f'{file_name} taşındı.')

print('Tüm .txt dosyaları taşındı.')
