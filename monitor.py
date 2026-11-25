
"""ЛР4. Мониторинг нагрузки компьютера."""

import csv
import time
from datetime import datetime

import psutil

INTERVAL = 1
SAMPLES = 20

THRESHOLDS = {
    "cpu": 80,
    "ram": 70,
    "disk": 80,
    "max_core": 80
}

LOG_FILE = "monitor_log.csv"


def take_sample():
    return {
        "time": datetime.now().strftime("%H:%M:%S"),
        "cpu": psutil.cpu_percent(interval=None),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "max_core": max(psutil.cpu_percent(percpu=True))
    }


def check_alerts(sample):
    alerts = []

    for metric, limit in THRESHOLDS.items():
        if sample[metric] >= limit:
            alerts.append(
                f"{metric.upper()} = {sample[metric]}% "
                f"(порог {limit}%)"
            )

    return alerts


def main():
    psutil.cpu_percent(interval=None)
    psutil.cpu_percent(interval=None, percpu=True)

    samples = []

    with open(
        LOG_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=[
                "time",
                "cpu",
                "ram",
                "disk",
                "max_core",
                "alert"
            ]
        )

        writer.writeheader()

        for _ in range(SAMPLES):
            time.sleep(INTERVAL)

            s = take_sample()
            alerts = check_alerts(s)

            s["alert"] = "; ".join(alerts)

            writer.writerow(s)
            samples.append(s)

            mark = " <-- ВНИМАНИЕ: " + s["alert"] if alerts else ""

            print(
                f"{s['time']} "
                f"CPU {s['cpu']:5.1f}% "
                f"RAM {s['ram']:5.1f}% "
                f"DISK {s['disk']:5.1f}% "
                f"MAX CORE {s['max_core']:5.1f}%"
                f"{mark}"
            )

    print("\nСТАТИСТИКА МОНИТОРИНГА")

    metrics = ["cpu", "ram", "disk", "max_core"]

    for metric in metrics:
        values = [s[metric] for s in samples]

        print(
            f"{metric.upper()}: "
            f"Среднее = {sum(values) / len(values):.1f}%, "
            f"Максимум = {max(values):.1f}%, "
            f"Минимум = {min(values):.1f}%"
        )

    print(f"\nЖурнал сохранён в {LOG_FILE}")


if __name__ == "__main__":
    main()
