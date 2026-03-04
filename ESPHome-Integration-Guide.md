# Updated System - ESPHome Breath Sensor Integration

## ✨ What Changed

The Python backend now **directly connects to your ESPHome breath sensor** at `10.16.129.122` using the same method as your breath sensor code.

## 🔄 How It Works

### Before:
```
Backend → HTTP GET → http://10.16.129.122:5000/breath → Get breath rate
```

### Now:
```
Backend → ESPHome API (port 6053) → Real-time breath rate updates
```

**Advantages:**
- ✅ Real-time updates (no polling needed)
- ✅ More efficient
- ✅ Automatic reconnection
- ✅ Same method as your breath sensor code

## 📦 New Dependency

Install the ESPHome API library:

```bash
pip install aioesphomeapi
```

Or install all:
```bash
pip install -r requirements.txt
```

## 🚀 How to Use

### Step 1: Install Dependencies

```bash
pip install Flask flask-cors requests aioesphomeapi
```

### Step 2: Run the Backend

```bash
python app.py
```

**You'll see:**
```
🔄 Starting ESPHome listener for breath sensor at 10.16.129.122
🚀 Starting Cognitive Load API...
✅ Connected to ESPHome breath sensor at 10.16.129.122
[14:23:45] Breath Rate: 16.0
[14:23:48] Breath Rate: 17.0
```

### Step 3: Start Calibration

```bash
curl -X POST http://localhost:8080/api/calibrate/start \
  -H "Content-Type: application/json" \
  -d '{"seeedStudioIp": "10.16.129.122"}'
```

**Note:** The IP parameter is kept for API compatibility but not actually used for HTTP requests. The backend connects directly via ESPHome API.

## 🔧 Configuration

If your breath sensor IP changes, edit `cognitive_load_service.py`:

```python
# ESPHome breath sensor configuration
self.esp_ip = "10.16.129.122"  # ← Change this
self.breath_key = 3149911513   # ← Your breath sensor key
```

## 📊 What You'll See

### Backend Console:
```
✅ Connected to ESPHome breath sensor at 10.16.129.122
[14:25:10] Breath Rate: 16.0
[14:25:13] Breath Rate: 17.0
✓ Sent HR: 75.5 BPM | Response code: 200

🔄 Calibration started for 90 seconds...
Calibration progress: 10s / 90s (HR: 10, BR: 10)
Calibration progress: 20s / 90s (HR: 20, BR: 20)
...
✅ Calibration complete!
Baseline Heart Rate: 72.50
Baseline Breath Rate: 16.20
```

## 🆚 Comparison with HTTP Method

| Method | Connection Type | Updates | Efficiency |
|--------|----------------|---------|------------|
| **ESPHome API** (New) | Persistent connection | Real-time push | ✅ High |
| **HTTP polling** (Old) | Request per sample | Manual fetch | ⚠️ Medium |

## ⚠️ Troubleshooting

### "ESPHome connection error"

**Check:**
1. Breath sensor is running at `10.16.129.122`
2. Port 6053 is accessible
3. Both devices on same network

**Test connection:**
```bash
# Ping the sensor
ping 10.16.129.122
```

### Breath rate stays at 0

**Possible causes:**
1. ESPHome sensor not connected yet (wait a few seconds)
2. Wrong `breath_key` value
3. Sensor not publishing data

**Check:**
- Look for `✅ Connected to ESPHome` message
- You should see `[HH:MM:SS] Breath Rate: X.X` messages

### Connection keeps dropping

**Solution:**
- The backend automatically reconnects
- Check network stability
- Ensure ESPHome device has stable power

## 🎯 Complete Workflow

1. **Start backend:** `python app.py`
2. **Wait for:** `✅ Connected to ESPHome breath sensor`
3. **Start ESP32** heart rate sensor (posts to backend)
4. **Start calibration:** POST to `/api/calibrate/start`
5. **Monitor:** GET `/api/cognitive-load/current`

## 📱 API Still Works the Same

All API endpoints unchanged:
- `POST /api/heartrate` - ESP32 sends heart rate
- `GET /api/heartrate` - Get heart rate
- `GET /api/breathrate` - Get breath rate (now from ESPHome)
- `GET /api/cognitive-load/current` - Get cognitive load
- `POST /api/calibrate/start` - Start calibration
- `GET /api/calibrate/status` - Check status

## ✅ Benefits

1. **Real-time:** Breath rate updates immediately
2. **Efficient:** No polling overhead
3. **Reliable:** Automatic reconnection
4. **Same as your code:** Uses identical ESPHome API method

---

**Ready to use! Just install aioesphomeapi and run!** 🎉
