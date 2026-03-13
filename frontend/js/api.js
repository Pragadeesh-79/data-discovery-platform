const BASE_URL = "http://127.0.0.1:8000";

async function fetchFromAPI(endpoint, options = {}) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Backend connection error: ${error.message}`);
        // Do not crash UI
        return { error: "Backend connection error" };
    }
}

async function scanLocalFolder() {
    return await fetchFromAPI("/scan/local");
}

async function fetchRiskScore() {
    return await fetchFromAPI("/risk");
}

async function fetchReports() {
    return await fetchFromAPI("/reports");
}

async function fetchHeatmap() {
    return await fetchFromAPI("/reports/heatmap");
}

async function fetchLineage() {
    return await fetchFromAPI("/lineage");
}

async function uploadAndScanFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${BASE_URL}/scan/upload`, {
            method: "POST",
            body: formData,
        });
        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Backend connection error: ${error.message}`);
        return { error: "Backend connection error" };
    }
}

// Global exposure for HTML inline calls
window.scanLocalFolder = scanLocalFolder;
window.uploadAndScanFile = uploadAndScanFile;
window.fetchRiskScore = fetchRiskScore;
window.fetchReports = fetchReports;
window.fetchHeatmap = fetchHeatmap;
window.fetchLineage = fetchLineage;
