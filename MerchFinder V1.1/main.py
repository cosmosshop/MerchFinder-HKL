import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
import pyautogui
import time
import os
import logging
from playsound import playsound
import pygetwindow as gw
import json
from pynput import keyboard # Pynput kütüphanesini içe aktar

# Dil metinlerini ayrı dosyadan içe aktar
from language import LANG_TEXTS

# --- Global Ayarlar ve Sabitler ---

# Klasör yolları
GORSEL_KLASORU = "final_images"
SES_DOSYASI = os.path.join("sounds", "eep-02.wav") # "sounds" klasörü ve "eep-02.wav" dosyası olmalı

# Log ayarı
logging.basicConfig(filename="total_battle_bot.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Global Çalışma Bayrağı
calisiyor_bot = False

# Total Battle Pencere Adı
TOTAL_BATTLE_PENCERE_ADI = "Total Battle" # Total Battle penceresinin tam adı

# Bot Ayarları (Varsayılan)
CONFIDENCE_SEVIYESI = 0.8 # Görsel eşleşme hassasiyeti (0.0 - 1.0 arası)
TARAMA_BEKLEME_SURESI = 1.0 # Görsel arama döngüsü arasındaki bekleme süresi (saniye)
PENCERE_ODAKLAMA_ETKIN = False # Varsayılan False oldu
SES_ETKIN = True # Sesli bildirimleri etkinleştir

# Yapılandırma Dosyası
CONFIG_FILE = "config.json"

pencere = tk.Tk() # Pencere objesi burada oluşturuldu

# Varsayılan Dil ve Güncel Dil Değişkeni
CURRENT_LANG = tk.StringVar(value="tr") # Varsayılan dil Türkçe

# Bot İstatistikleri
toplam_tiklama_sayisi = 0
bulunamayan_resim_sayisi = 0
son_takas_zamani = "Yok"
listener = None # Kısayol tuşu dinleyicisi için global değişken

# Kısayol Tuşu Ayarı (şimdilik sabit, ayarlardan değiştirme seçeneği ekleyebiliriz)
BOT_SHORTCUT_KEY = keyboard.Key.f10 # Varsayılan olarak F10 tuşu
BOT_SHORTCUT_MODIFIER = keyboard.Key.alt_l # Varsayılan olarak sol Alt tuşu (sağ Alt için alt_r)


# --- Yapılandırma Dosyası Fonksiyonları ---
def load_settings():
    """Yapılandırma dosyasından ayarları yükler."""
    global CONFIDENCE_SEVIYESI, TARAMA_BEKLEME_SURESI, PENCERE_ODAKLAMA_ETKIN, SES_ETKIN, TOTAL_BATTLE_PENCERE_ADI, GORSEL_KLASORU, SES_DOSYASI, CURRENT_LANG
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                settings = json.load(f)
                CONFIDENCE_SEVIYESI = settings.get("confidence", CONFIDENCE_SEVIYESI)
                TARAMA_BEKLEME_SURESI = settings.get("scan_time", TARAMA_BEKLEME_SURESI)
                PENCERE_ODAKLAMA_ETKIN = settings.get("window_focus", PENCERE_ODAKLAMA_ETKIN)
                SES_ETKIN = settings.get("sound_enabled", SES_ETKIN)
                TOTAL_BATTLE_PENCERE_ADI = settings.get("tb_window_name", TOTAL_BATTLE_PENCERE_ADI)
                GORSEL_KLASORU = settings.get("image_folder", GORSEL_KLASORU)
                SES_DOSYASI = settings.get("sound_file", SES_DOSYASI)
                
                # Dil ayarını yüklerken, LANG_TEXTS'te varsa yükle, yoksa varsayılanı kullan
                loaded_lang = settings.get("language", CURRENT_LANG.get())
                if loaded_lang in LANG_TEXTS:
                    CURRENT_LANG.set(loaded_lang)
                else:
                    CURRENT_LANG.set("tr") # Geçersiz dil yüklenirse varsayılan Türkçe yap
                
                log_yaz("Ayarlar 'config.json' dosyasından yüklendi.", level="info", skip_lang_key=True)
        except json.JSONDecodeError as e:
            log_yaz(f"Yapılandırma dosyası okunurken hata: {e}. Varsayılan ayarlar kullanılıyor.", "error", skip_lang_key=True)
        except Exception as e:
            log_yaz(f"Ayarlar yüklenirken beklenmedik hata: {e}. Varsayılan ayarlar kullanılıyor.", "error", skip_lang_key=True)
    else:
        log_yaz("Yapılandırma dosyası bulunamadı. Varsayılan ayarlar kullanılıyor.", level="info", skip_lang_key=True)


def save_current_settings():
    """Güncel ayarları yapılandırma dosyasına kaydeder."""
    settings = {
        "confidence": CONFIDENCE_SEVIYESI,
        "scan_time": TARAMA_BEKLEME_SURESI,
        "window_focus": PENCERE_ODAKLAMA_ETKIN,
        "sound_enabled": SES_ETKIN,
        "tb_window_name": TOTAL_BATTLE_PENCERE_ADI,
        "image_folder": GORSEL_KLASORU,
        "sound_file": SES_DOSYASI,
        "language": CURRENT_LANG.get()
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        log_yaz("Ayarlar 'config.json' dosyasına kaydedildi.", level="info", skip_lang_key=True)
    except Exception as e:
        log_yaz(f"Ayarlar kaydedilirken hata: {e}", "error", skip_lang_key=True)


# --- Yardımcı Fonksiyonlar ---
def get_total_battle_window():
    """Total Battle penceresini bulur ve döndürür."""
    windows = gw.getWindowsWithTitle(TOTAL_BATTLE_PENCERE_ADI)
    if windows:
        return windows[0]
    return None

def log_yaz(mesaj_key, level="info", *args, skip_lang_key=False):
    """Mesajı log dosyasına ve GUI'deki Text widget'ına yazar."""
    timestamp = time.strftime('%H:%M:%S')
    
    if skip_lang_key:
        mesaj = mesaj_key # Eğer bu true ise, mesaj_key'i doğrudan mesaj olarak kullan
    else:
        # Metni LANG_TEXTS'ten alırken olası KeyError'ı önlemek için .get() kullan
        mesaj = LANG_TEXTS.get(CURRENT_LANG.get(), {}).get(mesaj_key, mesaj_key)
    
    try:
        mesaj = mesaj.format(*args)
    except IndexError:
        # format metodunda beklenen argüman sayısı ile verilen argüman sayısı uyuşmuyorsa
        # doğrudan mesajı kullan (bu durum nadiren yaşanmalı, genellikle anahtar eksikliğidir)
        mesaj = mesaj_key # Orijinal mesaj anahtarını kullan
        logging.warning(f"Format hatası: '{mesaj_key}' mesajı için {len(args)} argüman verildi, ancak beklenenden farklı olabilir.")


    log_text_widget.config(state=tk.NORMAL)

    if level == "error":
        logging.error(mesaj)
        log_text_widget.insert(tk.END, f"{timestamp} - HATA: {mesaj}\n", "error_tag")
    elif level == "warning":
        logging.warning(mesaj)
        log_text_widget.insert(tk.END, f"{timestamp} - UYARI: {mesaj}\n", "warning_tag")
    else: # info
        logging.info(mesaj)
        log_text_widget.insert(tk.END, f"{timestamp} - {mesaj}\n")
    
    log_text_widget.see(tk.END)
    log_text_widget.update_idletasks()
    
    log_text_widget.config(state=tk.DISABLED)

def play_sound(sound_file_path):
    if SES_ETKIN:
        if os.path.exists(sound_file_path):
            try:
                playsound(sound_file_path)
            except Exception as e:
                log_yaz("sound_error", "error", os.path.basename(sound_file_path), e)
        else:
            log_yaz("sound_file_not_found", "warning", sound_file_path)

# GUI Metinlerini Güncelleme Fonksiyonu
def update_gui_texts():
    current_lang_key = CURRENT_LANG.get()
    current_texts = LANG_TEXTS.get(current_lang_key, {}) # Dil bulunamazsa boş sözlük döndür

    pencere.title(current_texts.get("app_title", "Total Battle Bot"))
    control_frame.config(text=current_texts.get("control_panel_title", "Bot Control Panel"))
    log_labelframe.config(text=current_texts.get("log_title", "Event Log"))
    statistik_frame.config(text=current_texts.get("statistics_title", "Statistics")) # İstatistik başlığını güncelle
    
    # Durum etiketi
    if calisiyor_bot:
        durum_etiketi.config(text=current_texts.get("status_running", "Status: Bot Running"))
    else:
        durum_etiketi.config(text=current_texts.get("status_ready", "Status: Ready"))

    baslat_button.config(text=current_texts.get("start_button", "Start Bot"))
    durdur_button.config(text=current_texts.get("stop_button", "Stop Bot"))
    settings_button.config(text=current_texts.get("settings_button", "Settings"))
    
    # Altbilgi
    dev_info_label.config(text=current_texts.get("dev_info", "Developed by: Fatih / HKL | Version V1.10"))

    # İstatistik etiketlerini de güncelle
    update_statistics_labels()


def update_statistics_labels():
    """İstatistik etiketlerini güncelleyen fonksiyon."""
    toplam_tiklama_label.config(text=f"{LANG_TEXTS[CURRENT_LANG.get()].get('total_clicks_label', 'Toplam Tıklama')}: {toplam_tiklama_sayisi}")
    bulunamayan_resim_label.config(text=f"{LANG_TEXTS[CURRENT_LANG.get()].get('not_found_images_label', 'Bulunamayan Resim')}: {bulunamayan_resim_sayisi}")
    son_takas_label.config(text=f"{LANG_TEXTS[CURRENT_LANG.get()].get('last_trade_time_label', 'Son Takas Zamanı')}: {son_takas_zamani}")


# --- Bot Mantığı Fonksiyonu ---
def bot_gorevi():
    global calisiyor_bot
    log_yaz("bot_start_log")
    
    if not os.path.isdir(GORSEL_KLASORU):
        log_yaz("folder_error", "error", GORSEL_KLASORU)
        messagebox.showerror(LANG_TEXTS[CURRENT_LANG.get()]["app_title"], LANG_TEXTS[CURRENT_LANG.get()]["folder_error_popup"].format(GORSEL_KLASORU))
        durdur_bot()
        return

    while calisiyor_bot:
        tb_window = get_total_battle_window()
        
        if not tb_window:
            log_yaz("tb_window_not_found", "warning")
            time.sleep(TARAMA_BEKLEME_SURESI)
            continue
        
        if PENCERE_ODAKLAMA_ETKIN:
            try:
                if not tb_window.isActive:
                    tb_window.activate()
                    time.sleep(0.1)
            except Exception as e:
                log_yaz("window_focus_error", "warning", e)

        current_region = (tb_window.left, tb_window.top, tb_window.width, tb_window.height)
        
        found_image_in_cycle = False
        for dosya in os.listdir(GORSEL_KLASORU):
            if not dosya.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".bmp")):
                continue
            yol = os.path.join(GORSEL_KLASORU, dosya)
            
            try:
                konum = pyautogui.locateCenterOnScreen(yol, confidence=CONFIDENCE_SEVIYESI, region=current_region)
            except Exception as e:
                log_yaz("image_search_error", "error", dosya, e)
                continue

            if konum:
                pyautogui.click(konum)
                log_yaz("image_clicked_log", "info", dosya, konum)
                play_sound(SES_DOSYASI)
                found_image_in_cycle = True
                
                global toplam_tiklama_sayisi, son_takas_zamani
                toplam_tiklama_sayisi += 1
                son_takas_zamani = time.strftime('%H:%M:%S')
                pencere.after(0, update_statistics_labels) # GUI'yi ana thread'de güncelle

                break # Resim bulundu, diğerlerini aramaya gerek yok
        
        if not found_image_in_cycle:
            log_yaz("image_not_found_log")
            global bulunamayan_resim_sayisi
            bulunamayan_resim_sayisi += 1
            pencere.after(0, update_statistics_labels) # GUI'yi ana thread'de güncelle
        
        time.sleep(TARAMA_BEKLEME_SURESI)

