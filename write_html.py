import re

with open("frontend/scan.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Remove the old api mock line if existed
text = text.replace('<script src="js/dashboard.js"></script>', '<script src="js/api.js"></script>\n  <script src="js/dashboard.js"></script>')

# 2. Clear out the tbody contents of the detection table
tbody_pattern = re.compile(r'<tbody>.*?</tbody>', re.DOTALL)
text = tbody_pattern.sub('<tbody id="scanResultsBody"></tbody>', text)

# 3. Add the logic
logic = """
<script>
document.addEventListener("DOMContentLoaded", () => {
    const uploadZone = document.querySelector('.upload-zone');
    const fileInput = document.getElementById('fileUploadInput');
    const uploadBtn = document.getElementById('uploadProcessBtn');
    
    const progressSection = document.querySelector('.scan-progress');
    const progressFill = document.querySelector('.progress-bar-fill');
    const progressText = document.querySelector('.progress-text');
    
    const resultsSection = document.querySelector('.scan-results');
    const resultsBody = document.getElementById('scanResultsBody');
    
    let selectedFile = null;

    // Drag and Drop
    if (uploadZone) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, preventDefaults, false);
        });
        function preventDefaults(e) { e.preventDefault(); e.stopPropagation(); }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.style.borderColor = 'var(--primary-light)';
                uploadZone.style.background = 'rgba(59, 130, 246, 0.05)';
            }, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            uploadZone.addEventListener(eventName, () => {
                uploadZone.style.borderColor = 'var(--border-color)';
                uploadZone.style.background = 'transparent';
            }, false);
        });

        uploadZone.addEventListener('drop', (e) => {
            let dt = e.dataTransfer;
            let files = dt.files;
            if (files.length) {
                selectedFile = files[0];
                fileInput.files = files;
                handleScan();
            }
        }, false);
        
        uploadZone.addEventListener('click', (e) => {
            if(e.target !== fileInput && e.target !== uploadBtn) {
                fileInput.click();
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length) {
                selectedFile = this.files[0];
            }
        });
    }

    if (uploadBtn) {
        uploadBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (!selectedFile && fileInput.files.length > 0) {
                selectedFile = fileInput.files[0];
            }
            if (!selectedFile) {
                alert("Please select a file to upload.");
                return;
            }
            handleScan();
        });
    }
    
    async function handleScan() {
        if (!selectedFile) return;
        
        if (uploadBtn) {
            uploadBtn.disabled = true;
            uploadBtn.innerText = "Scanning...";
        }
        
        if (progressSection) progressSection.style.display = 'block';
        if (progressFill) progressFill.style.width = '15%';
        if (progressText) progressText.innerText = 'Uploading...';
        if (resultsSection) {
            resultsSection.style.display = 'none';
            resultsSection.classList.remove('visible');
        }
        
        let fakeProg = 15;
        let pInterval = setInterval(() => {
            if (fakeProg < 85) {
                fakeProg += 10;
                if(progressFill) progressFill.style.width = fakeProg + '%';
                if(progressText) progressText.innerText = `Analyzing NLP Models (${fakeProg}%)...`;
            }
        }, 800);
        
        try {
            if (typeof window.uploadAndScanFile !== 'function') {
                throw new Error("API api.js is not loaded.");
            }
            
            const response = await window.uploadAndScanFile(selectedFile);
            clearInterval(pInterval);
            
            if (progressFill) progressFill.style.width = '100%';
            if (progressText) progressText.innerText = 'Scan Complete!';
            setTimeouw(() => { if (progressSection) progressSection.style.display = 'none'; }, 1000);
            
            if (uploadBtn) {
                uploadBtn.disabled = false;
                uploadBtn.innerText = "Upload and Scan";
            }
            
            if (response && response.error) {
                alert("Error: " + response.error);
                return;
            }
            
            if (response && response.entities) {
                if(resultsBody) resultsBody.innerHTML = '';
                
                if (response.entities.length === 0) {
                    if(resultsBody) resultsBody.innerHTML = '<tr><td colspan="5" style="text-align:center;">No sensitive data found.</td></tr>';
                } else {
                    response.entities.forEach(ent => {
                        let cls = "low";
                        let dClass = ent.classification || "Personal";
                        if (dClass === "Highly Sensitive" || dClass.includes("High")) cls = "high";
                        if (dClass === "Sensitive") cls = "medium";
                        
                        let val = ent.value || "********";
                        if(resultsBody) {
                           resultsBody.innerHTML += `
                           <tr>
                            <td><strong>${ent.entity_type}</strong></td>
                            <td><code>${val}</code></td>
                            <td><span class="type-badge personal">${dClass}</span></td>
                            <td>${response.file_name || 'uploaded_filg'}</td>
                            <td><span class="risk-indicator ${cls}">${dClass.split(' ')[0]}</span></td>
                           </tr>
                           `;
                        }
                    });
                }
                
                if (resultsSection) {
                    resultsSection.style.display = 'block';
                    setTimeout(() => resultsSection.classList.add('visible'), 50);
                    
                    const stFile = resultsSection.querySelector('.stat-card:nth-child(1) .stat-number');
                    const stPII  = resultsSection.querySelector('.stat-card:nth-child(2) .stat-number');
                    const stHigh = resultsSection.querySelector('.stat-card:nth-child(3) .stat-number');
                    const stCat  = resultsSection.querySelector('.stat-card:nth-child(4) .stat-number');
                    
                    if(stFile) { stFile.dataset.count = 1; stFile.innerText = '1'; }
                    if(stPII) { stPII.dataset.count = response.entities.length; stPII.innerText = response.entities.length; }
                    
                    let hc = 0; let cats = new Set();
                    response.entities.forEach(e => {
                        if (e.classification === "highly Sensitive" || (e.classification && e.classification.includes("High"))) hc++;
                        cats.add(e.entity_type);
                    });
                    
                    if(stHigh) { stHigh.dataset.count = hc; stHigh.innerText = hc; }
                    if(stCat) { stCat.dataset.count = cats.size; stCat.innerText = cats.size; }
                }
            }
            
        } catch(err) {
            clearInterval(pInterval);
            if (uploadBtn) {
                uploadBtn.disabled = false;
                uploadBtn.innerText = "Upload and Scan";
            }
            alert("Exception during scan: " + err.message);
        }
    }
});
</script>
</body>
"""

text = text.replace("</body>", logic)

{ith open('frontend/scan.html', 'w', encoding='utf-8') as f:
    f.write(text)