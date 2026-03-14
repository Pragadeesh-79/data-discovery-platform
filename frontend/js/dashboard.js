// frontend/js/dashboard.js

let piiChartInstance = null; // Store chart instance to destroy it before re-rendering

document.addEventListener("DOMContentLoaded", async () => {
    // 1. Fetch data from backend API
    const data = await getDashboardStats();

    if (!data) {
        console.error("Failed to load dashboard data. Ensure backend is running!");
        return;
    }

    // 2. Safely Update UI Elements
    const totalRecordsEl = document.getElementById("totalRecords");
    const riskScoreEl = document.getElementById("riskScore");
    const complianceStatusEl = document.getElementById("complianceStatus");

    if (totalRecordsEl) totalRecordsEl.innerText = data.total_records;
    if (riskScoreEl) riskScoreEl.innerText = data.total_risk_score;
    if (complianceStatusEl) complianceStatusEl.innerText = data.compliance_status;

    // Apply color logic based on status
    if (complianceStatusEl && data.compliance_status === "Review Required") {
        complianceStatusEl.style.color = "#ff4d4d"; // Red alert
    } else if (complianceStatusEl) {
        complianceStatusEl.style.color = "#4ade80"; // Green safe
    }

    // 3. Render PII Distribution Chart
    renderPIIChart(data.pii_types);
});

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
