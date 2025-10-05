# Ball-Ballan 

Proyek Django sederhana yang dikembangkan oleh Rexy Adrian Fernando 2406495666 sebagai pemenuhan tugas mata kuliah Pemrograman Berbasis Platform (PBP).

🔗 Link Deployment:https://rexy-adrian-ballballan.pbp.cs.ui.ac.id/

---

# Tugas 2

---

## Proses Pembuatan Proyek Django

### Membuat Direktori dan Mengaktifkan Virtual Environment

1. Membuat folder direktori utama proyek bernama ```ball-ballan```.
2. Memindahkan direktori pada terminal ke direktori utama proyek.
3. Membuat _virtual environment_ Python pada direktori utama dengan command:

    ```bash
    python -m venv env
    ```

4. Menyalakan _virtual environment_ Python dengan command:
    ```bash
    env\Scripts\activate
    ```

### Menyiapkan _Dependencies_ dan Membuat Proyek Django

1. Membuat berkas ```requirements.txt``` dan menambahkan _dependencies_ yang diperlukan.
    isi requirements.txt:
    ```
    django
    gunicorn
    whitenoise
    psycopg2-binary
    requests
    urllib3
    ```

2. Melakukan instalasi terhadap _dependencies_ yang ada dengan perintah berikut:
    ```bash
    pip install -r requirements.txt
    ```
    Pastikan menjalankan virtual environment terlebih dahulu sebelum menjalankan perintah tersebut.

3. Membuat proyek Django bernama ```ball_ballan``` dengan perintah berikut:
    ```bash
    django-admin startproject ball_ballan .
    ```

### Konfigurasi _Environment Variables_ dan Proyek

1. Membuat file ```.env``` di dalam direktori root proyek dan menambahkan konfigurasi berikut:
    ```
    PRODUCTION=False
    ```

2. Membuat file. ```.env.prod``` di direktori yang sama dan menambahkan konfigurasi berikut:
    ```
    DB_NAME=<nama database>
    DB_HOST=<host database>
    DB_PORT=<port database>
    DB_USER=<username database>
    DB_PASSWORD=<password database>
    SCHEMA=tutorial
    PRODUCTION=True
    ```

    > - ```.env``` digunakan untuk development lokal.
    > - ```.env.prod``` digunakan untuk production deployment.

3. Modifikasi file ```settings.py``` untuk menggunakan _environment variables_. Tambahkan kode berikut di bagian atas file:
    ```python
    import os
    from dotenv import load_dotenv
    # Load environment variables from .env file
    load_dotenv()
    ```
4. Menambahkan kedua string berikut pada ```ALLOWED_HOSTS``` di ```settings.py``` untuk keperluan development:
    ```python
    ...
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    ...
    ```

5. Menambahkan konfigurasi ```PRODUCTION``` di atas code ```DEBUG``` di ```settings.py```.
    ```python
    PRODUCTION = os.getenv('PRODUCTION', 'False').lower() == 'true'
    ```

6. Mengubah konfigurasi database pada ```settings.py``` dengan kode berikut:
    ```python
    # Database configuration
    if PRODUCTION:
        # Production: gunakan PostgreSQL dengan kredensial dari environment variables
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv('DB_NAME'),
                'USER': os.getenv('DB_USER'),
                'PASSWORD': os.getenv('DB_PASSWORD'),
                'HOST': os.getenv('DB_HOST'),
                'PORT': os.getenv('DB_PORT'),
                'OPTIONS': {
                    'options': f"-c search_path={os.getenv('SCHEMA', 'public')}"
                }
            }
        }
    else:
        # Development: gunakan SQLite
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    ```

### Membuat Aplikasi ```main```

1. Menjalankan command berikut pada terminal:
    ```bash
    python manage.py startapp main
    ```
2. Menambahkan ```'main'``` ke dalam daftar aplikasi yang ada sebagai elemen paling terakhir pada variabel ```INSTALLED_APPS```, di ```settings```

