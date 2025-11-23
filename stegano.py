#!/usr/bin/env python3
"""
Image Steganography Tool
Sembunyikan text panjang di dalam gambar!
"""

from PIL import Image
import os
from colorama import Fore, Style, init
import pyfiglet

# Initialize colorama
init(autoreset=True)

def text_to_binary(text):
    """Convert text ke binary"""
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary):
    """Convert binary ke text"""
    text = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    return text

def encode_image(image_path, secret_text, output_path):
    """
    Sembunyikan text di dalam gambar menggunakan LSB Steganography
    """
    try:
        # Buka gambar
        img = Image.open(image_path)
        
        # Convert ke RGB kalau bukan
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get pixel data
        pixels = list(img.getdata())
        width, height = img.size
        
        # Tambahkan delimiter untuk marking end of message
        secret_text_with_delimiter = secret_text + "<<END>>"
        
        # Convert text ke binary
        binary_secret = text_to_binary(secret_text_with_delimiter)
        
        # Cek apakah gambar cukup besar untuk menyimpan text
        max_bytes = len(pixels) * 3  # 3 channels (RGB)
        required_bytes = len(binary_secret)
        
        if required_bytes > max_bytes:
            print(Fore.RED + f"[!] Error: Gambar terlalu kecil!")
            print(f"[!] Gambar bisa simpan: {max_bytes} bits")
            print(f"[!] Text butuh: {required_bytes} bits")
            print(f"[!] Gunakan gambar lebih besar atau text lebih pendek")
            return False
        
        # Encode binary ke pixels
        new_pixels = []
        binary_index = 0
        
        for pixel in pixels:
            r, g, b = pixel
            
            # Modify LSB of each channel
            if binary_index < len(binary_secret):
                # Modify red channel
                r = (r & 0xFE) | int(binary_secret[binary_index])
                binary_index += 1
            
            if binary_index < len(binary_secret):
                # Modify green channel
                g = (g & 0xFE) | int(binary_secret[binary_index])
                binary_index += 1
            
            if binary_index < len(binary_secret):
                # Modify blue channel
                b = (b & 0xFE) | int(binary_secret[binary_index])
                binary_index += 1
            
            new_pixels.append((r, g, b))
            
            if binary_index >= len(binary_secret):
                # Tambahkan sisa pixels tanpa modifikasi
                new_pixels.extend(pixels[len(new_pixels):])
                break
        
        # Buat gambar baru dengan pixels yang sudah dimodifikasi
        encoded_img = Image.new('RGB', (width, height))
        encoded_img.putdata(new_pixels)
        
        # Simpan gambar (gunakan PNG untuk lossless)
        if not output_path.lower().endswith('.png'):
            output_path += '.png'
        
        encoded_img.save(output_path, 'PNG')
        
        print(Fore.GREEN + f"\n✓ Berhasil encode!")
        print(Fore.CYAN + f"[*] Text length: {len(secret_text)} characters")
        print(Fore.CYAN + f"[*] Binary length: {len(binary_secret)} bits")
        print(Fore.CYAN + f"[*] Output saved: {output_path}")
        print(Fore.YELLOW + "\n[!] PENTING: Kirim sebagai FILE/DOCUMENT, bukan sebagai PHOTO!")
        print(Fore.YELLOW + "[!] Kalau kirim sebagai photo, WhatsApp akan compress dan data hilang!")
        
        return True
        
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return False

