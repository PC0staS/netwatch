// Debug: Verificar que el archivo se carga
console.log('📄 Archivo app.js cargado correctamente');

class NetWatchWeb {
    constructor() {
        console.log('🏗️  Creando instancia NetWatchWeb');
        this.charts = {};
        this.monitoring = false;
        this.selectedInterfaces = [];
        this.pollingInterval = null;
        
        this.init();
    }
    
    init() {
        console.log('🔧 Inicializando NetWatch Web');
        this.setupEventListeners();
        this.loadInterfaces();
    }
    
    setupEventListeners() {
        document.getElementById('start-btn').addEventListener('click', () => {
            console.log('🟢 Monitoreo iniciado');
            this.startMonitoring();
        });
        
        document.getElementById('stop-btn').addEventListener('click', () => {
            this.stopMonitoring();
        });
    }
    
    async loadInterfaces() {
        console.log('📡 Cargando interfaces...');
        try {
            const response = await fetch('/api/interfaces');
            const interfaces = await response.json();
            console.log('✅ Interfaces cargadas:', interfaces);
            this.displayInterfaces(interfaces);
        } catch (error) {
            console.error('❌ Error al cargar interfaces:', error);
        }
    }
    
    displayInterfaces(interfaces) {
        console.log('🖥️  Mostrando interfaces:', interfaces);
        const container = document.getElementById('interfaces-list');
        container.innerHTML = '';
        
        interfaces.forEach(iface => {
            const item = document.createElement('div');
            item.className = 'interface-item';
            
            item.innerHTML = `
                <input type="checkbox" id="interface-${iface}" value="${iface}" class="form-check-input">
                <label for="interface-${iface}" class="form-check-label">
                    <span class="status-indicator status-inactive"></span>
                    <i class="bi bi-ethernet me-2"></i>
                    ${iface}
                </label>
            `;
            
            container.appendChild(item);
        });
        console.log('✅ Interfaces mostradas en la UI');
    }
    