3. Membuat direktori ```templates``` dan membuat berkas ```main.html``` sebagai template untuk menampilkan data program.

4. Mengisi berkas ```main.html``` dengan html berikut:
    ```html
    <h1>Ball-Ballan</h1>

    <h5>App Name: </h5>
    <p>{{ appname }}</p>
    <h5>NPM: </h5>
    <p>{{ npm }}</p>
    <h5>Name: </h5>
    <p>{{ name }}<p>
    <h5>Class: </h5>
    <p>{{ class }}</p>
    ```
5. Mengubah berkas ```models.py``` dalam aplikasi ```main``` dengan kode berikut:
    ```python
    from django.db import models

    class Product(models.Model):
        CATEGORY_CHOICES = [
            ('jersey', 'Jersey'),
            ('sepatu', 'Sepatu'),
            ('peralatan', 'Peralatan'),
            ('aksesoris', 'Aksesoris'),
            ('jaket', 'Jaket'),
        ]

        name = models.CharField(max_length=40)
        price = models.IntegerField(default=0)
        description = models.TextField()
        thumbnail = models.URLField(blank=True, null=True)
        category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
        is_featured = models.BooleanField(default=False)
        stock = models.PositiveIntegerField(default=0)
        brand = models.CharField(max_length=20)
        
        def __str__(self):
            return self.name
    ```

    > Pada ```models.py``` berisi variabel bertipe field untuk model ```Product``` yang didefinisikan.

6. Mengintegrasikan komponen Model-View-Template (MVT) dengan menambahkan kode berikut pada ```views.py```:
    ```python
    from django.shortcuts import render

    def show_main(request):
        context = {
            'appname' : 'Ball-Ballan',
            'npm' : '2406495666',
            'name': 'Rexy Adrian Fernando',
            'class': 'PBP D'
        }

        return render(request, "main.html", context)
    ```
    Penjelasan kode:
    > Import render dari modul shortcut dan akan digunakan untuk render html
    > Menambahkan fungsi show_main untuk mengatur HTTP request dan return tampilan yang sesuai (pada variabel ```context```)

7. Melakukan routing pada aplikasi ```main``` pada file ```urls.py``` di direktori main:
    ```python
    from django.urls import path
    from main.views import show_main

    app_name = 'main'

    urlpatterns = [
        path('', show_main, name='show_main'),
    ]
    ```

### Menjalankan Server

1. Jalankan migrasi database dengan command:
    ```bash
    python manage.py migrate
    ```
2. Setelah migrasi, jalankan _server_ Django dengan command:
    ```bash
    python manage.py runserver
    ```

3. Buka http://localhost:8000 pada peramban web untuk melihat aplikasi Django yang berhasil dibuat.

4. Tekan ```Ctrl+C``` pada terminal untuk menonaktifkan _server_ kemudian command berikut untuk menonaktifkan _virtual environment_:
    ```bash
    deactivate
    ```
### Unggah Proyek ke Repositori Github

1. Inisiasi git dengan perintah
    ```bash
    git init
    ```

2. Menambahkan berkas ```.gitignore``` untuk mengabaikan berkas yang tidak perlu diunggah di GitHub.

3. Menghubungkan repositori lokal dengan repositori GitHub, lalu melakukan ```add```, ```commit```, dan ```push```.

### Deployment ke PWS (Pacil Web Service)

1. Akses halaman PWS pada https://pbp.cs.ui.ac.id.
2. Login dengan akun SSO UI.
3. Buat project baru di PWS.
4. Konfigurasi _Environment Variables_ sesuai dengan isi ```.env.prod```
5. Pada ```settings.py``` di proyek Django, tambahkan URL deployment PWS pada ALLOWED_HOSTS.
6. Menghubungkan repositori lokal dengan repositori GitHub, lalu melakukan ```add```, ```commit```, dan ```push```.
7. Lakukan ```add```, ```commit```, dan ```push``` ke PWS.

