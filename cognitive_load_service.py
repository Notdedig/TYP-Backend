"""
Cognitive Load Service
Handles calibration and cognitive load calculations
"""

import time
import requests
import asyncio
import threading
from threading import Lock
from aioesphomeapi import APIClient


class CognitiveLoadService:
    # Constants for cognitive load calculation
    WEIGHT_HR = 0.6
    WEIGHT_BR = 0.4
    MAX_DELTA_FOR_PAAS_9 = 0.40  # 40% increase maps to Paas 9
    CALIBRATION_DURATION_SECONDS = 90
    CALIBRATION_SAMPLING_INTERVAL = 1  # Sample every second
    
    def __init__(self):
        # Baseline values
        self.baseline_heart_rate = 0.0
        self.baseline_breath_rate = 0.0
        
        # Current values
        self.current_heart_rate = 0.0
        self.current_breath_rate = 0.0
        
        # Calibration state
        self._is_calibrated = False
        self._is_calibrating = False
        self.calibration_start_time = 0
        self.seeed_studio_ip = ""
        
        # Data storage during calibration
        self.calibration_heart_rates = []
        self.calibration_breath_rates = []
        
        # Thread safety
        self.lock = Lock()
        
        # ESPHome breath sensor configuration
        self.esp_ip = "10.16.129.122"
        self.breath_key = 3149911513
        self.latest_breath = 0.0
        self.esphome_connected = False
        
        # ESP32 heart-rate HTTP server to poll (default provided by user)
        self.heart_sensor_ip = "10.16.129.173"
        self.heart_sensor_port = 80
        self.heart_poll_interval = 1.0  # seconds
        
        # Start ESPHome listener and heart-rate poller in background
        self._start_esphome_listener()
        self._start_esp32_poller()
    
    def _start_esphome_listener(self):
        """Start ESPHome listener in background thread"""
        def run_listener():
            asyncio.run(self._esphome_listener())
        
        thread = threading.Thread(target=run_listener, daemon=True)
        thread.start()
        print(f"[*] Starting ESPHome listener for breath sensor at {self.esp_ip}")
    
    async def _esphome_listener(self):
        """Listen to ESPHome device for breath rate updates"""
        try:
            client = APIClient(self.esp_ip, 6053, None)
            await client.connect(login=True)
            self.esphome_connected = True
            print(f"[OK] Connected to ESPHome breath sensor at {self.esp_ip}")
            
            def on_state(state):
                if hasattr(state, "key") and state.key == self.breath_key:
                    with self.lock:
                        self.latest_breath = float(state.state)
                        self.current_breath_rate = self.latest_breath

                    # only log when not calibrating (calibration output should be quiet)
                    if not self._is_calibrating:
                        readable_time = time.strftime("%H:%M:%S")
                        print(f"[{readable_time}] Breath Rate: {self.latest_breath}")
            
            client.subscribe_states(on_state)
            
            # Keep connection alive
            while True:
                await asyncio.sleep(1)
                
        except Exception as e:
            self.esphome_connected = False
            print(f"[ERROR] ESPHome connection error: {e}")
            print("[WARN] Breath rate will not update until connection is restored")
    
    def add_heart_rate_reading(self, heart_rate):
        """Add a heart rate reading

        During calibration we skip zero values so the baseline isn't pulled down by
        missing/invalid measurements. We still update ``current_heart_rate`` for
        overall tracking.
        """
        with self.lock:
            self.current_heart_rate = heart_rate

            if self._is_calibrating:
                # ignore zeros while calibrating
                if heart_rate and heart_rate > 0:
                    self.calibration_heart_rates.append(heart_rate)
    
    def add_breath_rate_reading(self, breath_rate):
        """Add a breath rate reading

        During calibration we skip zero values so the baseline isn't pulled down by
        missing/invalid measurements. We still update ``current_breath_rate`` for
        overall tracking.
        """
        with self.lock:
            self.current_breath_rate = breath_rate

            if self._is_calibrating:
                # ignore zeros while calibrating
                if breath_rate and breath_rate > 0:
                    self.calibration_breath_rates.append(breath_rate)
                    
            # Log the breath rate reading
            if not self._is_calibrating:
                readable_time = time.strftime("%H:%M:%S")
                print(f"[{readable_time}] Breath Rate: {breath_rate}")
    
    def get_breath_rate_from_esphome(self):
        """Get current breath rate from ESPHome listener"""
        with self.lock:
            return self.latest_breath

    def _start_esp32_poller(self):
        """Start a background thread to poll the ESP32 /bpm endpoint for heart rate readings"""
        def run_poller():
            try:
                self._esp32_poller()
            except Exception as e:
                print(f"[ERROR] ESP32 poller terminated: {e}")

        thread = threading.Thread(target=run_poller, daemon=True)
        thread.start()
        print(f"[*] Starting ESP32 poller for heart sensor at {self.heart_sensor_ip}:{self.heart_sensor_port}")

    def _esp32_poller(self):
        """Continuously poll the ESP32 HTTP server for a BPM value and add it as a heart rate reading."""
        url = f"http://{self.heart_sensor_ip}:{self.heart_sensor_port}/bpm"
        while True:
            try:
                resp = requests.get(url, timeout=2)
                if resp.status_code == 200:
                    text = resp.text.strip()
                    try:
                        # Allow integer or float values
                        hr = float(text)
                        hr = int(hr)
                        # Basic sanity checks
                        if 0 < hr < 250:
                            self.add_heart_rate_reading(hr)
                            # avoid log spam during calibration
                            if not self._is_calibrating:
                                readable_time = time.strftime("%H:%M:%S")
                                print(f"[{readable_time}] Polled HR: {hr}")
                        else:
                            print(f"[WARN] Polled HR out of range: {text}")
                    except ValueError:
                        print(f"[WARN] Could not parse HR from response: {text}")
                else:
                    print(f"[WARN] ESP32 poll returned status {resp.status_code}")
            except requests.RequestException as e:
                print(f"[ERROR] Error polling ESP32 ({url}): {e}")

            time.sleep(self.heart_poll_interval)
    
    def start_calibration(self, seeed_studio_ip):
        """Start 90-second calibration process"""
        with self.lock:
            if self._is_calibrating:
                print("Calibration already in progress")
                return
            
            # seeed_studio_ip parameter kept for API compatibility
            self.seeed_studio_ip = seeed_studio_ip
            self._is_calibrating = True
            self._is_calibrated = False
            self.calibration_start_time = time.time()
            self.calibration_heart_rates = []
            self.calibration_breath_rates = []
        
        print("[*] Calibration started for 90 seconds...")
        print("[*] Both sensors should be posting data during this period...")
        
        # Calibration loop
        start_time = time.time()
        while time.time() - start_time < self.CALIBRATION_DURATION_SECONDS:
            elapsed = int(time.time() - start_time)
            remaining = self.CALIBRATION_DURATION_SECONDS - elapsed
            
            if elapsed % 10 == 0:  # Print every 10 seconds
                with self.lock:
                    hr_count = len(self.calibration_heart_rates)
                    br_count = len(self.calibration_breath_rates)
                print(f"Calibration progress: {elapsed}s / 90s (HR: {hr_count}, BR: {br_count})")
            
            time.sleep(self.CALIBRATION_SAMPLING_INTERVAL)
        
        self._finish_calibration()
    
    def _finish_calibration(self):
        """Finish calibration and calculate baselines"""
        with self.lock:
            self._is_calibrating = False
            
            # Calculate average heart rate
            if self.calibration_heart_rates:
                self.baseline_heart_rate = sum(self.calibration_heart_rates) / len(self.calibration_heart_rates)
            
            # Calculate average breath rate
            if self.calibration_breath_rates:
                self.baseline_breath_rate = sum(self.calibration_breath_rates) / len(self.calibration_breath_rates)
            
            self._is_calibrated = True
            
            print("[OK] Calibration complete!")
            print(f"Baseline Heart Rate: {self.baseline_heart_rate:.2f}")
            print(f"Baseline Breath Rate: {self.baseline_breath_rate:.2f}")
            print(f"Samples collected - HR: {len(self.calibration_heart_rates)}, BR: {len(self.calibration_breath_rates)}")
            
            # Clear calibration data
            self.calibration_heart_rates = []
            self.calibration_breath_rates = []
    
    def get_heart_rate_delta(self):
        """Calculate heart rate delta"""
        if self.baseline_heart_rate == 0:
            return 0.0
        return (self.current_heart_rate - self.baseline_heart_rate) / self.baseline_heart_rate
    
    def get_breath_rate_delta(self):
        """Calculate breath rate delta"""
        if self.baseline_breath_rate == 0:
            return 0.0
        return (self.current_breath_rate - self.baseline_breath_rate) / self.baseline_breath_rate
    
    def calculate_cognitive_load(self):
        """
        Calculate cognitive load using the formula:
        
        1. ΔHR = (HR_current - HR_baseline) / HR_baseline
        2. ΔBR = (BR_current - BR_baseline) / BR_baseline
        3. Load_raw = max(0, 0.6 × ΔHR + 0.4 × ΔBR)
        4. Load_Paas = clamp(1 + (Load_raw / 0.40) × 8, 1, 9)
        
        Returns: Cognitive load on Paas 9-point scale (1-9)
        """
        if not self._is_calibrated:
            return 1.0  # Return minimum Paas score if not calibrated
        
        # Current breath rate is automatically updated by ESPHome listener
        # No need to fetch manually
        
        delta_hr = self.get_heart_rate_delta()
        delta_br = self.get_breath_rate_delta()
        
        # Calculate raw load
        load_raw = max(0, self.WEIGHT_HR * delta_hr + self.WEIGHT_BR * delta_br)
        
        # Map to Paas 9-point scale
        load_paas = 1 + (load_raw / self.MAX_DELTA_FOR_PAAS_9) * 8
        
        # Clamp to valid range [1, 9]
        return self._clamp(load_paas, 1.0, 9.0)
    
    def get_predicted_cognitive_load(self):
        """Predict a future cognitive load value based on recent trends.
        
        Maintains an internal sliding window of the last 10 calculated loads.
        Once at least five samples are available it computes the average of the
        most recent three and the three values immediately preceding them to
        determine a simple linear trend.  This trend is extrapolated 30 seconds
        into the future and clamped to the valid Paas range.
        """
        # store last 10 values; make atomic with lock
        with self.lock:
            if not hasattr(self, 'recent_loads'):
                self.recent_loads = []
            
            current = self.calculate_cognitive_load()
            self.recent_loads.append(current)
            
            # keep last 10 values
            if len(self.recent_loads) > 10:
                self.recent_loads.pop(0)
            
            # need at least 5 values to predict
            if len(self.recent_loads) >= 5:
                # average of last 3 values
                recent_avg = sum(self.recent_loads[-3:]) / 3
                
                # average of 3 values before that
                older_avg = sum(self.recent_loads[-6:-3]) / 3
                
                # calculate trend (is it going up or down?)
                trend = recent_avg - older_avg
                
                # predict 30 seconds ahead
                prediction = current + (trend * 30)
                return self._clamp(prediction, 1.0, 9.0)
        
        return current  # not enough data, return current
    
    @staticmethod
    def _clamp(value, min_val, max_val):
        """Clamp value between min and max"""
        return max(min_val, min(max_val, value))
    
    def get_remaining_calibration_time(self):
        """Get remaining calibration time in seconds"""
        if not self._is_calibrating:
            return 0
        elapsed = int(time.time() - self.calibration_start_time)
        return max(0, self.CALIBRATION_DURATION_SECONDS - elapsed)
    
    # Getters
    def get_current_heart_rate(self):
        return self.current_heart_rate
    
    def get_current_breath_rate(self):
        # Breath rate is automatically updated by ESPHome listener
        return self.current_breath_rate
    
    def get_baseline_heart_rate(self):
        return self.baseline_heart_rate
    
    def get_baseline_breath_rate(self):
        return self.baseline_breath_rate
    
    def is_calibrated(self):
        return self._is_calibrated
    
    def is_calibrating(self):
        return self._is_calibrating