# --- Bot Kontrol Fonksiyonları ---
def baslat_bot():
    global calisiyor_bot
    if not calisiyor_bot:
        tb_window = get_total_battle_window()
        if not tb_window:
            messagebox.showwarning(LANG_TEXTS[CURRENT_LANG.get()]["app_title"], LANG_TEXTS[CURRENT_LANG.get()]["warning_popup_tb_window_not_found"])
            
        calisiyor_bot = True
        Thread(target=bot_gorevi, daemon=True).start()
        log_yaz("bot_start_log")
        baslat_button.config(state=tk.DISABLED, style="Red.TButton")
        durdur_button.config(state=tk.NORMAL, style="Green.TButton")
        durum_etiketi.config(text=LANG_TEXTS[CURRENT_LANG.get()]["status_running"], foreground="green")
    else:
        messagebox.showinfo(LANG_TEXTS[CURRENT_LANG.get()]["app_title"], LANG_TEXTS[CURRENT_LANG.get()]["bot_already_running_info"])

def durdur_bot():
    global calisiyor_bot
    if calisiyor_bot:
        calisiyor_bot = False
        log_yaz("bot_stopped_log")
        baslat_button.config(state=tk.NORMAL, style="Green.TButton")
        durdur_button.config(state=tk.DISABLED, style="Red.TButton")
        durum_etiketi.config(text=LANG_TEXTS[CURRENT_LANG.get()]["status_stopped"], foreground="red")
    else:
        messagebox.showinfo(LANG_TEXTS[CURRENT_LANG.get()]["app_title"], LANG_TEXTS[CURRENT_LANG.get()]["bot_already_stopped_info"])

