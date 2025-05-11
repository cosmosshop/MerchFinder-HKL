# Total Battle Otomatik Paralı Asker Takas Botu (Mercenary Exchange Automation Bot)

## Projeye Hoş Geldiniz!

Total Battle oynamayı seviyor musunuz, ancak sürekli tekrarlayan paralı asker takas işlemlerinin zaman alıcılığından ve monotonluğundan sıkıldınız mı? İşte bu proje tam da bu sorunu çözmek için tasarlandı! Total Battle Otomatik Paralı Asker Takas Botu, oyun içi takas süreçlerini sizin için otomatikleştirerek değerli zamanınızı geri kazandırır ve oyun deneyiminizi daha keyifli hale getirir.

Bu bot, gelişmiş görsel tanıma teknolojisini (PyAutoGUI kütüphanesi aracılığıyla) kullanarak oyun arayüzündeki belirli görselleri hassas bir şekilde algılar ve önceden tanımlanmış tıklama eylemlerini gerçekleştirir. Kullanıcı dostu arayüzü ve geniş özelleştirme seçenekleri sayesinde, kendi oyun tarzınıza ve ihtiyaçlarınıza göre botu kolayca ayarlayabilirsiniz.

**Geliştiren:** FATİH / HKL
**Versiyon:** V1.10 (veya projenin en güncel versiyonunu buraya yazın)
**Proje Durumu:** Aktif Geliştirme / Kararlı Sürüm

---

## ⚠️ Yasal Uyarı ve Risk Bilgisi ⚠️

**BU YAZILIMI KULLANMANIN TÜM RİSKİ KULLANICIYA AİTTİR VE TAMAMEN KULLANICININ SORUMLULUĞUNDADIR.**

Bu bot, Total Battle oyununu otomatikleştirmek için tasarlanmış bir araçtır. Çoğu çevrimiçi oyunun Hizmet Şartları (Terms of Service) ve Kullanım Politikaları, otomasyon araçlarının (botlar, makrolar vb.) kullanımını açıkça yasaklar.

**Bu yazılımın kullanılması, oyun hesabınızın askıya alınmasına, kalıcı olarak yasaklanmasına, oyun içi varlıklarınızın kaybedilmesine veya diğer oyun içi cezalara neden olabilir.**

Bu projenin geliştiricisi (FATİH / HKL), bu yazılımın kullanımından kaynaklanabilecek hiçbir hesap yasağı, veri kaybı, oyun içi ceza veya başka bir zarardan sorumlu değildir. Bu bot, sadece eğitim amaçlı ve otomasyon prensiplerini göstermek amacıyla oluşturulmuştur ve kullanıcıların kendi riskleri altında kullanmaları teşvik edilmektedir.

**BU YAZILIMIN KULLANIMI NEDENİYLE OLUŞABİLECEK HİÇBİR DOĞRUDAN VEYA DOLAYLI ZARARDAN VEYA SONUÇTAN GELİŞTİRİCİ SORUMLU TUTULAMAZ.**

**BU YAZILIMI İNDİREREK, KURARAK VEYA KULLANARAK, YUKARIDA BELİRTİLEN TÜM RİSKLERİ KABUL ETTİĞİNİZİ VE TÜM SORUMLULUĞU ÜSTLENDİĞİNİZİ GAYRİ KABİLİ RÜCU BEYAN ETMİŞ OLURSUNUZ.**

---

## Temel Özellikler ve Öne Çıkanlar

* **Akıllı Otomasyon:** Total Battle'daki paralı asker takas işlemlerini, ekranınızdaki görselleri tanıyarak otomatikleştirir. Belirli görselleri algıladığında belirlenen koordinatlara tıklama yapar.
* **Özelleştirilebilir Görsel Tanıma:**
    * **Hassasiyet Ayarı (% Confidence):** Botun görselleri ne kadar kesin bir şekilde tanıması gerektiğini ayarlayarak hata oranını minimize edebilirsiniz.
    * **Tarama Bekleme Süresi:** Her bir görsel arama döngüsü arasındaki süreyi belirleyerek botun hızını ve CPU kullanımını dengeleyebilirsiniz.
