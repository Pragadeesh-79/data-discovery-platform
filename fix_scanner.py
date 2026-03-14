import re

with open(r"d:\HACKATHON\data-discovery-platform\frontend\js\scanner.js", "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r"try\s*\{.*?\}\s*catch\s*\(error\)\s*\{.*?\}\s*finally\s*\{", re.DOTALL)

new_try_block = """try {
            if (typeof uploadFileForScan !== "function") {
                throw new Error("Missing uploadFileForScan. Please ensure the latest api.js is loaded.");
            }

            console.log(`[SCANNER] Uploading ${selectedFile.name} for real scanning...`);
            const scanResponse = await uploadFileForScan(selectedFile);

            clearInterval(pInterval);

            if (!scanResponse) {
                throw new Error("Upload failed. No response received.");
            }

            console.log(`[BACKEND] Scan complete:`, scanResponse);
            const extractedPII = scanResponse.detected_records || []; 

            if (progressFill) progressFill.style.width = "100%";
            if (progressText) progressText.innerText = `Scan Complete! Found ${extractedPII.length} records.`;
            
            setTimeout(() => { if (progressSection) progressSection.style.display = "none"; }, 1500);

            if (resultsBody) {
                resultsBody.innerHTML = "";
                if (extractedPII.length === 0) {
                    resultsBody.innerHTML = `<tr><td colspan="5" style="padding:12px; text-align:center; color:#94a3b8;">No PII detected! 🎉</td></tr>`;
                } else {
                    extractedPII.forEach(item => {
                        let riskColor = item.sensitivity === "High" ? "#ff4d4d" : (item.sensitivity === "Medium" ? "#fbbf24" : "#4ade80");
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
            }

            if (resultsSection) {
                resultsSection.style.display = "block";
            }

            if (typeof getDashboardStats === "function") {
                console.log("[SCANNER] Fetching updated dashboard stats...");
                const newStats = await getDashboardStats();
                console.log("[SCANNER] Dashboard stats refreshed:", newStats);
                const headerTotal = document.getElementById("totalRecords");
                if (headerTotal && newStats) {
                    headerTotal.innerText = newStats.total_records;
                }
            }

        } catch (error) {
            clearInterval(pInterval);
            if (progressFill) progressFill.style.backgroundColor = "red";
            if (progressText) progressText.innerText = "Scan failed!";
            console.error("[SCANNER ERROR]", error);
            alert("An error occurred during the scan or database push. Check the browser console.");
        } finally {"""

content = pattern.sub(new_try_block, content)

with open(r"d:\HACKATHON\data-discovery-platform\frontend\js\scanner.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated scanner.js successfully")