# --- Ayarlar Penceresi Fonksiyonu ---
def configure_settings():
    """Ayarlar penceresini açar."""
    settings_window = tk.Toplevel(pencere)
    settings_window.title(LANG_TEXTS[CURRENT_LANG.get()]["settings_window_title"])
    settings_window.geometry("450x450")
    settings_window.resizable(True, True)
    settings_window.transient(pencere)
    settings_window.grab_set()

    global CONFIDENCE_SEVIYESI, TARAMA_BEKLEME_SURESI, PENCERE_ODAKLAMA_ETKIN, SES_ETKIN, TOTAL_BATTLE_PENCERE_ADI, GORSEL_KLASORU, SES_DOSYASI
    
    # Ayarları tutmak için Tkinter değişkenleri
    confidence_var = tk.DoubleVar(value=CONFIDENCE_SEVIYESI)
    scan_time_var = tk.DoubleVar(value=TARAMA_BEKLEME_SURESI)
    window_focus_var = tk.BooleanVar(value=PENCERE_ODAKLAMA_ETKIN)
    sound_enabled_var = tk.BooleanVar(value=SES_ETKIN)
    total_battle_pencere_adi_var = tk.StringVar(value=TOTAL_BATTLE_PENCERE_ADI)
    gorsel_klasoru_var = tk.StringVar(value=GORSEL_KLASORU)
    ses_dosyasi_var = tk.StringVar(value=SES_DOSYASI)
    
    # Dil seçeneği için Combobox
    language_var_local = tk.StringVar(value=CURRENT_LANG.get())

    # Ayarlar penceresi için değişiklik bayrağı
    settings_changed = False 

    def on_setting_change(*args):
        nonlocal settings_changed
        settings_changed = True

    # Tkinter değişkenlerine izleyici atayarak değişiklikleri algıla
    confidence_var.trace_add("write", on_setting_change)
    scan_time_var.trace_add("write", on_setting_change)
    window_focus_var.trace_add("write", on_setting_change)
    sound_enabled_var.trace_add("write", on_setting_change)
    total_battle_pencere_adi_var.trace_add("write", on_setting_change)
    language_var_local.trace_add("write", on_setting_change)

    # Dosya seçiciler için özel durum
    def choose_image_folder_wrapper():
        nonlocal settings_changed
        old_folder = gorsel_klasoru_var.get()
        choose_image_folder_internal() # Mevcut fonksiyonu çağır
        if old_folder != gorsel_klasoru_var.get():
            settings_changed = True

    def choose_sound_file_wrapper():
        nonlocal settings_changed
        old_file = ses_dosyasi_var.get()
        choose_sound_file_internal() # Mevcut fonksiyonu çağır
        if old_file != ses_dosyasi_var.get():
            settings_changed = True

    settings_frame = ttk.Frame(settings_window, padding=15)
    settings_frame.pack(fill="both", expand=True)

    # --- Dil Seçeneği Ayarı ---
    ttk.Label(settings_frame, text=LANG_TEXTS.get(CURRENT_LANG.get(), {}).get("language_select_label", "Language:")).pack(pady=5, anchor="w")
    language_options = list(LANG_TEXTS.keys())
    language_combobox = ttk.Combobox(settings_frame, textvariable=language_var_local, values=language_options, state="readonly")
    language_combobox.pack(pady=5, padx=20, fill="x")

    # --- Görsel Hassasiyet Ayarı ---
    ttk.Label(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["confidence_label"]).pack(pady=5, anchor="w")
    confidence_slider = ttk.Scale(settings_frame, from_=0.5, to=1.0, orient="horizontal", variable=confidence_var, command=lambda s: confidence_label.config(text=f"{float(s)*100:.0f}%"))
    confidence_slider.pack(pady=5, padx=20, fill="x")
    confidence_label = ttk.Label(settings_frame, text=f"{CONFIDENCE_SEVIYESI*100:.0f}%")
    confidence_label.pack(pady=2, anchor="e")

    # --- Tarama Bekleme Süresi Ayarı ---
    ttk.Label(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["scan_time_label"]).pack(pady=5, anchor="w")
    scan_time_slider = ttk.Scale(settings_frame, from_=0.1, to=10.0, orient="horizontal", variable=scan_time_var, command=lambda s: scan_time_label.config(text=f"{float(s):.1f} sn"))
    scan_time_slider.pack(pady=5, padx=20, fill="x")
    scan_time_label = ttk.Label(settings_frame, text=f"{TARAMA_BEKLEME_SURESI:.1f} sn")
    scan_time_label.pack(pady=2, anchor="e")

    # --- Checkbox Ayarları ---
    ttk.Checkbutton(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["focus_checkbox"], variable=window_focus_var).pack(pady=5, anchor="w")
    ttk.Checkbutton(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["sound_checkbox"], variable=sound_enabled_var).pack(pady=5, anchor="w")

    # --- Total Battle Pencere Adı Ayarı ---
    ttk.Label(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["tb_window_name_label"]).pack(pady=5, anchor="w")
    ttk.Entry(settings_frame, textvariable=total_battle_pencere_adi_var, width=40).pack(pady=5, padx=20, fill="x")

    # --- Görsel Klasörü Seçimi ---
    def choose_image_folder_internal(): # Fonksiyon adı çakışmasını önlemek için değiştirildi
        new_folder = filedialog.askdirectory(title=LANG_TEXTS[CURRENT_LANG.get()]["choose_image_folder_button"], initialdir=GORSEL_KLASORU)
        if new_folder:
            gorsel_klasoru_var.set(new_folder)
            log_yaz("image_folder_updated", "info", new_folder)
        else:
            log_yaz("image_folder_cancelled", "warning")
            
    ttk.Button(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["choose_image_folder_button"], command=choose_image_folder_wrapper).pack(pady=5) # Wrapper kullanıldı
    ttk.Label(settings_frame, textvariable=gorsel_klasoru_var, wraplength=400, font=("Arial", 9)).pack(pady=2, padx=20, fill="x")

    # --- Ses Dosyası Seçimi ---
    def choose_sound_file_internal(): # Fonksiyon adı çakışmasını önlemek için değiştirildi
        new_file = filedialog.askopenfilename(title=LANG_TEXTS[CURRENT_LANG.get()]["choose_sound_file_button"], filetypes=[("WAV dosyaları", "*.wav")], initialdir=os.path.dirname(SES_DOSYASI))
        if new_file:
            ses_dosyasi_var.set(new_file)
            log_yaz("sound_file_updated", "info", new_file)
        else:
            log_yaz("sound_file_cancelled", "warning")

    ttk.Button(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["choose_sound_file_button"], command=choose_sound_file_wrapper).pack(pady=5) # Wrapper kullanıldı
    ttk.Label(settings_frame, textvariable=ses_dosyasi_var, wraplength=400, font=("Arial", 9)).pack(pady=2, padx=20, fill="x")

    # --- Ayarları Kaydet Butonu ---
    def save_settings():
        nonlocal settings_changed # settings_changed'ı değiştirebilmek için nonlocal anahtar kelimesi
        global CONFIDENCE_SEVIYESI, TARAMA_BEKLEME_SURESI, PENCERE_ODAKLAMA_ETKIN, SES_ETKIN, TOTAL_BATTLE_PENCERE_ADI, GORSEL_KLASORU, SES_DOSYASI, CURRENT_LANG
        
        CONFIDENCE_SEVIYESI = confidence_var.get()
        TARAMA_BEKLEME_SURESI = scan_time_var.get()
        PENCERE_ODAKLAMA_ETKIN = window_focus_var.get()
        SES_ETKIN = sound_enabled_var.get()
        TOTAL_BATTLE_PENCERE_ADI = total_battle_pencere_adi_var.get()
        GORSEL_KLASORU = gorsel_klasoru_var.get()
        SES_DOSYASI = ses_dosyasi_var.get()
        
        old_lang = CURRENT_LANG.get()
        CURRENT_LANG.set(language_var_local.get())
        if old_lang != CURRENT_LANG.get():
            update_gui_texts()
            log_yaz("language_updated", "info", CURRENT_LANG.get())

        log_yaz("settings_saved_log")
        log_yaz("setting_confidence", "info", CONFIDENCE_SEVIYESI*100)
        log_yaz("setting_scan_time", "info", TARAMA_BEKLEME_SURESI)
        log_yaz("setting_window_focus", "info", 'Etkin' if PENCERE_ODAKLAMA_ETKIN else 'Devre Dışı')
        log_yaz("setting_sound_enabled", "info", 'Etkin' if SES_ETKIN else 'Devre Dışı')
        log_yaz("setting_tb_window_name", "info", TOTAL_BATTLE_PENCERE_ADI)
        log_yaz("setting_image_folder", "info", GORSEL_KLASORU)
        log_yaz("setting_sound_file", "info", SES_DOSYASI)
        log_yaz("setting_language", "info", CURRENT_LANG.get())
        
        save_current_settings() # Ayarları dosyaya kaydet
        settings_changed = False # Ayarlar kaydedildiği için bayrağı False yap

        settings_window.destroy()

    ttk.Button(settings_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["save_settings_button"], command=save_settings, style="Accent.TButton").pack(pady=15)

    # Ayarlar penceresi için kapanma protokülünü yakala
    def on_settings_closing():
        if settings_changed:
            if messagebox.askokcancel(
                LANG_TEXTS[CURRENT_LANG.get()]["settings_not_saved_title"],
                LANG_TEXTS[CURRENT_LANG.get()]["settings_not_saved_confirm"]
            ):
                settings_window.destroy()
        else:
            settings_window.destroy()

    settings_window.protocol("WM_DELETE_WINDOW", on_settings_closing)
    settings_window.wait_window(settings_window) # Pencere kapanana kadar ana programı bekletir