* **Gelişmiş Pencere Yönetimi:**
    * **Otomatik Pencere Odaklama:** Tıklama eylemi öncesinde Total Battle penceresini otomatik olarak aktif hale getirerek, botun yanlış pencereye tıklamasını veya arka planda kalmasını engeller.
    * **Ayarlanabilir Pencere Adı:** Total Battle penceresinin başlığını kendi oyun dilinize veya ayarlarınıza göre kolayca yapılandırabilirsiniz.
* **Çok Yönlü Geri Bildirim Sistemi:**
    * **Sesli Bildirimler:** Botun belirli eylemleri (örn: takas başarıyla yapıldı) gerçekleştirdiğinde sizi sesli olarak bilgilendirebilir.
    * **Detaylı Olay Günlüğü:** Uygulama arayüzünde ve harici bir log dosyasında (total_battle_bot.log) botun tüm işlemlerini, başarılarını ve karşılaşılan hataları gerçek zamanlı olarak takip edebilirsiniz.
* **Kullanıcı Dostu Arayüz (GUI):**
    * `Tkinter` ile geliştirilmiş basit ve anlaşılır bir arayüz sayesinde botu kolayca başlatabilir, durdurabilir ve ayarlarını yapılandırabilirsiniz.
    * **Çoklu Dil Desteği:** Türkçe, İngilizce, Fransızca, Almanca, İspanyolca dahil olmak üzere birden fazla dil seçeneği ile global bir kullanıcı deneyimi sunar. `language.py` dosyası sayesinde yeni diller eklemek oldukça kolaydır.
* **Etkin Kontrol Mekanizmaları:**
    * **Global Kısayol Tuşu:** Oyunun içindeyken bile `Alt + F10` (varsayılan) gibi belirlenmiş bir klavye kısayolu ile botu anında başlatabilir veya durdurabilirsiniz.
    * **İstatistik Raporlama:** Anlık olarak toplam tıklama sayısını, bulunamayan görsel sayısını ve son takas zamanını takip ederek botun verimliliğini gözlemleyebilirsiniz.
* **Kalıcı Ayarlar:** Ayarlarınız `config.json` dosyasına kaydedilir, böylece botu her başlattığınızda yeniden yapılandırmak zorunda kalmazsınız. Uygulamadan çıkmadan önce ayarlarınızı kaydetmediğinizde sizi uyarır.

## Kurulum Rehberi

Bu botu çalıştırmak için aşağıdaki adımları izleyin:

1.  **Python Kurulumu:**
    * Bilgisayarınızda Python 3.x (tercihen 3.8 ve üzeri) kurulu olduğundan emin olun.
    * Python'ı resmi web sitesinden indirin: [python.org](https://www.python.org/downloads/)
    * Kurulum sırasında **"Add Python to PATH"** seçeneğini mutlaka işaretleyin. Bu, komut satırından Python komutlarını çalıştırmanıza olanak tanır.

2.  **Gerekli Python Kütüphaneleri:**
    * Komut İstemi'ni (Windows için `CMD` veya `PowerShell`) veya Terminal'i (macOS/Linux için) açın.
    * Aşağıdaki komutu çalıştırarak gerekli kütüphaneleri yükleyin:
        ```bash
        pip install pyautogui pygetwindow playsound pynput
        ```
        * `pyautogui`: Ekran otomasyonu ve görsel tanıma için.
        * `pygetwindow`: Pencere yönetimi (bulma, odaklama) için.
        * `playsound`: Sesli bildirimler için.
        * `pynput`: Klavye kısayolu dinlemesi için.

3.  **Proje Dosyalarını Edinin:**
    * Bu projenin tüm kaynak kodlarını (main.py, language.py, sounds klasörü, final_images klasörü, config.json - eğer varsa silinmeli) bilgisayarınızda belirlediğiniz bir klasöre indirin veya Git kullanarak klonlayın.

    * **`final_images` Klasörü:** Bu klasör, botun oyun içinde tanıyacağı ve tıklayacağı görselleri içermelidir.
        * Bu görsellerin `PNG` veya `JPG` formatında ve net olduğundan emin olun.
        * Görseller, oyun arayüzündeki tıklanabilir alanları **tam olarak** yansıtmalıdır. Ekran görüntüsü alırken sadece tıklanacak alanı seçmeye özen gösterin.
        * Oyun içi arayüzde küçük değişiklikler olduğunda bu görselleri güncellemeniz gerekebilir.
    * **`sounds` Klasörü:** Bu klasörün içinde, botun sesli bildirimler için kullanacağı `eep-02.wav` (veya başka bir `.wav` uzantılı) bir ses dosyası bulunduğundan emin olun. Ayarlar kısmından bu dosyanın yolunu değiştirebilirsiniz.

