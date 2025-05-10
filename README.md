# Kişisel Finans Yönetim Sistemi

Bu proje, kişisel finanslarınızı yönetmenize yardımcı olan bir masaüstü uygulamasıdır. Gelir ve giderlerinizi kategorize edebilir, raporlar oluşturabilir ve finansal durumunuzu takip edebilirsiniz.

## Özellikler

- Kullanıcı kaydı ve girişi
- Gelir ve gider takibi
- Kategori bazlı finansal raporlama
- Tarih aralığına göre filtreleme
- Profil yönetimi ve tema seçenekleri

## Kurulum

1. Python 3.8 veya daha yüksek bir sürümü yükleyin.
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. Uygulamayı başlatın:
   ```bash
   python src/gui.py
   ```

## Kullanım

1. Uygulamayı başlattığınızda, kayıt ol veya giriş yap seçenekleri sunulacaktır.
2. Ana menüden gelir veya gider ekleyebilir, raporlar görüntüleyebilirsiniz.
3. Profil ayarlarından kişisel bilgilerinizi güncelleyebilir ve tema seçebilirsiniz.

## Proje Yapısı

Proje aşağıdaki ana bileşenlerden oluşmaktadır:

- `gui.py`: Kullanıcı arayüzü ve ana uygulama mantığı
- `database.py`: Veritabanı işlemleri
- `user.py`: Kullanıcı yönetimi
- `income.py`: Gelir yönetimi
- `expense.py`: Gider yönetimi

## Veritabanı

Uygulama SQLite veritabanı kullanmaktadır. Veritabanı dosyası (`finance.db`) otomatik olarak oluşturulacaktır.

## Geliştirme Durumu

- ✅ Kullanıcı Yönetimi
- ✅ Gelir Yönetimi
- ✅ Gider Yönetimi
- ✅ Temel Raporlama