def decode_image(image_path):
    """
    Extract hidden text dari gambar
    """
    try:
        # Buka gambar
        img = Image.open(image_path)
        
        # Convert ke RGB kalau bukan
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Get pixel data
        pixels = list(img.getdata())
        
        # Extract LSB dari setiap channel
        binary_data = ''
        
        for pixel in pixels:
            r, g, b = pixel
            
            # Extract LSB
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)
        
        # Convert binary ke text
        extracted_text = binary_to_text(binary_data)
        
        # Cari delimiter
        delimiter = "<<END>>"
        if delimiter in extracted_text:
            secret_message = extracted_text.split(delimiter)[0]
            print(Fore.GREEN + "\n✓ Berhasil decode!")
            print(Fore.CYAN + f"[*] Message length: {len(secret_message)} characters")
            print(Fore.YELLOW + "\n" + "="*60)
            print(Fore.WHITE + secret_message)
            print(Fore.YELLOW + "="*60 + "\n")
            
            # Tanya apakah mau save ke file
            save = input(Fore.GREEN + "[?] Simpan ke file txt? (y/n): " + Style.RESET_ALL).lower()
            if save == 'y':
                output_file = input(Fore.GREEN + "[+] Nama file output (default: extracted.txt): " + Style.RESET_ALL).strip()
                if not output_file:
                    output_file = "extracted.txt"
                if not output_file.endswith('.txt'):
                    output_file += '.txt'
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(secret_message)
                print(Fore.GREEN + f"✓ Saved to {output_file}")
            
            return True
        else:
            print(Fore.RED + "[!] Tidak ada hidden message ditemukan!")
            print(Fore.YELLOW + "[!] Pastikan gambar ini memang berisi hidden message")
            return False
        
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return False

def encode_menu():
    """Menu untuk encode text ke gambar"""
    print(Fore.CYAN + "\n=== ENCODE: Sembunyikan Text di Gambar ===" + Style.RESET_ALL)
    
    # Input gambar
    print(Fore.YELLOW + "\n[!] Gunakan gambar PNG atau JPG")
    print(Fore.YELLOW + "[!] Semakin besar gambar, semakin banyak text yang bisa disimpan")
    image_path = input(Fore.GREEN + "[+] Path ke gambar (contoh: photo.jpg): " + Style.RESET_ALL).strip()
    
    if not os.path.exists(image_path):
        print(Fore.RED + f"[!] File tidak ditemukan: {image_path}")
        return
    
    # Input text (manual atau dari file)
    print(Fore.YELLOW + "\n[?] Dari mana text yang mau disembunyikan?")
    print("[1] Ketik manual")
    print("[2] Baca dari file .txt")
    choice = input(Fore.GREEN + "[+] Pilih (1/2): " + Style.RESET_ALL).strip()
    
    secret_text = ""
    
    if choice == "2":
        text_file = input(Fore.GREEN + "[+] Path ke file txt: " + Style.RESET_ALL).strip()
        if not os.path.exists(text_file):
            print(Fore.RED + f"[!] File tidak ditemukan: {text_file}")
            return
        
        with open(text_file, 'r', encoding='utf-8') as f:
            secret_text = f.read()
        
        print(Fore.CYAN + f"[*] Loaded {len(secret_text)} characters dari file")
    else:
        print(Fore.YELLOW + "\n[!] Ketik text yang mau disembunyikan (Enter 2x untuk selesai):")
        lines = []
        while True:
            line = input()
            if line == "" and len(lines) > 0 and lines[-1] == "":
                break
            lines.append(line)
        secret_text = '\n'.join(lines[:-1])  # Remove last empty line
    
    if not secret_text:
        print(Fore.RED + "[!] Text tidak boleh kosong!")
        return
    
    # Output path
    output_path = input(Fore.GREEN + "[+] Nama file output (default: encoded.png): " + Style.RESET_ALL).strip()
    if not output_path:
        output_path = "encoded.png"
    
    # Encode!
    print(Fore.CYAN + "\n[*] Encoding...")
    encode_image(image_path, secret_text, output_path)

def decode_menu():
    """Menu untuk decode text dari gambar"""
    print(Fore.CYAN + "\n=== DECODE: Extract Hidden Text ===" + Style.RESET_ALL)
    
    # Input gambar
    print(Fore.YELLOW + "\n[!] Gunakan gambar yang sudah di-encode")
    print(Fore.YELLOW + "[!] Pastikan gambar TIDAK di-compress (kirim sebagai document di WA)")
    image_path = input(Fore.GREEN + "[+] Path ke gambar: " + Style.RESET_ALL).strip()
    
    if not os.path.exists(image_path):
        print(Fore.RED + f"[!] File tidak ditemukan: {image_path}")
        return
    
    # Decode!
    print(Fore.CYAN + "\n[*] Decoding...")
    decode_image(image_path)