4.  **Temiz Kurulum (Önerilir):**
    * Botu ilk kez çalıştırıyorsanız veya büyük bir güncelleme yaptıysanız, projenin ana dizinindeki `config.json` dosyasını (eğer varsa) silmeniz önerilir. Bu, botun varsayılan ayarlarla sıfırdan başlamasını ve herhangi bir eski/bozuk yapılandırma sorununu önlemesini sağlar.

## Botun Kullanımı

1.  **Total Battle Oyununu Başlatın:** Botu çalıştırmadan önce Total Battle oyununu bilgisayarınızda açın. Oyun penceresinin görünür ve etkileşime açık olduğundan emin olun.
2.  **Bot Uygulamasını Başlatın:**
    * Proje klasörüne gidin.
    * `main.py` dosyasını Python ile çalıştırın. Bunu, dosya gezgininden çift tıklayarak (Python kurulumunuz doğruysa) veya Komut İstemi/Terminal'de projenin bulunduğu dizine gidip `python main.py` yazarak yapabilirsiniz.
3.  **Ayarları Yapılandırın:**
    * Uygulama arayüzünde bulunan "Ayarlar" butonuna tıklayarak ayarlar penceresini açın.
    * Burada botun çalışma parametrelerini (hassasiyet, tarama süresi, pencere adı vb.) kendi ihtiyaçlarınıza göre ayarlayabilirsiniz.
    * **Dil Seçimi:** Açılır menüden tercih ettiğiniz arayüz dilini (Türkçe, İngilizce, Fransızca, Almanca, İspanyolca) seçebilirsiniz.
    * Ayarları yaptıktan sonra "Ayarları Kaydet" butonuna basarak değişikliklerinizi `config.json` dosyasına kaydedin.
4.  **Botu Başlatın/Durdurun:**
    * Ana arayüzdeki "Botu Başlat" butonuna tıklayarak botun paralı asker takas görevini başlatabilirsiniz.
    * Görevi durdurmak için "Botu Durdur" butonuna tıklayın.
    * Alternatif olarak, oyundayken botu hızlıca başlatmak veya durdurmak için global kısayol tuşu olan `Alt + F10`'u kullanabilirsiniz.
5.  **Olay Günlüğü ve İstatistikleri Takip Edin:**
    * Uygulama penceresinin alt kısmındaki "Olay Günlüğü" alanından botun tüm eylemlerini, uyarılarını ve hata mesajlarını gerçek zamanlı olarak izleyebilirsiniz.
    * "İstatistikler" bölümü, toplam yapılan tıklama sayısını, bulunamayan görsel sayısını ve son takas işleminin ne zaman gerçekleştiğini size anlık olarak gösterir.

## Geliştirme ve Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılarınızı memnuniyetle karşılarız. Eğer projeye katkıda bulunmak isterseniz:

1.  Proje deposunu çatallayın (`Fork`).
2.  Yeni özellikler veya hata düzeltmeleri için yeni bir dal (`branch`) oluşturun.
3.  Yaptığınız değişiklikleri içeren bir "Pull Request" gönderin. Lütfen yaptığınız değişiklikleri açıkça açıklayın ve uygunsa ekran görüntüleri veya test sonuçları ekleyin.
4.  Yeni dil çevirileri veya mevcut dil metinlerinin iyileştirilmesi için de katkıda bulunabilirsiniz.

Kod kalitesini ve sürdürülebilirliği artırmak için yapıcı eleştirilere ve önerilere açığız.

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır. Bu lisans, yazılımı özgürce kullanmanıza, değiştirmenize, dağıtmanıza ve kopyalamanıza olanak tanır. Daha fazla bilgi için `LICENSE` dosyasına bakın.

---