## Bagan Arsitektur Django

![](assets/mvt.png)

---

## Jelaskan peran ```settings.py``` dalam proyek Django!

Peran ```settings.py``` pada proyek Django adalah sebagai pusat kontrol semua konfigurasi pada proyek Django, seperti ```ALLOWED_HOST```, ```INSTALLED_APPS```, ```TEMPLATES```, ```DATABASES```, dan lain-lain, serta mengatur konfigurasi seperti bahasa, zona waktu, dan lain-lain.

## Bagaimana cara kerja migrasi database di Django?

Di Django, migrasi database adalah proses yang menghubungkan perubahan pada model Python dengan struktur yang sebenarnya ada di dalam database. Django menggunakan migrasi agar pengembang tidak perlu menulis perintah SQL secara manual setiap kali ada penyesuaian. prosesnya adalah:

Mengubah ```models.py``` seperti menambah field atau atribut.

Membuat file migrasi pada terminal:
    ```
    python manage.py makemigrations
    ```

Menjalankan migrasi dengan command:
    ```
    python manage.py migrate
    ```

Cek migrasi yang telah dijalankan (opsional)
    ```
    python manage.py showmigrations
    ```

## Menurut Anda, dari semua framework yang ada, mengapa framework Django dijadikan permulaan pembelajaran pengembangan perangkat lunak?

Salah satu alasan Django dijadikan permulaan pembelajaran pengembangan perangkat lunak karena django merupakan framework yang ramah pemula. Salah satunya karena berbasis python, yang merupakan bahasa yang mudah dipahami, bahkan orang non-IT sekalipun. Selain fitur bawaan (auth, admin, ORM, middleware, dll), Django memiliki banyak library untuk memudahkan pengembang yang bisa dipakai untuk menambah fitur pada aplikasi. Dari sisi komunitas, Django memiliki dokumentasi yang sangat lengkap serta materi tutorial yang sangat banyak. Hal ini membuat pembelajaran lebih mudah untuk diikuti, bahkan bagi yang baru masuk ke dunia pemrograman web.

### Apakah ada feedback untuk asisten dosen tutorial 1 yang telah kamu kerjakan sebelumnya?

Jawab:

Menurut saya, asdos pada tutorial 1 sudah cukup membantu.

---

# Tugas 3

---

## Mengapa data delivery diperlukan dalam pengimplementasian sebuah platform?

Data delivery diperlukan agar client (seperti peramban atau aplikasi lainnya) dapat bertukar informasi dengan server dan memproses informasi tersebut.
Tanpa data delivery, aplikasi hanya menyimpan data statis dan tidak dapat menampilkan data yang dinamis.

## XML vs JSON? Kenapa JSON lebih populer?

Menurut saya json lebih baik dari xml karena beberapa alasan:
* Lebih ringkas dan mudah dibaca oleh orang umum maupun developer
* Menjadi standar di API modern (RESTful API), Hampir semua web service, mobile app, dan microservices menggunakan JSON sebagai format default
* Lebih ringan dan ukuran data lebih kecil sehingga transfer data lebih cepat dan efisien
* Kompatibel dan dapat diproses langsung oleh banyak bahasa pemrograman

Karena hal tersebutlah JSON dapat dikatakan lebih populer.

## Fungsi ```is_valid()``` pada Django

Fungsi digunakan untuk memvalidasi data yang dikirim lewat form. Hal ini dibutuhkan untuk mencegah data-data yang tidak valid dari form masuk ke database.

## Mengapa ```csrf_token``` dibutuhkan saat membuat form Django?

* ```csrf_token``` adalah token yang digunakan untuk mencegah serangan Cross-Site Request Forgery (CSRF).
* Jika tidak ada token, penyerang dapat membuat pengguna seolah-oleh meminta request tertentu pada website dan web akan mengeksekusinya. Hal tersebut dapat dimanfaatkan penyerang untuk melakukan aksinya.
* Dengan adanya ```csrf_token```, setiap form punya token unik yang harus cocok dengan yang di server.

