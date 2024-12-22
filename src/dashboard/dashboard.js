// Dashboard functionality
async function loadDashboardData() {
    try {
        const response = await fetch('/api/dashboard-data');
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error loading dashboard data:', error);
    }
}

function updateDashboard(data) {
    updateMetrics(data);
    updateAlerts(data.alerts);
    updateCharts(data);
}

function updateMetrics(data) {
    // Update POS metrics
    const posMetrics = document.getElementById('posMetrics');
    posMetrics.innerHTML = generateMetricsHTML(data.pos);

    // Update AI metrics
    const aiMetrics = document.getElementById('aiMetrics');
    aiMetrics.innerHTML = generateMetricsHTML(data.ai);

    // Update Blockchain metrics
    const blockchainMetrics = document.getElementById('blockchainMetrics');
    blockchainMetrics.innerHTML = generateMetricsHTML(data.blockchain);
}

function generateMetricsHTML(metrics) {
    return `
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Status</span>
            <span class="font-semibold ${metrics.status === 'healthy' ? 'text-green-500' : 'text-red-500'}">
                ${metrics.status}
            </span>
        </div>
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Open Issues</span>
            <span class="font-semibold">${metrics.openIssues}</span>
        </div>
        <div class="flex justify-between items-center">
            <span class="text-gray-600">Last Update</span>
            <span class="font-semibold">${metrics.lastUpdate}</span>
        </div>
    `;
}

function updateAlerts(alerts) {
    const alertsList = document.getElementById('alertsList');
    alertsList.innerHTML = alerts.map(alert => `
        <div class="flex items-center p-2 ${alert.severity === 'high' ? 'bg-red-100' : 'bg-yellow-100'} rounded">
            <div class="mr-2">
                ${alert.severity === 'high' ? '🔴' : '⚠️'}
            </div>
            <div>
                <div class="font-semibold">${alert.title}</div>
                <div class="text-sm text-gray-600">${alert.message}</div>
            </div>
        </div>
    `).join('');
}

function updateCharts(data) {
    // Activity Chart
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    new Chart(activityCtx, {
        type: 'line',
        data: {
            labels: data.activityData.labels,
            datasets: [{
                label: 'Commits',
                data: data.activityData.commits,
                borderColor: 'rgb(59, 130, 246)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true
        }
    });

    // Performance Chart
    const performanceCtx = document.getElementById('performanceChart').getContext('2d');
    new Chart(performanceCtx, {
        type: 'bar',
        data: {
            labels: data.performanceData.labels,
            datasets: [{
                label: 'Performance Score',
                data: data.performanceData.scores,
                backgroundColor: 'rgb(59, 130, 246)'
            }]
        },
        options: {
            responsive: true
        }
    });
}

// Load dashboard data every 5 minutes
loadDashboardData();
setInterval(loadDashboardData, 5 * 60 * 1000);