# --- GUI Kurulumu ---

pencere.geometry("550x650")
pencere.resizable(True, True)
pencere.configure(bg="#F0F0F0")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#F0F0F0", foreground="#333333", font=("Arial", 10))
style.configure("TButton", font=("Arial", 10, "bold"), padding=8, relief="flat")
style.map("TButton", background=[('active', '#cccccc')])

style.configure("Green.TButton", background="#4CAF50", foreground="white")
style.map("Green.TButton", background=[('active', '#45a049')])
style.configure("Red.TButton", background="#F44336", foreground="white")
style.map("Red.TButton", background=[('active', '#da190b')])
style.configure("Blue.TButton", background="#2196F3", foreground="white")
style.map("Blue.TButton", background=[('active', '#1976D2')])
style.configure("Orange.TButton", background="#FF9800", foreground="white")
style.map("Orange.TButton", background=[('active', '#fb8c00')])
style.configure("Accent.TButton", background="#673AB7", foreground="white")
style.map("Accent.TButton", background=[('active', '#5E35B1')])


# Başlık
app_title_label = ttk.Label(pencere, text=LANG_TEXTS[CURRENT_LANG.get()]["app_title"], font=("Arial", 20, "bold"), background="#F0F0F0", foreground="#333333")
app_title_label.pack(pady=20)

