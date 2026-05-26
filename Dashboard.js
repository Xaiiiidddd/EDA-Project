document.addEventListener('DOMContentLoaded', () => {
 
    if (typeof DATA_SUMMARY === 'undefined') {
        showErrorState("Data Summary file (data_summary.js) could not be loaded. Please run 'python run_project.py' first to generate statistics.");
        return;
    }
    const data = DATA_SUMMARY;
 
    initNavigation();
    populateKPIs(data.kpis, data.metadata);
    initCharts(data);
    populateBreakdowns(data.breakdowns);
    populateCorrelationGrid(data.correlation);
    populateDataTable(data.samples);
    initFiltersAndSearch(data.samples);
});

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const tabPanes = document.querySelectorAll('.tab-pane');
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const targetTab = item.getAttribute('data-tab');
            // Toggle Nav Active state
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');
            // Toggle Tab Pane Visibility
            tabPanes.forEach(pane => {
                pane.classList.remove('active');
                if (pane.id === `tab-${targetTab}`) {
                    pane.classList.add('active');
                }
            });
        });
    });
}

function populateKPIs(kpis, metadata) {
    document.getElementById('analysis-time').innerText = `Generated: ${metadata.generated_at}`;
    
   
    animateNumber('kpi-customers', 0, kpis.total_customers, 0, '');
    animateNumber('kpi-revenue', 0, kpis.total_revenue, 2, '$');
    animateNumber('kpi-spend', 0, kpis.avg_spend, 2, '$');
    animateNumber('kpi-churn', 0, kpis.churn_rate, 2, '', '%');
    animateNumber('kpi-rating', 0, kpis.avg_rating, 1, '', ' / 5');
}

function animateNumber(elementId, start, end, decimals, prefix = '', suffix = '') {
    const obj = document.getElementById(elementId);
    if (!obj) return;
    
    let localStart = start;
    const duration = 800; // ms
    const stepTime = 15;
    const steps = Math.ceil(duration / stepTime);
    const stepIncrement = (end - start) / steps;
    let currentStep = 0;
    const timer = setInterval(() => {
        currentStep++;
        localStart += stepIncrement;
        
        if (currentStep >= steps) {
            clearInterval(timer);
            obj.innerText = prefix + end.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
        } else {
            obj.innerText = prefix + localStart.toLocaleString(undefined, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }) + suffix;
        }
    }, stepTime);
}