def calculate_capacity():
    """Hitung kapasitas gambar untuk menyimpan text"""
    print(Fore.CYAN + "\n=== CALCULATE: Cek Kapasitas Gambar ===" + Style.RESET_ALL)
    
    image_path = input(Fore.GREEN + "[+] Path ke gambar: " + Style.RESET_ALL).strip()
    
    if not os.path.exists(image_path):
        print(Fore.RED + f"[!] File tidak ditemukan: {image_path}")
        return
    
    try:
        img = Image.open(image_path)
        width, height = img.size
        total_pixels = width * height
        
        # 3 bits per pixel (RGB), 8 bits per character
        max_chars = (total_pixels * 3) // 8
        max_words = max_chars // 5  # Estimasi average word length
        
        print(Fore.GREEN + f"\n✓ Gambar: {width}x{height} pixels")
        print(Fore.CYAN + f"[*] Total pixels: {total_pixels:,}")
        print(Fore.CYAN + f"[*] Max characters: ~{max_chars:,}")
        print(Fore.CYAN + f"[*] Max words (estimate): ~{max_words:,}")
        print(Fore.CYAN + f"[*] Max pages (250 words/page): ~{max_words//250}")
        
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")

def main_menu():
    """Main menu"""
    # Banner
    banner = pyfiglet.figlet_format("Stegano-Tool")
    print(Fore.CYAN + banner)
    print(Fore.GREEN + Style.BRIGHT + "\t\t\t\tby Nara-666 | Enhanced" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n=== Image Steganography Tool ===" + Style.RESET_ALL)
    print(Fore.WHITE + "Hide text messages inside images!\n")
    
    while True:
        print(Fore.YELLOW + "\nChoose an option:")
        print("[1] Encode - Hide text in image")
        print("[2] Decode - Extract hidden text from image")
        print("[3] Calculate - Check image capacity")
        print("[4] Help")
        print("[0] Exit")
        
        choice = input(Fore.GREEN + Style.BRIGHT + "\n[+] Enter option -> " + Style.RESET_ALL).strip()
        
        if choice == "1":
            encode_menu()
        elif choice == "2":
            decode_menu()
        elif choice == "3":
            calculate_capacity()
        elif choice == "4":
            show_help()
        elif choice == "0":
            print(Fore.CYAN + "\n👋 Goodbye!\n")
            break
        else:
            print(Fore.RED + "[!] Invalid option!")

def show_help():
    """Show help"""
    print(Fore.CYAN + "\n=== HELP ===" + Style.RESET_ALL)
    print(Fore.WHITE + """
🔹 ENCODE (Hide Text):
   1. Pilih gambar (PNG/JPG)
   2. Input text yang mau disembunyikan
   3. Tool akan generate gambar baru dengan hidden message
   4. KIRIM SEBAGAI DOCUMENT/FILE di WhatsApp, BUKAN sebagai Photo!

🔹 DECODE (Extract Text):
   1. Download gambar dari WhatsApp (sebagai document)
   2. Pilih opsi Decode
   3. Text akan ter-extract otomatis

🔹 TIPS:
   - Gunakan gambar besar (1000x1000+) untuk text panjang
   - Selalu kirim sebagai FILE/DOCUMENT, bukan Photo
   - Compression akan merusak hidden message
   - Format PNG lebih aman dari JPG

🔹 TECHNICAL:
   - Menggunakan LSB (Least Significant Bit) Steganography
   - Modifikasi pixel terakhir setiap RGB channel
   - Invisible to human eye
   - Delimiter: <<END>> untuk marking end of message
    """)

# Run
if __name__ == "__main__":
    main_menu()