# Ana kontrol çerçevesi
control_frame = ttk.LabelFrame(pencere, text=LANG_TEXTS[CURRENT_LANG.get()]["control_panel_title"], padding=20)
control_frame.pack(pady=10, padx=20, fill="x")
control_frame.config(relief="groove", borderwidth=2)

# Durum etiketi
durum_etiketi = ttk.Label(control_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["status_ready"], font=("Arial", 14), foreground="gray", background=style.configure("TLabel")["background"])
durum_etiketi.pack(pady=10)

# İstatistikler Çerçevesi
statistik_frame = ttk.LabelFrame(control_frame, text=LANG_TEXTS[CURRENT_LANG.get()].get("statistics_title", "İstatistikler"), padding=10)
statistik_frame.pack(pady=10, padx=5, fill="x")
statistik_frame.config(relief="flat", borderwidth=1)

toplam_tiklama_label = ttk.Label(statistik_frame, text="Toplam Tıklama: 0")
toplam_tiklama_label.pack(pady=2, anchor="w")

bulunamayan_resim_label = ttk.Label(statistik_frame, text="Bulunamayan Resim: 0")
bulunamayan_resim_label.pack(pady=2, anchor="w")

son_takas_label = ttk.Label(statistik_frame, text="Son Takas Zamanı: Yok")
son_takas_label.pack(pady=2, anchor="w")