let charts = {};
function initCharts(data) {

    const gridColor = 'rgba(255, 255, 255, 0.05)';
    const textColor = '#9ca3af';
    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } }
            }
        },
        scales: {
            x: {
                grid: { color: gridColor },
                ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
            },
            y: {
                grid: { color: gridColor },
                ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
            }
        }
    };

    const ctxAge = document.getElementById('ageDistributionChart').getContext('2d');
    charts.age = new Chart(ctxAge, {
        type: 'bar',
        data: {
            labels: data.distributions.age.labels,
            datasets: [{
                label: 'Customer Count',
                data: data.distributions.age.values,
                backgroundColor: 'rgba(99, 102, 241, 0.7)',
                borderColor: '#6366f1',
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: chartOptions
    });
  
    const ctxSpend = document.getElementById('spendDistributionChart').getContext('2d');
    charts.spend = new Chart(ctxSpend, {
        type: 'bar',
        data: {
            labels: data.distributions.spend.labels,
            datasets: [{
                label: 'Frequency',
                data: data.distributions.spend.values,
                backgroundColor: 'rgba(20, 184, 166, 0.7)',
                borderColor: '#14b8a6',
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: chartOptions
    });

    const membershipLabels = ['Bronze', 'Silver', 'Gold', 'Premium'];
    const membershipSpends = membershipLabels.map(label => data.breakdowns.membership[label].Avg_Spend);
    const ctxTier = document.getElementById('tierSpendChart').getContext('2d');
    charts.tier = new Chart(ctxTier, {
        type: 'bar',
        data: {
            labels: membershipLabels,
            datasets: [{
                label: 'Average Spend ($)',
                data: membershipSpends,
                backgroundColor: [
                    'rgba(245, 158, 11, 0.7)',  // Bronze - amber
                    'rgba(156, 163, 175, 0.7)', // Silver - gray
                    'rgba(217, 119, 6, 0.7)',   // Gold - dark gold
                    'rgba(139, 92, 246, 0.7)'   // Premium - violet
                ],
                borderColor: ['#f59e0b', '#9ca3af', '#d97706', '#8b5cf6'],
                borderWidth: 1.5,
                borderRadius: 6
            }]
        },
        options: chartOptions
    });
   
    const catLabels = Object.keys(data.breakdowns.category);
    const catCounts = catLabels.map(label => data.breakdowns.category[label].Count);
    const ctxCat = document.getElementById('categoryDistributionChart').getContext('2d');
    charts.category = new Chart(ctxCat, {
        type: 'doughnut',
        data: {
            labels: catLabels,
            datasets: [{
                data: catCounts,
                backgroundColor: [
                    'rgba(99, 102, 241, 0.65)',
                    'rgba(236, 72, 153, 0.65)',
                    'rgba(20, 184, 166, 0.65)',
                    'rgba(245, 158, 11, 0.65)',
                    'rgba(16, 185, 129, 0.65)'
                ],
                borderColor: ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#10b981'],
                borderWidth: 1.5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 10 } }
                }
            }
        }
    });
  
    const regionLabels = Object.keys(data.breakdowns.location);
    const regionChurnRates = regionLabels.map(label => data.breakdowns.location[label].Churn_Rate * 100);
    const ctxRegion = document.getElementById('regionChurnChart').getContext('2d');
    charts.region = new Chart(ctxRegion, {
        type: 'bar',
        data: {
            labels: regionLabels,
            datasets: [{
                label: 'Churn Rate (%)',
                data: regionChurnRates,
                backgroundColor: 'rgba(244, 63, 94, 0.7)',
                borderColor: '#f43f5e',
                borderWidth: 1.5,
                borderRadius: 4
            }]
        },
        options: {
            indexAxis: 'y',
            ...chartOptions
        }
    });
}

function populateBreakdowns(breakdowns) {
    const tbody = document.querySelector('#breakdown-summary-table tbody');
    tbody.innerHTML = '';
    const sections = [
        { label: 'Membership Tier', data: breakdowns.membership },
        { label: 'Region', data: breakdowns.location },
        { label: 'Preferred Category', data: breakdowns.category },
        { label: 'Age Cohort', data: breakdowns.age_group }
    ];
    sections.forEach(section => {
        let first = true;
        const keys = Object.keys(section.data);
        keys.forEach(key => {
            const item = section.data[key];
            const tr = document.createElement('tr');
            
            if (first) {
                const tdLabel = document.createElement('td');
                tdLabel.innerText = section.label;
                tdLabel.rowSpan = keys.length;
                tdLabel.style.fontWeight = '600';
                tdLabel.style.color = 'var(--color-indigo)';
                tr.appendChild(tdLabel);
                first = false;
            }
            tr.innerHTML += `
                <td><strong>${key}</strong></td>
                <td>${item.Count.toLocaleString()}</td>
                <td>$${item.Avg_Spend.toFixed(2)}</td>
                <td><span class="badge ${item.Churn_Rate > 0.3 ? 'churned' : 'active'}">${(item.Churn_Rate * 100).toFixed(1)}%</span></td>
            `;
            tbody.appendChild(tr);
        });
    });
}
function populateCorrelationGrid(corr) {
    const gridContainer = document.getElementById('correlation-matrix-grid');
    gridContainer.innerHTML = '';
    const variables = Object.keys(corr);
    const size = variables.length;
   
    gridContainer.style.gridTemplateColumns = `repeat(${size + 1}, 1fr)`;
 
    const corner = document.createElement('div');
    corner.className = 'matrix-header-label';
    corner.innerText = '';
    gridContainer.appendChild(corner);
 
    variables.forEach(v => {
        const header = document.createElement('div');
        header.className = 'matrix-header-label';
        header.innerText = shortenLabel(v);
        gridContainer.appendChild(header);
    });
  
    variables.forEach(rowVar => {
     
        const rowHeader = document.createElement('div');
        rowHeader.className = 'matrix-header-label';
        rowHeader.style.justifyContent = 'flex-end';
        rowHeader.style.paddingRight = '8px';
        rowHeader.innerText = shortenLabel(rowVar);
        gridContainer.appendChild(rowHeader);
     
        variables.forEach(colVar => {
            const val = corr[rowVar][colVar];
            const cell = document.createElement('div');
            cell.className = 'matrix-cell';
            
      
            cell.style.backgroundColor = getCorrColor(val);
            cell.innerHTML = `
                <span class="matrix-cell-val" style="color: ${Math.abs(val) > 0.45 ? '#ffffff' : 'var(--text-primary)'}">${val >= 0 ? '+' : ''}${val.toFixed(2)}</span>
                <span class="matrix-cell-label">${shortenLabel(rowVar)} vs ${shortenLabel(colVar)}</span>
            `;
            gridContainer.appendChild(cell);
        });
    });
}

function getCorrColor(val) {
  
    if (val >= 0) {
    
        const factor = val; // 0 to 1
        const r = Math.round(31 + (99 - 31) * factor);
        const g = Math.round(41 + (102 - 41) * factor);
        const b = Math.round(55 + (241 - 55) * factor);
        return `rgb(${r}, ${g}, ${b})`;
    } 
 
    else {
        const factor = Math.abs(val); // 0 to 1
        const r = Math.round(31 + (244 - 31) * factor);
        const g = Math.round(41 + (63 - 41) * factor);
        const b = Math.round(55 + (94 - 55) * factor);
        return `rgb(${r}, ${g}, ${b})`;
    }
}

function shortenLabel(label) {
    const mapping = {
        'Total_Spend_Cleaned': 'Spend',
        'Items_Purchased': 'Items',
        'Average_Rating': 'Rating',
        'Discount_Applied': 'Discount',
        'Churn_Status': 'Churn',
        'Age': 'Age'
    };
    return mapping[label] || label;
}

function populateDataTable(samples) {
    const tbody = document.querySelector('#sample-data-table tbody');
    tbody.innerHTML = '';
    samples.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${row.Customer_ID}</strong></td>
            <td>${typeof row.Age === 'number' ? row.Age.toFixed(0) : row.Age}</td>
            <td>${row.Gender}</td>
            <td>${row.Location}</td>
            <td>${row.Membership_Level}</td>
            <td>$${row.Total_Spend_Cleaned.toFixed(2)}</td>
            <td>${row.Average_Rating.toFixed(1)}</td>
            <td>${row.Purchase_Frequency}</td>
            <td>${row.Preferred_Category}</td>
            <td><span style="font-family: monospace;">${row.Last_Purchase_Date}</span></td>
            <td><span class="badge ${row.Churn_Status === 1 ? 'churned' : 'active'}">${row.Churn_Status === 1 ? 'Churned' : 'Retained'}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function initFiltersAndSearch(samples) {
    const searchInput = document.getElementById('table-search');
    const tierFilter = document.getElementById('membership-filter');
    const updateTable = () => {
        const searchValue = searchInput.value.toLowerCase().strip ? searchInput.value.toLowerCase().trim() : searchInput.value.toLowerCase();
        const selectedTier = tierFilter.value;
        const filteredSamples = samples.filter(row => {
          
            const matchesTier = selectedTier === 'ALL' || row.Membership_Level === selectedTier;
           
            const matchesSearch = 
                row.Customer_ID.toLowerCase().includes(searchValue) ||
                row.Location.toLowerCase().includes(searchValue) ||
                row.Preferred_Category.toLowerCase().includes(searchValue) ||
                row.Purchase_Frequency.toLowerCase().includes(searchValue);
                
            return matchesTier && matchesSearch;
        });
        populateDataTable(filteredSamples);
    };
    searchInput.addEventListener('input', updateTable);
    tierFilter.addEventListener('change', updateTable);
}

function showErrorState(message) {
    const main = document.querySelector('.main-content');
    main.innerHTML = `
        <div style="background-color: rgba(244, 63, 94, 0.1); border: 1px solid var(--color-rose); border-radius: 12px; padding: 40px; text-align: center; margin-top: 50px;">
            <i class="fa-solid fa-triangle-exclamation" style="font-size: 3rem; color: var(--color-rose); margin-bottom: 20px;"></i>
            <h2 style="margin-bottom: 10px;">Environment Warning</h2>
            <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 20px auto; line-height: 1.6;">${message}</p>
        </div>
    `;
}
