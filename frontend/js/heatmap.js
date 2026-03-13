document.addEventListener("DOMContentLoaded", () => {
    // Expected structure from API: 
    // { "hr": { "Aadhaar": 3, "PAN": 2 }, "finance": { "PAN": 4 } }
    
    const API_URL = "http://localhost:8000/reports/heatmap";

    fetchHeatmapData();

    function fetchHeatmapData() {
        showLoading(true);
        
        fetch(API_URL)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                showLoading(false);
                renderHeatmap(data);
            })
            .catch(error => {
                console.error("Error fetching heatmap data:", error);
                showLoading(false);
                showError(true);
            });
    }

    function showLoading(isLoading) {
        const spinner = document.getElementById("loadingSpinner");
        const chartContainer = document.getElementById("chartContainer");
        
        if (isLoading) {
            spinner.classList.remove("d-none");
            chartContainer.classList.add("d-none");
        } else {
            spinner.classList.add("d-none");
            chartContainer.classList.remove("d-none");
        }
    }

    function showError(isError) {
        const alert = document.getElementById("errorAlert");
        const chartContainer = document.getElementById("chartContainer");
        
        if (isError) {
            alert.classList.remove("d-none");
            chartContainer.classList.add("d-none");
        } else {
            alert.classList.add("d-none");
        }
    }

    function renderHeatmap(data) {
        const ctx = document.getElementById("heatmapChart").getContext("2d");
        
        // 1. Extract and sort unique sources (Y-axis)
        const sources = Object.keys(data).sort();
        
        // 2. Extract and sort unique entity types (X-axis)
        const entityTypesSet = new Set();
        sources.forEach(source => {
            Object.keys(data[source]).forEach(type => entityTypesSet.add(type));
        });
        const entityTypes = Array.from(entityTypesSet).sort();
        
        // 3. Transform data for chartjs-chart-matrix
        // Matrix expects data in format: [{x: 'Aadhaar', y: 'hr', v: 3}, ...]
        const matrixData = [];
        let maxCount = 0;
        
        sources.forEach(source => {
            entityTypes.forEach(type => {
                const count = data[source][type] || 0;
                if (count > maxCount) maxCount = count;
                
                matrixData.push({
                    x: type,
                    y: source,
                    v: count
                });
            });
        });

        // 4. Define Color Scale based on intensity
        const getColor = (value) => {
            if (value === 0) return 'rgba(30, 41, 59, 1)'; // Match card background (#1e293b)
            
            // Normalize value between 0.1 and 1.0 (prevent being too invisible if > 0)
            const normalized = maxCount > 0 ? value / maxCount : 0;
            const alpha = 0.2 + (0.8 * normalized);
            
            // Green for low (1-2), Orange for medium (3-5), Red for high (>5)
            // Or gradient based on relative normalized value
            if (normalized < 0.33) {
                // Return a nice green: #10b981
                return `rgba(16, 185, 129, ${Math.max(0.4, alpha)})`;
            } else if (normalized < 0.66) {
                // Return orange: #f59e0b
                return `rgba(245, 158, 11, ${alpha + 0.1})`; 
            } else {
                // Return red: #ef4444
                return `rgba(239, 68, 68, ${alpha})`;
            }
        };

        // 5. Render Chart
        new Chart(ctx, {
            type: 'matrix',
            data: {
                datasets: [{
                    label: 'Sensitive Data Highlights',
                    data: matrixData,
                    backgroundColor: (ctx) => {
                        const value = ctx.dataset.data[ctx.dataIndex].v;
                        return getColor(value);
                    },
                    borderColor: '#334155', // Border to separate cells clearly
                    borderWidth: 1,
                    width: (ctx) => {
                        const chartArea = ctx.chart.chartArea;
                        if (!chartArea) return 0;
                        return (chartArea.right - chartArea.left) / entityTypes.length - 2;
                    },
                    height: (ctx) => {
                        const chartArea = ctx.chart.chartArea;
                        if (!chartArea) return 0;
                        return (chartArea.bottom - chartArea.top) / sources.length - 2;
                    }
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: () => '', // Disable top title array
                            label: (context) => {
                                const v = context.raw;
                                return `${v.y} » ${v.x}: ${v.v} items`;
                            }
                        },
                        displayColors: false, // Don't show color box in tooltip
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleFont: { size: 14, family: 'Inter' },
                        bodyFont: { size: 14, family: 'Inter' },
                        padding: 12
                    },
                    legend: {
                        display: false // We use our custom HTML legend instead
                    }
                },
                scales: {
                    x: {
                        type: 'category',
                        labels: entityTypes,
                        ticks: {
                            display: true,
                            color: '#e2e8f0',
                            font: { family: 'Inter', size: 13 }
                        },
                        grid: { display: false },
                        border: { display: false }
                    },
                    y: {
                        type: 'category',
                        labels: sources,
                        offset: true,
                        ticks: {
                            display: true,
                            color: '#e2e8f0',
                            font: { family: 'Inter', size: 13 }
                        },
                        grid: { display: false },
                        border: { display: false }
                    }
                }
            }
        });
    }
});
