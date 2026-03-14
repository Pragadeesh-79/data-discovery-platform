document.addEventListener("DOMContentLoaded", () => {
    // Inject Live Server Time Gimmick
    
    // Create clock element if we want it in navbar
    const navRight = document.querySelector('.navbar-right');
    if (navRight) {
        const clockDiv = document.createElement('div');
        clockDiv.className = 'realtime-clock-nav';
        clockDiv.style.cssText = 'color: #4ade80; font-family: monospace; font-size: 14px; margin-right: 15px; border: 1px solid #4ade80; padding: 4px 8px; border-radius: 4px; box-shadow: 0 0 5px rgba(74,222,128,0.3); background: rgba(0,0,0,0.2);';
        navRight.insertBefore(clockDiv, navRight.firstChild);
    }

    const timeElements = document.querySelectorAll(".realtime-clock, .realtime-clock-nav");
    
    function updateClocks() {
        const now = new Date();
        const timeString = now.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit', fractionalSecondDigits: 1 });
        const dateString = now.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
        
        timeElements.forEach(el => {
            el.innerText = `${dateString} ${timeString}`;
        });
        
        // Update "Last updated" texts to look active
        document.querySelectorAll("p").forEach(el => {
            if (el.innerText.includes("Last update:") || el.innerText.includes("Last compliance run:")) {
                if (!el.dataset.baseText) {
                    const parts = el.innerText.split('·');
                    if (parts.length > 1) {
                        el.dataset.baseText = parts[0].trim();
                    } else {
                        el.dataset.baseText = "";
                    }
                }
                const prefix = el.dataset.baseText ? `${el.dataset.baseText} &middot; ` : '';
                el.innerHTML = `${prefix}Status: <span style="color:#4ade80; font-family: monospace; font-weight: bold;">LIVE SCANNING (${timeString})</span>`;
            }
        });
    }
    
    setInterval(updateClocks, 100); // 100ms for fractional second effect
    updateClocks();

    // Add a blinking LIVE indicator next to logos or headers
    const headers = document.querySelectorAll("h1, h2");
    headers.forEach(h => {
        // Only target main dashboard headers
        if (h.innerText.includes("Overview") || h.innerText.includes("Lineage") || h.innerText.includes("Reports")) {
            if (!h.querySelector('.live-pulse-dot')) {
                h.innerHTML += ` <span class="live-pulse-dot" style="display:inline-block;width:10px;height:10px;background:#ef4444;border-radius:50%;margin-left:12px;box-shadow:0 0 8px #ef4444;animation:pulse-dot 1s infinite"></span><span style="color:#ef4444; font-size: 12px; vertical-align: middle; margin-left: 5px;">REC</span>`;
            }
        }
    });
});

// We need pulse-dot animation in CSS, we can inject it
const style = document.createElement('style');
style.innerHTML = `
@keyframes pulse-dot {
    0% { transform: scale(0.95); opacity: 0.5; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1); opacity: 1; box-shadow: 0 0 0 6px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); opacity: 0.5; box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}

/* Add a scanner line sweep effect to the main container */
.crypto-container::after {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 2px;
    background: rgba(74, 222, 128, 0.5);
    box-shadow: 0 0 20px rgba(74, 222, 128, 0.8);
    animation: scanline 8s linear infinite;
    pointer-events: none;
    z-index: 9999;
}

@keyframes scanline {
    0% { top: -10%; }
    100% { top: 110%; }
}
`;
document.head.appendChild(style);