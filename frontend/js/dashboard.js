// frontend/js/dashboard.js

let piiChartInstance = null; // Store chart instance to destroy it before re-rendering

document.addEventListener("DOMContentLoaded", () => {
    // Initial fetch
    fetchAndUpdateDashboard();

    // Set up real-time polling every 5 seconds
    setInterval(fetchAndUpdateDashboard, 5000);
});

async function fetchAndUpdateDashboard() {
    // 1. Fetch data from backend API
    const data = await getDashboardStats();

    if (!data) {
        console.error("Failed to load dashboard data. Ensure backend is running!");
        return;
    }

    // 2. Safely Update UI Elements
    const filesScannedEl = document.getElementById("filesScannedVal");
    const piiDetectedEl = document.getElementById("piiDetectedVal");
    const highRiskEl = document.getElementById("highRiskVal");
    const complianceStatusEl = document.getElementById("complianceStatus");

    if (filesScannedEl) filesScannedEl.innerText = data.files_scanned !== undefined ? data.files_scanned : 0;
    if (piiDetectedEl) piiDetectedEl.innerText = data.pii_detected !== undefined ? data.pii_detected : 0;
    if (highRiskEl) highRiskEl.innerText = data.high_risk !== undefined ? data.high_risk : 0;

    if (complianceStatusEl && data.compliance_status) {
        complianceStatusEl.innerText = data.compliance_status;
        // Apply color logic based on status
        if (data.compliance_status === "Review Required") {
            complianceStatusEl.style.color = "#ff4d4d"; // Red alert
        } else {
            complianceStatusEl.style.color = "#4ade80"; // Green safe
        }
    }

    // 3. Render PII Distribution Chart
    if (data.pii_types && Object.keys(data.pii_types).length > 0) {
        renderPIIChart(data.pii_types);
    }
}

/**
 * Initializes and dynamically handles Chart.js graphing 
 */
function renderPIIChart(piiTypes) {
    const ctx = document.getElementById("piiChart");
    if (!ctx) return;

    // If a chart exists, destroy it before rendering a new one to prevent glitching overlaps
    if (piiChartInstance) {
        piiChartInstance.destroy();
    }

    // Extract Keys (e.g. Email, PAN) and Values (e.g. 5, 2)
    const labels = Object.keys(piiTypes);
    const data = Object.values(piiTypes);

    piiChartInstance = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Identified Types",
                data: data,
                backgroundColor: ["#ecc94b", "#4ade80", "#60a5fa", "#f87171", "#c084fc"],
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false 
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: "#9ca3af" }
                },
                x: {
                    ticks: { color: "#9ca3af" }
                }
            }
        }
    });
}