# Butonlar
button_frame = ttk.Frame(control_frame)
button_frame.pack(pady=10)

baslat_button = ttk.Button(button_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["start_button"], command=baslat_bot, style="Green.TButton", width=15)
baslat_button.pack(side=tk.LEFT, padx=10)
durdur_button = ttk.Button(button_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["stop_button"], command=durdur_bot, style="Red.TButton", width=15)
durdur_button.pack(side=tk.RIGHT, padx=10)
durdur_button.config(state=tk.DISABLED)

settings_button = ttk.Button(control_frame, text=LANG_TEXTS[CURRENT_LANG.get()]["settings_button"], command=configure_settings, style="Blue.TButton", width=15)
settings_button.pack(pady=15)

# Log alanı
log_labelframe = ttk.LabelFrame(pencere, text=LANG_TEXTS[CURRENT_LANG.get()]["log_title"], padding=10)
log_labelframe.pack(fill="both", expand=True, padx=20, pady=10)
log_labelframe.config(relief="groove", borderwidth=2)

log_text_widget = tk.Text(log_labelframe, height=15, font=("Consolas", 10), bg="white", fg="#333333", selectbackground="#ADD8E6", selectforeground="#333333", wrap="word", state=tk.DISABLED)
log_text_widget.pack(side="left", fill="both", expand=True)

