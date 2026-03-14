// frontend/js/api.js

const API_BASE_URL = "http://localhost:8000";

/**
 * Fetches the aggregated dashboard statistics from the backend.
 * @returns {Promise<Object>} Dashboard data (total records, risk score, PII types, etc.)
 */
async function getDashboardStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/dashboard-stats`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching dashboard stats:", error);
        return null;
    }
}

/**
 * Fetches the inventory of detected PII records.
 * @returns {Promise<Object>} List of PII records.
 */
async function getInventory() {
    try {
        const response = await fetch(`${API_BASE_URL}/inventory`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error fetching inventory:", error);
        return null;
    }
}

/**
 * Submits a new scan result to the backend.
 * @param {Object} record - The PII record to save.
 */
async function submitScanResult(record) {
    try {
        const response = await fetch(`${API_BASE_URL}/scan-results`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(record)
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error("Error submitting scan result:", error);
        return null;
    }
}

/**
 * Uploads a file to the backend for real PII scanning.
 * @param {File} file - The file to upload.
 */
async function uploadFileForScan(file) {
    console.log("Uploading file...", file.name);
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE_URL}/scan/upload`, {
            method: "POST",
            body: formData
            // Note: When using FormData, do NOT set 'Content-Type' manually.   
        });
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Scan response:", data);
        return data;