## Postman — Data Delivery

1. **Products (XML)**
   <img width="1920" height="1080" alt="Screenshot (38)" src="https://github.com/user-attachments/assets/af5db4fd-8150-4d31-93b9-6afcf1dd51e8" />


2. **Products (JSON)**
   <img width="1920" height="1080" alt="Screenshot (39)" src="https://github.com/user-attachments/assets/0e0ec1b4-04d3-4b13-bb82-88d365566947" />


3. **Product by ID (XML)**
   <img width="1920" height="1080" alt="Screenshot (40)" src="https://github.com/user-attachments/assets/a9ea1177-3b88-4dcd-94ed-6a6f01285068" />


4. **Product by ID (JSON)**
    <img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/25aa51c7-6b87-4da8-970a-1d12e497f59f" />

## Implementasi Tugas 3 secara _step by step_

* Membuat base.html sebagai kerangka atau template dasar untuk views. Membuat base html terdeteksi sebagai template dasar di settings.
* Memodifikasi template main.html agar sesuai template.
* Menambahkan file add_product.html dan product_detail.html sebagai kerangka untuk forms.
* Membuat ```forms.py``` sebagai struktur form untuk mennerima produk baru.
* Membuat fungsi pada views untuk menambahkan produk (add_product), menampilkan detail (show_product), show product xml, show product json, show product xml by id, show product json by id.
* Membuat URL routing untuk semua views.
* Menambahkan fitur delivery data (XML, JSON, JSON by id) dengan serializers di views.py.
* Mengecek hasil di endpoint /xml/, /json/, /xml/<id>/, /json/<id>/.
* Deploy ke Pacil Web Service.

## Feedback asdos

Asdos pada tutorial 2 sudah cukup membantu.

---

# Tugas 4

---

## Django AuthenticationForm

```AuthenticationForm``` di Django adalah form bawaan (built-in) yang digunakan untuk proses login _user_. Autentikasi dilakukan dengan dengan memeriksa username, password, serta status aktif dari user dengan fungsi ```authenticate()```.

### Kelebihan

* Form login terintegrasi dan sudah disediakan (built-in) sehingga tidak perlu membuat form login secara manual.
* Dapat Disesuaikan kebutuhan dengan meng-override method bawaannya.
* Mudah digunakan.

### Kekurangan

* Field default terbatas pada username dan password.
* Hanya memeriksa ```is_active```. Jika ada ketentuan login tambahan (misalnya verifikasi email, akun diblokir, dll), harus override confirm_login_allowed() atau menambah logika sendiri.

## Perbedaan antara autentikasi dan otorisasi dan bagaiamana Django mengimplementasikannya

### Autentikasi
Autentikasi (Authentication) → proses memverifikasi identitas seseorang.
* Contoh: apakah username dan password cocok dengan user yang terdaftar.

#### Implementasi Django

* Ditangani oleh modul django.contrib.auth.

* Fungsi utama:

    ```python
    authenticate(request, username, password) # memverifikasi user.

    login(request, user) # menandai user sebagai “authenticated” di session.

    logout(request) # menghapus status autentikasi dari session.

    ```
* Middleware yang terlibat: ```AuthenticationMiddleware```, untuk menghubungkan request dengan user (request.user).


### Otorisasi
Otorisasi (Authorization) → proses menentukan hak akses dari user setelah _user_ terverifikasi.
* Contoh: menentukan page apa saja yang boleh diakses atau diubah olej _user_.

#### Implementasi Django
* Ditangani lewat permissions dan groups untuk tiap pengguna

* Dekorator untuk view:

    * ```@login_required```, memastikan user sudah login (autentikasi).

    * ```@permission_required('app_label.permission_codename')```, memastikan user punya izin spesifik (otorisasi).


## Kelebihan dan kekurangan session dan cookies dalam konteks menyimpan state di aplikasi web