    async startMonitoring() {
        const checkboxes = document.querySelectorAll('#interfaces-list input[type="checkbox"]:checked');
        this.selectedInterfaces = Array.from(checkboxes).map(cb => cb.value);
        
        console.log('🔄 Interfaces seleccionadas:', this.selectedInterfaces);
        
        if (this.selectedInterfaces.length === 0) {
            alert('Por favor selecciona al menos una interfaz');
            return;
        }
        
        try {
            // Iniciar monitoreo en el backend
            console.log('🚀 Iniciando monitoreo en el backend...');
            const response = await fetch('/api/start_monitoring', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    interfaces: this.selectedInterfaces
                })
            });
            
            if (!response.ok) {
                throw new Error(`Error al iniciar monitoreo: ${response.status}`);
            }
            
            const result = await response.json();
            console.log('✅ Monitoreo iniciado en el backend:', result);
            
            this.monitoring = true;
            console.log('🎯 Iniciando monitoreo en frontend');
            
            // Actualizar UI
            document.getElementById('start-btn').disabled = true;
            document.getElementById('stop-btn').disabled = false;
            
            // Crear contenedores para estadísticas
            this.createStatsContainers();
            
            // Iniciar polling
            this.startPolling();
            
        } catch (error) {
            console.error('❌ Error al iniciar monitoreo:', error);
            alert('Error al iniciar el monitoreo. Revisa la consola para más detalles.');
        }
    }
    
    async stopMonitoring() {
        this.monitoring = false;
        console.log('⏹️  Deteniendo monitoreo');
        
        try {
            // Detener monitoreo en el backend
            console.log('🛑 Deteniendo monitoreo en el backend...');
            const response = await fetch('/api/stop_monitoring', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                console.log('✅ Monitoreo detenido en el backend');
            } else {
                console.warn('⚠️ Error al detener monitoreo en el backend');
            }
        } catch (error) {
            console.error('❌ Error al detener monitoreo:', error);
        }
        
        // Detener polling
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
        
        // Actualizar UI
        document.getElementById('start-btn').disabled = false;
        document.getElementById('stop-btn').disabled = true;
        
        // Limpiar gráficos
        Object.values(this.charts).forEach(chart => chart.destroy());
        this.charts = {};
        
        // Limpiar contenedor de estadísticas
        document.getElementById('stats-container').innerHTML = '';
    }
    
    startPolling() {
        console.log('📡 Iniciando polling cada 2 segundos');
        this.pollingInterval = setInterval(() => {
            this.fetchStats();
        }, 2000);
        
        // Hacer la primera llamada inmediatamente
        this.fetchStats();
    }
    
    async fetchStats() {
        if (!this.monitoring) return;
        
        try {
            console.log('📊 Obteniendo estadísticas reales...');
            
            // Hacer petición real a la API
            const response = await fetch('/api/stats');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const realStats = await response.json();
            console.log('✅ Estadísticas reales recibidas:', realStats);
            
            // Verificar si hay datos disponibles
            if (Object.keys(realStats).length === 0) {
                console.warn('⚠️ No hay datos disponibles del servidor');
                this.showDisconnectedState();
                return;
            }
            
            // Filtrar solo las interfaces seleccionadas
            const filteredStats = {};
            let hasValidData = false;
            
            this.selectedInterfaces.forEach(iface => {
                if (realStats[iface]) {
                    filteredStats[iface] = realStats[iface];
                    hasValidData = true;
                } else {
                    console.warn(`⚠️ No se encontraron datos para la interfaz: ${iface}`);
                }
            });
            
            if (!hasValidData) {
                console.warn('⚠️ No hay datos válidos para las interfaces seleccionadas');
                this.showDisconnectedState();
                return;
            }
            
            // Actualizar UI con datos reales
            this.updateStats(filteredStats);
            
        } catch (error) {
            console.error('❌ Error al obtener estadísticas:', error);
            this.showDisconnectedState();
        }
    }
    
    showDisconnectedState() {
        console.log('🔴 Mostrando estado desconectado');
        const container = document.getElementById('stats-container');
        container.innerHTML = `
            <div class="connection-status disconnected">
                <i class="bi bi-wifi-off"></i>
                <span>Desconectado - No hay datos disponibles</span>
            </div>
            <div class="no-data">
                <div class="no-data-icon">
                    <i class="bi bi-router"></i>
                </div>
                <div class="no-data-message">Sin conexión al monitor de red</div>
                <div class="no-data-subtitle">Verifica la conexión y el estado del servicio</div>
            </div>
        `;
    }
    
    createStatsContainers() {
        const container = document.getElementById('stats-container');
        container.innerHTML = '';
        const n = this.selectedInterfaces.length;
        let gridClass = 'stats-grid';
        if (n <= 2) gridClass += ' few';
        else if (n <= 4) gridClass += ' medium';
        else gridClass += ' many';

        // Crear el grid
        const grid = document.createElement('div');
        grid.className = gridClass;

        this.selectedInterfaces.forEach(iface => {
            const statsDiv = document.createElement('div');
            statsDiv.className = 'stat-card';
            statsDiv.innerHTML = `
                <h3 class="card-title mb-3">
                    <i class="bi bi-router"></i> ${iface}
                </h3>
                <div class="row g-2 mb-2">
                    <div class="col-6">
                        <div class="stat-value" id="sent-speed-${iface}">0 B/s</div>
                        <div class="stat-label"><i class="bi bi-arrow-up-circle"></i> Sent Speed</div>
                    </div>
                    <div class="col-6">
                        <div class="stat-value" id="recv-speed-${iface}">0 B/s</div>
                        <div class="stat-label"><i class="bi bi-arrow-down-circle"></i> Recv Speed</div>
                    </div>
                    <div class="col-6">
                        <div class="stat-value" id="sent-total-${iface}">0 B</div>
                        <div class="stat-label"><i class="bi bi-bar-chart-line"></i> Total Sent</div>
                    </div>
                    <div class="col-6">
                        <div class="stat-value" id="recv-total-${iface}">0 B</div>
                        <div class="stat-label"><i class="bi bi-bar-chart-line"></i> Total Recv</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="chart-${iface}"></canvas>
                </div>
            `;
            grid.appendChild(statsDiv);
        });
        container.appendChild(grid);
        
        // Create charts after DOM is fully updated
        setTimeout(() => {
            this.selectedInterfaces.forEach(iface => {
                this.createChart(iface);
            });
        }, 100);
    }
    
    createChart(iface) {
        const canvas = document.getElementById(`chart-${iface}`);
        if (!canvas) {
            console.error(`Canvas element for interface '${iface}' not found. Chart will not be created.`);
            return;
        }
        
        console.log(`Creating chart for interface: ${iface}`);
        const ctx = canvas.getContext('2d');
        
        // Destroy existing chart if it exists
        if (this.charts[iface]) {
            this.charts[iface].destroy();
        }
        
        this.charts[iface] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: 60}, (_, i) => i + 1),
                datasets: [
                    {
                        label: 'Enviado',
                        data: new Array(60).fill(0),
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.4
                    },
                    {
                        label: 'Recibido',
                        data: new Array(60).fill(0),
                        borderColor: '#f093fb',
                        backgroundColor: 'rgba(240, 147, 251, 0.1)',
                        fill: true,
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return formatBytes(value) + '/s';
                            }
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Tiempo (segundos)'
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: `Tráfico de Red - ${iface}`
                    },
                    legend: {
                        display: true,
                        position: 'top'
                    }
                }
            }
        });
    }
    
    updateStats(stats) {
        Object.keys(stats).forEach(iface => {
            const data = stats[iface];
            
            // Actualizar valores numéricos
            document.getElementById(`sent-speed-${iface}`).textContent = formatBytes(data.sent_speed) + '/s';
            document.getElementById(`recv-speed-${iface}`).textContent = formatBytes(data.recv_speed) + '/s';
            document.getElementById(`sent-total-${iface}`).textContent = formatBytes(data.sent_total);
            document.getElementById(`recv-total-${iface}`).textContent = formatBytes(data.recv_total);
            
            // Actualizar gráfico
            if (this.charts[iface]) {
                const chart = this.charts[iface];
                chart.data.datasets[0].data = data.sent_history.slice(-60);
                chart.data.datasets[1].data = data.recv_history.slice(-60);
                chart.update('none');
            }
        });
    }
    
    updateStatusIndicators() {
        const indicators = document.querySelectorAll('.status-indicator');
        indicators.forEach(indicator => {
            const iface = indicator.parentElement.textContent.trim();
            if (this.monitoring && this.selectedInterfaces.includes(iface)) {
                indicator.className = 'status-indicator status-active';
            } else {
                indicator.className = 'status-indicator status-inactive';
            }
        });
    }
}

// Función auxiliar para formatear bytes
function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Inicializar la aplicación
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM cargado, iniciando NetWatch Web App');
    try {
        const app = new NetWatchWeb();
        console.log('✅ NetWatch Web App iniciada correctamente');
    } catch (error) {
        console.error('❌ Error al inicializar NetWatch Web App:', error);
    }
});
