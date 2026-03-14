// frontend/js/scanner.js

document.addEventListener("DOMContentLoaded", () => {
    // 1. Grab DOM Elements
    const fileInput = document.getElementById("fileUploadInput");
    const uploadBtn = document.getElementById("uploadProcessBtn");
    const uploadText = document.getElementById("uploadText");
    
    const progressSection = document.querySelector(".scan-progress");
    const progressFill = document.querySelector(".progress-bar-fill");
    const progressText = document.querySelector(".progress-text");
    
    const resultsSection = document.querySelector(".scan-results");
    const resultsBody = document.getElementById("scanResultsBody");
    
    let selectedFile = null;

    // 2. File Selection Logic
    if (uploadBtn) {
        uploadBtn.addEventListener("click", () => {
            if (!selectedFile && fileInput.files.length > 0) {
                selectedFile = fileInput.files[0];
            }
            if (!selectedFile) {
                fileInput.click();
                return;
            }
            handleScan();
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (this.files.length > 0) {
                selectedFile = this.files[0];
                if (uploadText) {
                    uploadText.innerText = `Selected: ${selectedFile.name}. Click Upload!`;
                    uploadText.style.color = "#4ade80";
                }
            }
        });
    }

    // 3. Scan & Integration Logic
    async function handleScan() {
        if (!selectedFile) return;

        // SAFEGUARD: Ensure api.js loaded correctly before proceeding
        if (typeof submitScanResult !== "function") {
            const errMsg = "Critical Error: API helper (api.js) is missing! Ensure api.js is loaded above scanner.js in scan.html";
            console.error(errMsg);
            alert(errMsg);
            return;
        }
        
        // Lock UI State
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning...';
        
        if (progressSection) progressSection.style.display = "block";
        if (resultsSection) resultsSection.style.display = "none";

        // Fun hackathon simulation: Fake progress bar
        let fakeProg = 5;
        let pInterval = setInterval(() => {
            if (fakeProg < 90) {
                fakeProg += Math.floor(Math.random() * 15) + 5;
                if (fakeProg > 90) fakeProg = 90;
                if (progressFill) progressFill.style.width = fakeProg + "%";
                if (progressText) progressText.innerText = `Analyzing content... (${fakeProg}%)`;
            }
        }, 500);

        try {
            // STEP 1: SIMULATE SCAN DELAY (2.5 seconds)
            await new Promise(resolve => setTimeout(resolve, 2500));
            
            // STEP 2: MOCK DETECTED PII DATA 
            // In reality, this data would come from the python backend analyzing the file bytes.
            const mockExtractedPII = [
                {
                    type: "Email",
                    value: "ceo@company.com",
                    location: `uploads/${selectedFile.name}`,
                    source: "local_folder",
                    owner: "Executive Team",
                    sensitivity: "Medium",
                    risk_score: 5
                },
                {
                    type: "PAN",
                    value: "ABCDE1234F",
                    location: `uploads/${selectedFile.name}`,
                    source: "local_folder",
                    owner: "Finance Team",
                    sensitivity: "High",
                    risk_score: 8
                }
            ];

            // STEP 3: SEND DATA TO BACKEND via api.js using POST /scan-results
            console.log(`[SCANNER] Pushing ${mockExtractedPII.length} found records to database...`);
            
            for (const record of mockExtractedPII) {
                console.log(`[SCANNER] Sending payload:`, record);
                const response = await submitScanResult(record); // Calls FastAPI!
                console.log(`[BACKEND] Accepted:`, response);
            }
            
            // STEP 4: UPDATE UI PROGRESS
            clearInterval(pInterval);
            if (progressFill) progressFill.style.width = "100%";
            if (progressText) progressText.innerText = "Scan Complete! Check Database.";
            
            setTimeout(() => { if (progressSection) progressSection.style.display = "none"; }, 1000);

            // STEP 5: RENDER UI TABLE
            if (resultsBody) {
                resultsBody.innerHTML = "";
                mockExtractedPII.forEach(item => {
                    let riskColor = item.sensitivity === "High" ? "#ff4d4d" : "#fbbf24";
                    resultsBody.innerHTML += `
                        <tr style="border-bottom:1px solid #333;">
                            <td style="padding:12px;"><strong>${item.type}</strong></td>
                            <td style="padding:12px; font-family:monospace;">${item.value}</td>
                            <td style="padding:12px;"><span style="background:#334155; padding:4px 8px; border-radius:4px;">${item.sensitivity}</span></td>
                            <td style="padding:12px; color:#94a3b8;">${item.location}</td>
                            <td style="padding:12px; color:${riskColor}; font-weight:bold;">${item.risk_score} / 10</td>
                        </tr>
                    `;
                });
            }
            
            if (resultsSection) {
                resultsSection.style.display = "block";
            }

        } catch (error) {
            console.error("[SCANNER ERROR]", error);
            alert("An error occurred during the scan or database push. Check the browser console.");
        } finally {
            // Restore UI Buttons
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = '<i class="fas fa-shield-halved"></i> Upload and Scan';
            selectedFile = null;
            if (fileInput) fileInput.value = "";
            if (uploadText) {
                uploadText.innerText = `or click to browse your computer`;
                uploadText.style.color = "";
            }
        }
    }
});