### Cookies
Data kecil disimpan di browser client dan dikirim bersama setiap request ke server.

#### Kelebihan
* Ringan karena data disimpan di client, serta stateless di server karena tidak perlu menyimpan data user.
* Bisa dipakai lintas request/domain.
* Mudah digunakan karena browser client mendukung cookies secara default.

#### Kekurangan
* Data yang bisa disimpan terbatas (≈4 KB).
* Data tidak dienkripsi sehingga rawan untuk disalahgunakan.
* Tidak cocok untuk data sensitif.

### Session
Session menyimpan data user di server, dengan hanya session ID dikirim ke browser client.

#### Kelebihan
* Bisa menyimpan data besar/kompleks karena disimpan di server langsung.
* Lebih aman karena data penting tidak disimpan di client.
* Developer punya kontrol penuh di server sehingga bisa hapus/ubah session kapan saja tanpa tergantung client.
* Terintegrasi dengan proses autentikasi user.

#### Kekurangan

* Membebani server karena semua data session harus disimpan (di memori, file, atau database).
* Tidak stateless, yang artinya berlawanan dengan prinsip REST (Representational State Transfer) atau server menyimpan state user.
* Ketergantungan pada cookie karena cookie menyimpan session ID.

## Risiko potensial yang harus diwaspadai dari penggunaan _cookies_ dan bagaimana Django menangani hal tersebut

### Risiko potensial penggunaan cookies:
* Pencurian Cookie (Session Hijacking): Jika cookie (misalnya sessionid) dicuri lewat sniffing, penyerang bisa mengambil alih sesi user.

* XSS (Cross-Site Scripting): Jika aplikasi rentan XSS, attacker bisa memasukkan dan mengeksekusi program JavaScript berbahaya untuk mencuri cookie dari browser.

* CSRF (Cross-Site Request Forgery): Penyerang membuat user melakukan request tak diinginkan (misalnya transfer dana) hanya dengan membuat mereka klik link/visit halaman.

* Manipulasi Data Client-Side: Jika developer menyimpan data sensitif langsung di cookie tanpa enkripsi/validasi, user atau oknum bisa mengubah isi cookie.

### Bagaimana django menangani risiko cookie

* HTTPOnly Cookies: Membuat cookie tidak bisa diakses lewat JavaScript → mencegah pencurian via XSS.

* Secure Cookies: Hanya mengirim cookie lewat HTTPS, tidak lewat HTTP.

* SameSite Cookies: Membatasi pengiriman cookie lintas situs → mencegah CSRF.

* CSRF Protection Middleware: Django otomatis memberi token CSRF untuk tiap form POST. Token ini harus cocok dengan yang dikirim user, sehingga request berbahaya bisa ditolak.

* Automatic Session Expiry: Membatasi masa session cookie → meminimalisir risiko penyalahgunaan jangka panjang.

## Implementasi Tugas 4 secara _step by step_

### Implementasi Fungsi Register, Login, dan Logout User
* Membuat fungsi ```register``` dengan memanfaatkan form bawaan Django: ```UserCreationForm()```, dengan request method "POST", kemudian membuat file ```register.html``` sebagai template tampilan untuk user.
* Membuat fungsi ```login_user``` dengan memanfaatkan form bawaan Django: ```AuthenticationForm```, dan fungsi bawaan Django: ```authenticate``` dan ```login```, dengan request method "POST", kemudian membuat file ```login.html``` sebagai template tampilan untuk user.
* Membuat fungsi ```logout_user``` dengan memanfaatkan fungsi bawaan Django: ```logout```, yang akan langsung me-_redirect_ tampilan ke laman login.
* Melakukan routing untuk masing-masing fungsi pada ```urls.py```.
* Merestriksi tampilan dengan dekorator ```@login_required(login_url='/login')``` pada ```views```.
* Menambahkan ```response.set_cookie('last_login', str(datetime.datetime.now()))``` untuk mendaftarkan cookie ```last_login```, di ```response```, dengan timestamp, pada fungsi ```login_user```.
* Menambahkan ```response.delete_cookie('last_login')``` untuk menghapus cookie ```last_login``` dari daftar cookies di ```response```.

