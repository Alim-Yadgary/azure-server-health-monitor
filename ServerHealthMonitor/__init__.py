"""
Azure Function: ServerHealthMonitor
Author: Alim Yadgary
Description:
    HTTP-triggered Azure Function that returns a real-time health report
    for the host server — CPU usage, memory, disk space, and uptime.
    Designed to mirror the kind of monitoring done in a data centre
    environment, but deployed as a serverless cloud-native function on
    Microsoft Azure.

Trigger:  HTTP GET/POST  →  /api/ServerHealthMonitor
Returns:  JSON health report with status classification
"""

import azure.functions as func
import json
import platform
import datetime
import psutil  # lightweight cross-platform system metrics library


def main(req: func.HttpRequest) -> func.HttpResponse:
    """Entry point called by the Azure Functions runtime."""

    # ── Collect system metrics ──────────────────────────────────────────
    cpu_percent   = psutil.cpu_percent(interval=1)          # 1-second sample
    memory        = psutil.virtual_memory()
    disk          = psutil.disk_usage("/")
    boot_time     = datetime.datetime.fromtimestamp(psutil.boot_time())
    uptime        = datetime.datetime.now() - boot_time

    # ── Classify overall health ─────────────────────────────────────────
    # Thresholds mirror common SLA alert rules used in enterprise data centres
    warnings = []

    if cpu_percent > 85:
        warnings.append(f"HIGH CPU: {cpu_percent}% (threshold: 85%)")
    if memory.percent > 90:
        warnings.append(f"HIGH MEMORY: {memory.percent}% (threshold: 90%)")
    if disk.percent > 80:
        warnings.append(f"LOW DISK SPACE: {disk.percent}% used (threshold: 80%)")

    status = "HEALTHY" if not warnings else "WARNING"

    # ── Build response payload ──────────────────────────────────────────
    report = {
        "status":     status,
        "timestamp":  datetime.datetime.utcnow().isoformat() + "Z",
        "host": {
            "os":       platform.system(),
            "version":  platform.version(),
            "uptime":   str(uptime).split(".")[0],          # trim microseconds
        },
        "metrics": {
            "cpu": {
                "usage_percent": cpu_percent,
                "core_count":    psutil.cpu_count(logical=True),
                "health":        "OK" if cpu_percent <= 85 else "WARNING",
            },
            "memory": {
                "total_gb":    round(memory.total  / (1024 ** 3), 2),
                "used_gb":     round(memory.used   / (1024 ** 3), 2),
                "free_gb":     round(memory.available / (1024 ** 3), 2),
                "usage_percent": memory.percent,
                "health":        "OK" if memory.percent <= 90 else "WARNING",
            },
            "disk": {
                "total_gb":    round(disk.total / (1024 ** 3), 2),
                "used_gb":     round(disk.used  / (1024 ** 3), 2),
                "free_gb":     round(disk.free  / (1024 ** 3), 2),
                "usage_percent": disk.percent,
                "health":        "OK" if disk.percent <= 80 else "WARNING",
            },
        },
        "warnings": warnings,
        "project": {
            "author":      "Alim Yadgary",
            "description": "Cloud-native server health monitor — Azure Functions + Python",
            "cert":        "Microsoft Azure Fundamentals (AZ-900)",
        }
    }

    # ── Return JSON response ────────────────────────────────────────────
    return func.HttpResponse(
        body=json.dumps(report, indent=2),
        status_code=200,
        mimetype="application/json"
    )
