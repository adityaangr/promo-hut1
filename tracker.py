from flask import Flask, request, jsonify, render_template_string
import os

app = Flask(__name__)

# Halaman utama sederhana
@app.route('/')
def home():
    return render_template_string("""
        <h2>IP Tracker</h2>
        <p>Akses halaman ini dari perangkat target untuk mendapatkan info lokasi IP.</p>
        <p>Contoh: bagikan link ini ke orang lain, lalu buka log Railway untuk melihat request-nya.</p>
        <hr>
        <p>Request IP dan data lain juga bisa dilihat via endpoint /track</p>
    """)

# Endpoint untuk melacak IP dan User-Agent
@app.route('/track', methods=['GET'])
def track():
    # Ambil IP Address
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Ambil User-Agent (info browser / perangkat)
    user_agent = request.headers.get('User-Agent')

    # Log ke terminal Railway (bisa dilihat di Deploy Logs)
    print(f"Request diterima dari IP: {ip_address}")
    print(f"User-Agent: {user_agent}")
    print("===========")

    # Balas ke user (misal, hanya tampilkan IP-nya)
    return jsonify({
        "status": "ok",
        "ip": ip_address,
        "user_agent": user_agent
    })

# Jalankan Flask app di hosting Railway
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