### Menghubungkan Model Product dan User
* Menambahkan variabel user pada product
  ```python
      class Product(models.Model):
      user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
      ...
  ```
  * Melakukan migrasi model.
  * Memodifikasi ```login_user``` untuk mengisi field user dengan nilai ```request.user```, yaitu pengguna yang sedang login. Dengan cara ini, setiap objek yang dibuat akan secara otomatis terhubung dengan pengguna yang membuatnya.

## Feedback asdos

Asdos pada tutorial 3 sudah cukup membantu. Saya tidak mengalami kesulitan dalam mengerjakan tutorial 3. Penjelasan yang diberikan asdos sudah cukup jelas dan membantu.

---

# Tugas 5

---

## Urutan Prioritas Pengambilan CSS Selector

* Inline style pada elemen HTML memiliki prioritas tertinggi. ```style="..."```

* ID selector (#id) memiliki prioritas di bawah inline style.

* Class selector, pseudo-class, dan attribute selector (.class, :hover, [type="text"]) memiliki prioritas di bawah ID.

* Element selector dan pseudo-element (p, div, ::before, ::after) memiliki prioritas terendah.

* Aturan dengan !important akan mengabaikan aturan lain meskipun specificity-nya lebih rendah.

## Pentingnya Responsive Design dalam Pengembangan Aplikasi Web

Responsive design adalah pendekatan dalam desain web agar tampilan dapat menyesuaikan berbagai ukuran layar perangkat (desktop, tablet, smartphone). Konsep ini penting karena:

* Memudahkan pengguna mengakses aplikasi dari berbagai perangkat tanpa hambatan.

* Meningkatkan kenyamanan (user experience).

* Mendukung optimasi mesin pencari (SEO).

* Mengurangi kebutuhan dalam membuat versi terpisah untuk perangkat yang berbeda.

### Contoh aplikasi yang sudah memakai resposive design
* Tokopedia
* Shopee
* X
* Instagram


## Margin, Border, Padding

CSS punya 4 lapisan box model: Margin, border, padding, dan content, dengan margin sebagai lapisan terluar dan content sebagai lapisan terdalam.

* Margin adalah jarak terluar elemen untuk memberi spasi antarelemen).

* Border adalah garis tepi yang membungkus elemen.

* Padding adalah jarak antara isi elemen (content) dengan border.

Implementasi:
```css
.box {
  margin: 20px;              /* jarak dari elemen lain */
  border: 2px solid black;   /* garis tepi */
  padding: 15px;             /* ruang di dalam kotak */
}
```

## Flex Box dan Grid Layout

### Flexbox (Flexible Box Layout)
Flexbox digunakan untuk mengatur layout satu dimensi (baris atau kolom). Cocok untuk elemen yang perlu diratakan atau didistribusikan ruangnya, misalnya navbar, tombol sejajar, atau centering.
contoh:
```css
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
```

### Grid Layout
Grid layout digunakan untuk mengatur layout dua dimensi (baris dan kolom). Cocok untuk membuat layout kompleks seperti dashboard atau galeri gambar.
contoh:
```css
.container {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  grid-template-rows: auto auto;
  gap: 10px;
}
```

## Implementasi Tugas 4 secara _step by step_

* Membuat fitur hapus dan edit produk pada ```views.py```, routing pada ```urls.py```, lalu template html pada ```edit_product.html```
* Menggunakan framework tailwind css untuk kustomisasi design.
* Membuat kustomisasi desain pada template HTML yang telah dibuat pada tugas-tugas sebelumnya, serta menambahkan ```card_product.html``` dan ```navbar.html```
* Membuat design untuk tiap template html agar seragam dan responsive antardevice.
* Membuat tampilan jika sudah ada produk dan belum ada produk.
