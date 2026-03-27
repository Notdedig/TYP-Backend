"""
Cognitive Load Service
Handles calibration and cognitive load calculations
"""

import time
import requests
import threading
from threading import Lock


class CognitiveLoadService:
    # Constants for cognitive load calculation
    WEIGHT_HR = 0.6
    WEIGHT_BR = 0.4
    MAX_DELTA_FOR_PAAS_9 = 0.15  # 40% increase maps to Paas 9
    CALIBRATION_DURATION_SECONDS = 90
    CALIBRATION_SAMPLING_INTERVAL = 1  # Sample every second

    def __init__(self):
        self.lock = Lock()

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

        # Data storage during calibration
        self.calibration_heart_rates = []
        self.calibration_breath_rates = []

    def add_heart_rate_reading(self, heart_rate):
        """Add a heart rate reading"""
        with self.lock:
            self.current_heart_rate = heart_rate

            if self._is_calibrating and heart_rate > 0:
                self.calibration_heart_rates.append(heart_rate)

    def add_breath_rate_reading(self, breath_rate):
        """Add a breath rate reading"""
        with self.lock:
            self.current_breath_rate = breath_rate

            if self._is_calibrating and breath_rate > 0:
                self.calibration_breath_rates.append(breath_rate)

        # Log outside lock
        if not self._is_calibrating:
            readable_time = time.strftime("%H:%M:%S")
            print(f"[{readable_time}] Breath Rate: {breath_rate}")

    def _start_esp32_poller(self):
        """Start background thread for ESP32 polling"""

        def run_poller():
            try:
                self._esp32_poller()
            except Exception as e:
                print(f"[ERROR] ESP32 poller terminated: {e}")

        thread = threading.Thread(target=run_poller, daemon=True)
        thread.start()

        print(
            f"[*] Starting ESP32 poller at "
            f"{self.heart_sensor_ip}:{self.heart_sensor_port}"
        )

    def _esp32_poller(self):
        """Continuously poll ESP32 for heart rate"""
        url = f"http://{self.heart_sensor_ip}:{self.heart_sensor_port}/bpm"

        while True:
            try:
                resp = requests.get(url, timeout=2)

                if resp.status_code == 200:
                    text = resp.text.strip()

                    try:
                        hr = int(float(text))

                        if 0 < hr < 250:
                            self.add_heart_rate_reading(hr)

                            if not self._is_calibrating:
                                readable_time = time.strftime("%H:%M:%S")
                                print(f"[{readable_time}] Polled HR: {hr}")
                        else:
                            print(f"[WARN] HR out of range: {text}")

                    except ValueError:
                        print(f"[WARN] Invalid HR response: {text}")
                else:
                    print(f"[WARN] Status {resp.status_code}")

            except requests.RequestException as e:
                print(f"[ERROR] ESP32 polling failed: {e}")

            time.sleep(self.heart_poll_interval)

    def start_calibration(self):
        """Start 90-second calibration"""
        with self.lock:
            if self._is_calibrating:
                print("Calibration already in progress")
                return

            self._is_calibrating = True
            self._is_calibrated = False
            self.calibration_start_time = time.time()
            self.calibration_heart_rates.clear()
            self.calibration_breath_rates.clear()

        print("[*] Calibration started (90 seconds)...")

        start_time = time.time()

        while time.time() - start_time < self.CALIBRATION_DURATION_SECONDS:
            elapsed = int(time.time() - start_time)

            if elapsed % 10 == 0:
                with self.lock:
                    print(
                        f"Progress: {elapsed}s / 90s "
                        f"(HR: {len(self.calibration_heart_rates)}, "
                        f"BR: {len(self.calibration_breath_rates)})"
                    )

            time.sleep(self.CALIBRATION_SAMPLING_INTERVAL)

        self._finish_calibration()

    def _finish_calibration(self):
        """Compute baselines"""
        with self.lock:
            self._is_calibrating = False

            if self.calibration_heart_rates:
                self.baseline_heart_rate = (
                    sum(self.calibration_heart_rates)
                    / len(self.calibration_heart_rates)
                )

            if self.calibration_breath_rates:
                self.baseline_breath_rate = (
                    sum(self.calibration_breath_rates)
                    / len(self.calibration_breath_rates)
                )

            self._is_calibrated = True

            print("[OK] Calibration complete!")
            print(f"Baseline HR: {self.baseline_heart_rate:.2f}")
            print(f"Baseline BR: {self.baseline_breath_rate:.2f}")

            self.calibration_heart_rates.clear()
            self.calibration_breath_rates.clear()

    def get_heart_rate_delta(self):
        if self.baseline_heart_rate == 0:
            return 0.0

        return (
            self.current_heart_rate - self.baseline_heart_rate
        ) / self.baseline_heart_rate

    def get_breath_rate_delta(self):
        if self.baseline_breath_rate == 0:
            return 0.0

        return (
            self.current_breath_rate - self.baseline_breath_rate
        ) / self.baseline_breath_rate

    def calculate_cognitive_load(self):
        """Return Paas scale (1–9)"""
        if not self._is_calibrated:
            return 1.0

        delta_hr = self.get_heart_rate_delta()
        delta_br = self.get_breath_rate_delta()

        load_raw = max(
            0,
            self.WEIGHT_HR * delta_hr +
            self.WEIGHT_BR * delta_br
        )

        load_paas = 1 + (load_raw / self.MAX_DELTA_FOR_PAAS_9) * 8

        return self._clamp(load_paas, 1.0, 9.0)

    def get_predicted_cognitive_load(self):
        with self.lock:
            if not hasattr(self, "recent_loads"):
                self.recent_loads = []

            current = self.calculate_cognitive_load()
            self.recent_loads.append(current)

            if len(self.recent_loads) > 10:
                self.recent_loads.pop(0)

            if len(self.recent_loads) >= 6:
                recent_avg = sum(self.recent_loads[-3:]) / 3
                older_avg = sum(self.recent_loads[-6:-3]) / 3

                trend = recent_avg - older_avg
                prediction = current + (trend * 30)

                return self._clamp(prediction, 1.0, 9.0)

        return current

    @staticmethod
    def _clamp(value, min_val, max_val):
        return max(min_val, min(max_val, value))

    def get_remaining_calibration_time(self):
        if not self._is_calibrating:
            return 0

        elapsed = int(time.time() - self.calibration_start_time)
        return max(0, self.CALIBRATION_DURATION_SECONDS - elapsed)

    # Getters
    def get_current_heart_rate(self):
        return self.current_heart_rate

    def get_current_breath_rate(self):
        return self.current_breath_rate

    def get_baseline_heart_rate(self):
        return self.baseline_heart_rate

    def get_baseline_breath_rate(self):
        return self.baseline_breath_rate

    def is_calibrated(self):
        return self._is_calibrated

    def is_calibrating(self):
        return self._is_calibrating