log_text_widget.tag_configure("error_tag", foreground="red", font=("Consolas", 10, "bold"))
log_text_widget.tag_configure("warning_tag", foreground="orange")

log_scrollbar = ttk.Scrollbar(log_labelframe, orient="vertical", command=log_text_widget.yview)
log_scrollbar.pack(side="right", fill="y")
log_text_widget.config(yscrollcommand=log_scrollbar.set)

# Altbilgi
dev_info_label = ttk.Label(pencere, text=LANG_TEXTS[CURRENT_LANG.get()]["dev_info"], font=("Arial", 9), background="#F0F0F0", foreground="gray")
dev_info_label.pack(side="bottom", pady=10)


# Kısayol Tuşu Dinleyicisi Fonksiyonu
def on_press_shortcut(key):
    global calisiyor_bot
    try:
        # Hem Alt tuşuna basılıp basılmadığını hem de ana tuşun basılıp basılmadığını kontrol et
        if (key == BOT_SHORTCUT_KEY) and (keyboard.Controller().alt_l or keyboard.Controller().alt_r):
            if not calisiyor_bot:
                # Bot çalışmıyorsa başlat
                pencere.after(0, baslat_bot) # GUI thread'inde çalıştır
            else:
                # Bot çalışıyorsa durdur
                pencere.after(0, durdur_bot) # GUI thread'inde çalıştır
    except AttributeError:
        # Özel tuşlar (Shift, Ctrl, Alt gibi) basıldığında hata vermesini engelle
        pass

# Listener'ı başlatma fonksiyonu
def start_shortcut_listener():
    global listener
    if listener is None or not listener.running: # Eğer listener yoksa veya çalışmıyorsa başlat
        listener = keyboard.Listener(on_press=on_press_shortcut)
        listener.start()

# Pencere kapanırken yapılacak işlemler (Listener'ı da durduracak)
def on_closing_with_listener():
    global calisiyor_bot, listener
    if messagebox.askokcancel(LANG_TEXTS[CURRENT_LANG.get()]["app_title"], LANG_TEXTS[CURRENT_LANG.get()]["exit_confirm"]):
        calisiyor_bot = False
        if listener is not None and listener.running:
            listener.stop() # Listener'ı durdur
            listener.join() # Listener thread'inin bitmesini bekle (iyi uygulama)
        pencere.destroy()

# Pencere kapanma protokolünü güncelle
pencere.protocol("WM_DELETE_WINDOW", on_closing_with_listener)


# --- Uygulama Başlangıcı ---
load_settings() # Ayarları yükle
update_gui_texts() # GUI metinlerini yüklenen ayarlara göre güncelle (Dil ayarı da yüklenecek)
start_shortcut_listener() # Kısayol tuşu dinleyiciyi başlat

pencere.mainloop()