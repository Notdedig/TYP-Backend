# Python Flask Backend - Quick Start Guide

## 🎯 Super Quick Start (3 Steps!)

### Step 1: Install Python

**Windows:**
- Download: https://www.python.org/downloads/
- During install: ✅ Check "Add Python to PATH"
- Verify: Open CMD → type `python --version`

**Mac:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 2: Install Dependencies

```bash
pip install Flask flask-cors requests
```

### Step 3: Run the Server

**Windows:**
```cmd
python app.py
```

**Mac/Linux:**
```bash
python3 app.py
```

**Or double-click:** `run-server.bat` (Windows) or `run-server.sh` (Mac/Linux)

✅ **Done!** Server running at http://localhost:8080

---

## 📝 File Structure

You only need **3 files**:

```
your-project-folder/
├── app.py                      # Main API (Flask routes)
├── cognitive_load_service.py   # Calculation logic
└── requirements.txt            # Dependencies
```

---

## 🧪 Test It Works

### Test 1: Open in browser
Go to: http://localhost:8080

You should see JSON with API endpoints.

### Test 2: Send heart rate
```bash
curl -X POST http://localhost:8080/api/heartrate -H "Content-Type: application/json" -d "{\"heartRate\": 75.5}"
```

### Test 3: Get heart rate
```bash
curl http://localhost:8080/api/heartrate
```

---

## 🔥 Why Python is Easier Than Java

| Task | Python | Java (Spring Boot) |
|------|--------|-------------------|
| **Install** | 1 installer | Java JDK + Maven |
| **Files needed** | 3 files | 10+ files |
| **Start server** | `python app.py` | `mvn spring-boot:run` |
| **Build time** | Instant | 30+ seconds |
| **Lines of code** | ~200 | ~500 |
| **Memory usage** | 50 MB | 200 MB |

---

## 🌐 Connect ESP32

**Same as Java version!** ESP32 doesn't know the difference.

```cpp
const char* serverUrl = "http://192.168.1.10:8080/api/heartrate";
```

---

## 🦆 DuckDNS Integration

**Exactly the same as Java!**

1. Get domain from duckdns.org
2. Port forward port 8080
3. Update ESP32 to: `http://yourdomain.duckdns.org:8080/api/heartrate`

---

## 🚀 Run 24/7 on Windows

### Option 1: Keep Window Open
Just leave the command prompt window running.

### Option 2: Hide Window (using pythonw)
```cmd
pythonw app.py
```

This runs without showing a window!

### Option 3: Windows Service
1. Download NSSM: https://nssm.cc/download
2. Install service:
```cmd
nssm install CognitiveLoadAPI "C:\Python\python.exe" "C:\path\to\app.py"
nssm start CognitiveLoadAPI
```

---

## 🐧 Run 24/7 on Linux

### Using screen (simple):
```bash
screen -S api
python3 app.py
# Press Ctrl+A then D to detach
# Reattach with: screen -r api
```

### Using systemd (proper):
Create `/etc/systemd/system/cognitive-load.service`:
```ini
[Unit]
Description=Cognitive Load API

[Service]
ExecStart=/usr/bin/python3 /path/to/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable cognitive-load
sudo systemctl start cognitive-load
```

---

## 🔧 Common Issues

### "Python not found"
- Windows: Reinstall Python, check "Add to PATH"
- Type `python` or `python3` or `py`

### "No module named flask"
```bash
pip install Flask flask-cors requests
```

### "Port 8080 already in use"
Edit `app.py`, change the last line:
```python
app.run(host='0.0.0.0', port=8081, debug=True)  # Changed to 8081
```

### Can't access from ESP32
1. Find your PC's IP: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
2. Test: `curl http://YOUR_IP:8080`
3. If fails: Check firewall (allow port 8080)

---

## 📊 All API Endpoints

Same as Java version:

```
POST   /api/heartrate               → Send HR from ESP32
GET    /api/heartrate               → Get HR data
GET    /api/breathrate              → Get BR data
GET    /api/cognitive-load/current  → Get cognitive load
GET    /api/cognitive-load/predicted → Get predicted load
POST   /api/calibrate/start         → Start calibration
GET    /api/calibrate/status        → Check calibration
```

---

## 🎯 Full Workflow

1. **Start Python server:** `python app.py`
2. **Test locally:** `curl http://localhost:8080`
3. **Set up port forwarding** on router (port 8080)
4. **Get DuckDNS domain:** yourdomain.duckdns.org
5. **Update ESP32:** Use DuckDNS URL
6. **Start calibration:** Send POST to `/api/calibrate/start`
7. **Monitor cognitive load:** GET `/api/cognitive-load/current`

---

## 💡 Tips

**Run on startup (Windows):**
1. Create shortcut to `run-server.bat`
2. Press `Win+R` → type `shell:startup` → Enter
3. Put shortcut in the Startup folder

**View logs:**
```bash
python app.py > api.log 2>&1
```

**Production server:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

---

## ✅ Checklist

- [ ] Python installed (`python --version`)
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server running (`python app.py`)
- [ ] Tested locally (http://localhost:8080)
- [ ] Port forwarding configured (if using remotely)
- [ ] DuckDNS set up (if using remotely)
- [ ] ESP32 updated with server URL
- [ ] Calibration tested
- [ ] Cognitive load working

---

**That's it! Python version is ready to use! 🎉**

Much simpler than Java, same functionality!
