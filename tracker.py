from flask import Flask, request, render_template_string
import datetime
import json
import os

app = Flask(__name__)

HTML_PAGE = """
<!doctype html>
<html>
<head><title>Bagikan Lokasi</title></head>
<body>
<h3>Mohon izinkan akses lokasi agar bisa dikirim otomatis.</h3>
<script>
navigator.geolocation.getCurrentPosition(pos => {
    fetch("/report", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            lat: pos.coords.latitude,
            lon: pos.coords.longitude,
            acc: pos.coords.accuracy
        })
    });
    document.body.innerHTML = "<h3>✅ Terima kasih, lokasi sudah dikirim!</h3>";
}, err => {
    document.body.innerHTML = "<h3>❌ Akses lokasi ditolak atau gagal.</h3>";
});
</script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/report', methods=['POST'])
def report():
    data = request.json
    ip = request.remote_addr
    ua = request.headers.get('User-Agent')
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = {
        "time": timestamp,
        "ip": ip,
        "lat": data.get("lat"),
        "lon": data.get("lon"),
        "acc": data.get("acc"),
        "ua": ua
    }

    # Simpan ke file JSON
    if not os.path.exists("location_log.json"):
        with open("location_log.json", "w") as f:
            json.dump([], f)

    with open("location_log.json", "r") as f:
        logs = json.load(f)

    logs.append(log_entry)

    with open("location_log.json", "w") as f:
        json.dump(logs, f, indent=4)

    print(f"[{timestamp}] Lokasi diterima dari {ip} ({data})")
    return {"status": "ok"}

@app.route('/logs')
def logs():
    if not os.path.exists("location_log.json"):
        return "Belum ada data lokasi."

    with open("location_log.json") as f:
        logs = json.load(f)

    html = "<h2>📍 Log Lokasi</h2><table border=1 cellpadding=6><tr><th>Waktu</th><th>IP</th><th>Lokasi</th><th>Akurasi (m)</th><th>Perangkat</th></tr>"
    for item in reversed(logs):
        if item["lat"] and item["lon"]:
            link = f"https://www.google.com/maps?q={item['lat']},{item['lon']}"
            lokasi_html = f'<a href="{link}" target="_blank">{item["lat"]:.6f}, {item["lon"]:.6f}</a>'
        else:
            lokasi_html = "-"
        html += f"<tr><td>{item['time']}</td><td>{item['ip']}</td><td>{lokasi_html}</td><td>{item.get('acc','')}</td><td>{item['ua']}</td></tr>"
    html += "</table>"
    return html

if name == '__main__':
    app.run(host="0.0.0.0", port=10000)