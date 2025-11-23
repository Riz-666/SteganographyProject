#!/usr/bin/env python3
"""
WhatsApp Simple Spammer
Kirim pesan berulang ke nomor tertentu dengan mudah!
"""

import pyautogui
import time
import webbrowser
from colorama import Fore, Style, init
import pyfiglet

init(autoreset=True)

def format_phone_number(phone):
    """Format nomor telepon ke format internasional"""
    phone = phone.replace("+", "").replace("-", "").replace(" ", "")
    
    # Kalau dimulai dengan 0, ganti jadi 62
    if phone.startswith("0"):
        phone = "62" + phone[1:]
        print(Fore.YELLOW + f"[!] Nomor dikonversi: {phone}" + Style.RESET_ALL)
    
    return phone

def open_whatsapp_chat(phone_number):
    """Buka WhatsApp Web ke nomor tertentu"""
    url = f"https://web.whatsapp.com/send?phone={phone_number}"
    
    print(Fore.CYAN + f"\n[*] Membuka WhatsApp Web..." + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] Target: {phone_number}" + Style.RESET_ALL)
    print(Fore.RED + "[!] Pastikan WhatsApp Web sudah login!" + Style.RESET_ALL)
    
    webbrowser.open(url)
    
    print(Fore.YELLOW + "\n[!] Tunggu loading..." + Style.RESET_ALL)
    for i in range(15, 0, -1):
        print(f"\r{Fore.CYAN}⏳ {i} detik...{Style.RESET_ALL}", end="")
        time.sleep(1)
    print(f"\r{Fore.GREEN}✓ Chat terbuka!{Style.RESET_ALL}     ")

def send_message_fast(message):
    """Kirim 1 pesan dengan metode fast typing"""
    try:
        # Fast typing
        for char in message:
            if char == '\n':
                pyautogui.hotkey('shift', 'enter')
            else:
                pyautogui.write(char, interval=0.001)
        
        time.sleep(0.2)
        
        # Send
        pyautogui.press('enter')
        time.sleep(0.3)
        
        return True
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {e}" + Style.RESET_ALL)
        return False

def spam_messages(message, count, delay=0.5):
    """
    Spam pesan berkali-kali
    message: text yang mau dikirim
    count: berapa kali mau kirim
    delay: jeda antar pesan (detik)
    """
    print(Fore.CYAN + f"\n[*] Akan mengirim {count} pesan..." + Style.RESET_ALL)
    print(Fore.YELLOW + "[!] Pastikan cursor di kolom ketik WhatsApp!" + Style.RESET_ALL)
    print(Fore.RED + "\n[!] Countdown 10 detik untuk posisikan cursor..." + Style.RESET_ALL)
    
    for i in range(10, 0, -1):
        print(f"\r{Fore.RED}⏰ {i}...{Style.RESET_ALL}", end="")
        time.sleep(1)
    
    print(f"\r{Fore.GREEN}🚀 MULAI KIRIM!{Style.RESET_ALL}     \n")
    
    success_count = 0
    
    for i in range(1, count + 1):
        try:
            # Kirim pesan
            if send_message_fast(message):
                success_count += 1
                print(Fore.GREEN + f"✓ [{i}/{count}] Terkirim!" + Style.RESET_ALL)
            else:
                print(Fore.RED + f"✗ [{i}/{count}] Gagal!" + Style.RESET_ALL)
            
            # Delay sebelum pesan berikutnya (kecuali pesan terakhir)
            if i < count:
                time.sleep(delay)
                
        except KeyboardInterrupt:
            print(Fore.YELLOW + f"\n\n[!] Dihentikan oleh user!" + Style.RESET_ALL)
            print(Fore.CYAN + f"[*] Berhasil kirim: {success_count}/{count} pesan" + Style.RESET_ALL)
            return
        except Exception as e:
            print(Fore.RED + f"✗ [{i}/{count}] Error: {e}" + Style.RESET_ALL)
    
    # Summary
    print(Fore.GREEN + Style.BRIGHT + f"\n🎉 SELESAI!" + Style.RESET_ALL)
    print(Fore.CYAN + f"[*] Total terkirim: {success_count}/{count} pesan" + Style.RESET_ALL)
    
    if success_count < count:
        print(Fore.YELLOW + f"[!] Gagal: {count - success_count} pesan" + Style.RESET_ALL)

