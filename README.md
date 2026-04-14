# ☁️ Azure Server Health Monitor

> A cloud-native server health monitoring function built with **Python** and deployed on **Microsoft Azure Functions**.  
> Built to demonstrate real-world cloud skills aligned with the **AZ-900** certification and data centre operations experience.

---

## 🔍 What It Does

This Azure Function provides an HTTP endpoint that returns a **real-time server health report**, including:

| Metric | Detail |
|--------|--------|
| 🖥️ CPU Usage | Current usage % with health status |
| 🧠 Memory | Total, used, free (GB) + usage % |
| 💾 Disk Space | Total, used, free (GB) + usage % |
| ⏱️ Uptime | Time since last boot |
| ⚠️ Warnings | Auto-flagged if thresholds are breached |

### Alert Thresholds (mirrors enterprise data centre SLA rules)

| Metric | Warning Threshold |
|--------|------------------|
| CPU | > 85% |
| Memory | > 90% |
| Disk | > 80% used |

---

## 📡 Example Response

```json
{
  "status": "HEALTHY",
  "timestamp": "2026-04-14T13:00:00Z",
  "host": {
    "os": "Linux",
    "version": "...",
    "uptime": "2 days, 4:31:12"
  },
  "metrics": {
    "cpu": {
      "usage_percent": 12.5,
      "core_count": 2,
      "health": "OK"
    },
    "memory": {
      "total_gb": 1.75,
      "used_gb": 0.85,
      "free_gb": 0.9,
      "usage_percent": 48.6,
      "health": "OK"
    },
    "disk": {
      "total_gb": 30.0,
      "used_gb": 8.2,
      "free_gb": 21.8,
      "usage_percent": 27.3,
      "health": "OK"
    }
  },
  "warnings": []
}
```

---

## 🗂️ Project Structure

```
azure-monitor-project/
│
├── ServerHealthMonitor/
│   ├── __init__.py        # Main function logic
│   └── function.json      # HTTP trigger binding config
│
├── host.json              # Azure Functions host configuration
├── requirements.txt       # Python dependencies
├── local.settings.json    # Local dev settings (not committed)
└── .gitignore
```

---

## 🚀 How to Deploy to Azure

### Prerequisites
- [Azure account](https://azure.microsoft.com/free/) (free tier works)
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local) installed
- Python 3.9+

### Steps

**1. Clone the repo**
```bash
git clone https://github.com/Alim-Yadgary/azure-server-health-monitor.git
cd azure-server-health-monitor
```

**2. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**3. Test locally**
```bash
func start
# Visit: http://localhost:7071/api/health
```

**4. Deploy to Azure**
```bash
# Login to Azure
az login

# Create a resource group
az group create --name rg-health-monitor --location uksouth

# Create a storage account (required by Functions)
az storage account create --name sthealthmonitor --location uksouth \
  --resource-group rg-health-monitor --sku Standard_LRS

# Create the Function App
az functionapp create --resource-group rg-health-monitor \
  --consumption-plan-location uksouth \
  --runtime python --runtime-version 3.9 \
  --functions-version 4 \
  --name alim-health-monitor \
  --storage-account sthealthmonitor \
  --os-type linux

# Deploy your code
func azure functionapp publish alim-health-monitor
```

**5. Test your live endpoint**
```
GET https://alim-health-monitor.azurewebsites.net/api/health
```

---

## 🛠️ Technologies Used

- **Microsoft Azure Functions** (serverless compute)
- **Python 3.9**
- **psutil** (system metrics)
- **Azure CLI**

---

## 📜 Certifications

- ✅ Microsoft Azure Fundamentals — **AZ-900**
- 📚 In progress: Microsoft Azure Administrator — **AZ-104**

---

## 👤 Author

**Alim Yadgary**  
Data Centre Engineer | Cloud & Infrastructure  
[LinkedIn](https://www.linkedin.com/in/alim-yadgary-bb2041228/) • [Email](mailto:Yadgary2@hotmail.com)

---

*This project was built as part of a portfolio to demonstrate practical Azure and Python skills alongside data centre operations experience.*