def main():
    """Main program"""
    # Banner
    banner = pyfiglet.figlet_format("WA Spam Bot")
    print(Fore.CYAN + banner)
    print(Fore.GREEN + Style.BRIGHT + "\t\t   WhatsApp Spammer" + Style.RESET_ALL)
    print(Fore.YELLOW + "\t\t      by Nara-666 😈\n" + Style.RESET_ALL)
    
    print(Fore.RED + "⚠️  PERHATIAN:" + Style.RESET_ALL)
    print(Fore.YELLOW + "   - Gunakan untuk testing ke NOMOR SENDIRI!" + Style.RESET_ALL)
    print(Fore.YELLOW + "   - Jangan spam ke orang lain (bisa di-block/report)" + Style.RESET_ALL)
    print(Fore.YELLOW + "   - Gunakan dengan bijak!\n" + Style.RESET_ALL)
    
    # Input nomor target
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "📱 TARGET NOMOR" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    
    phone = input(Fore.GREEN + "\n[+] Nomor WhatsApp target (Harus: +6281234567890): " + Style.RESET_ALL).strip()
    
    if not phone:
        print(Fore.RED + "[!] Nomor tidak boleh kosong!" + Style.RESET_ALL)
        return
    
    phone = format_phone_number(phone)
    
    # Konfirmasi nomor
    confirm = input(Fore.YELLOW + f"\n[?] Kirim ke {phone}? (y/n): " + Style.RESET_ALL).lower()
    if confirm != 'y':
        print(Fore.RED + "[!] Dibatalkan." + Style.RESET_ALL)
        return
    
    # Input pesan
    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "💬 PESAN" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n[?] Dari mana pesan?" + Style.RESET_ALL)
    print("[1] Ketik manual")
    print("[2] Baca dari file .txt")
    
    source = input(Fore.GREEN + "[+] Pilih (1/2): " + Style.RESET_ALL).strip()
    
    message = ""
    
    if source == "2":
        # Baca dari file
        filename = input(Fore.GREEN + "[+] Nama file: " + Style.RESET_ALL).strip()
        
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                message = f.read()
            
            print(Fore.GREEN + f"✓ Loaded {len(message)} characters" + Style.RESET_ALL)
            
        except FileNotFoundError:
            print(Fore.RED + f"[!] File tidak ditemukan: {filename}" + Style.RESET_ALL)
            return
        except Exception as e:
            print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)
            return
    else:
        # Ketik manual
        print(Fore.YELLOW + "\n[!] Ketik pesan (Enter 2x untuk selesai):" + Style.RESET_ALL)
        lines = []
        empty_count = 0
        
        while True:
            try:
                line = input()
                if line == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                lines.append(line)
            except EOFError:
                break
        
        message = '\n'.join(lines[:-1]) if len(lines) > 1 else '\n'.join(lines)
    
    if not message.strip():
        print(Fore.RED + "[!] Pesan tidak boleh kosong!" + Style.RESET_ALL)
        return
    
    # Preview pesan
    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "📄 PREVIEW PESAN" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.WHITE + message + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.YELLOW + f"[*] Total: {len(message)} characters" + Style.RESET_ALL)
    
    # Jumlah spam
    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "🔢 JUMLAH SPAM" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    
    count_input = input(Fore.GREEN + "\n[+] Berapa kali mau kirim? (default: 1): " + Style.RESET_ALL).strip()
    count = int(count_input) if count_input.isdigit() and int(count_input) > 0 else 1
    
    # Delay setting
    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "⏱️  DELAY ANTAR PESAN" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    
    print(Fore.YELLOW + "\n[?] Berapa detik delay antar pesan?" + Style.RESET_ALL)
    print("[*] 0.3 = Super cepat (spam mode)")
    print("[*] 0.5 = Cepat")
    print("[*] 1.0 = Normal (recommended)")
    print("[*] 2.0 = Lambat (lebih natural)")
    
    delay_input = input(Fore.GREEN + "[+] Delay (detik, default: 0.5): " + Style.RESET_ALL).strip()
    
    try:
        delay = float(delay_input) if delay_input else 0.5
        if delay < 0:
            delay = 0.5
    except ValueError:
        delay = 0.5
    
    # Summary konfirmasi
    print(Fore.CYAN + "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.GREEN + "📋 SUMMARY" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    print(Fore.YELLOW + f"   Target    : {phone}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"   Pesan     : {len(message)} chars" + Style.RESET_ALL)
    print(Fore.YELLOW + f"   Jumlah    : {count}x" + Style.RESET_ALL)
    print(Fore.YELLOW + f"   Delay     : {delay}s" + Style.RESET_ALL)
    print(Fore.YELLOW + f"   Total time: ~{count * delay:.1f}s" + Style.RESET_ALL)
    print(Fore.CYAN + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + Style.RESET_ALL)
    
    # Final confirmation
    final = input(Fore.RED + Style.BRIGHT + "\n[?] MULAI SPAM? (y/n): " + Style.RESET_ALL).lower()
    
    if final != 'y':
        print(Fore.RED + "[!] Dibatalkan." + Style.RESET_ALL)
        return
    
    # Buka WhatsApp chat
    open_whatsapp_chat(phone)
    
    # SPAM!
    spam_messages(message, count, delay)
    
    # Done
    print(Fore.GREEN + Style.BRIGHT + "\n✨ Program selesai!" + Style.RESET_ALL)
    print(Fore.CYAN + "Terima kasih sudah menggunakan WA Spam Bot! 🚀\n" + Style.RESET_ALL)
    print(Fore.CYAN + "- Nara-666! 😈\n" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n[!] Program dihentikan oleh user (Ctrl+C)" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\n[!] Error: {e}" + Style.RESET_ALL)