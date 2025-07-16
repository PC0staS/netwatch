"""
Web Interface for NetWatch - Network Monitor
"""

import os
import json
import time
from collections import deque
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from threading import Thread
import psutil

# Manejo de importaciones relativas y absolutas
try:
    from .monitor import NetworkMonitor
except ImportError:
    from monitor import NetworkMonitor

class WebInterface:
    def __init__(self, monitor):
        self.monitor = monitor
        self.app = Flask(__name__, 
                        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
                        static_folder=os.path.join(os.path.dirname(__file__), 'static'))
        self.app.config['SECRET_KEY'] = 'netwatch-secret-key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        self.running = False
        self.setup_routes()
        
    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')
        
        @self.app.route('/api/interfaces')
        def get_interfaces():
            interfaces = self.monitor.get_available_interfaces()
            return jsonify(interfaces)
        
        @self.app.route('/api/stats')
        def get_stats():
            stats = {}
            for interface in self.monitor.selected_interfaces:
                if interface in self.monitor.interface_data:
                    data = self.monitor.interface_data[interface]
                    stats[interface] = {
                        'sent_speed': data['sent_history'][-1] if data['sent_history'] else 0,
                        'recv_speed': data['recv_history'][-1] if data['recv_history'] else 0,
                        'sent_total': data['sent_total'] if 'sent_total' in data else 0,
                        'recv_total': data['recv_total'] if 'recv_total' in data else 0,
                        'sent_history': list(data['sent_history']),
                        'recv_history': list(data['recv_history'])
                    }
            return jsonify(stats)
        
        @self.app.route('/api/start_monitoring', methods=['POST'])
        def start_monitoring_api():
            try:
                data = request.get_json()
                interfaces = data.get('interfaces', [])
                
                print(f"🔄 API: Iniciando monitoreo para interfaces: {interfaces}")
                
                if interfaces:
                    self.monitor.selected_interfaces = interfaces
                    # Inicializar datos para las interfaces seleccionadas
                    for interface in interfaces:
                        if interface not in self.monitor.interface_data:
                            self.monitor.interface_data[interface] = {
                                'sent_history': deque(maxlen=60),
                                'recv_history': deque(maxlen=60),
                                'sent_total': 0,
                                'recv_total': 0,
                                'last_sent': 0,
                                'last_recv': 0
                            }
                            print(f"✅ Inicializado datos para {interface}")
                    
                    if not self.running:
                        self.start_monitoring()
                        print("🚀 Monitoreo iniciado desde API")
                    
                    return jsonify({'success': True, 'message': 'Monitoreo iniciado', 'interfaces': interfaces})
                else:
                    return jsonify({'success': False, 'message': 'No se proporcionaron interfaces'}), 400
                    
            except Exception as e:
                print(f"❌ Error en start_monitoring_api: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/stop_monitoring', methods=['POST'])
        def stop_monitoring_api():
            try:
                print("🛑 API: Deteniendo monitoreo...")
                self.running = False
                self.monitor.selected_interfaces = []
                return jsonify({'success': True, 'message': 'Monitoreo detenido'})
            except Exception as e:
                print(f"❌ Error en stop_monitoring_api: {e}")
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.socketio.on('connect')
        def handle_connect():
            print('🌐 Cliente conectado a la interfaz web')
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            print('🌐 Cliente desconectado de la interfaz web')
            
        @self.socketio.on('start_monitoring')
        def handle_start_monitoring(data):
            interfaces = data.get('interfaces', [])
            print(f"🔄 Iniciando monitoreo para interfaces: {interfaces}")
            if interfaces:
                self.monitor.selected_interfaces = interfaces
                # Inicializar datos para las interfaces seleccionadas
                for interface in interfaces:
                    if interface not in self.monitor.interface_data:
                        self.monitor.interface_data[interface] = {
                            'sent_history': deque(maxlen=60),
                            'recv_history': deque(maxlen=60),
                            'sent_total': 0,
                            'recv_total': 0,
                            'last_sent': 0,
                            'last_recv': 0
                        }
                        print(f"✅ Inicializado datos para {interface}")
                if not self.running:
                    self.start_monitoring()
                    print("🚀 Monitoreo iniciado")
                    
        @self.socketio.on('stop_monitoring')
        def handle_stop_monitoring():
            self.running = False
    
    def start_monitoring(self):
        self.running = True
        thread = Thread(target=self.monitoring_loop)
        thread.daemon = True
        thread.start()
    
    def monitoring_loop(self):
        print("🔄 Iniciando bucle de monitoreo...")
        while self.running:
            try:
                self.monitor.update_data()
                stats = {}
                for interface in self.monitor.selected_interfaces:
                    if interface in self.monitor.interface_data:
                        data = self.monitor.interface_data[interface]
                        stats[interface] = {
                            'sent_speed': data['sent_history'][-1] if data['sent_history'] else 0,
                            'recv_speed': data['recv_history'][-1] if data['recv_history'] else 0,
                            'sent_total': data['sent_total'] if 'sent_total' in data else 0,
                            'recv_total': data['recv_total'] if 'recv_total' in data else 0,
                            'sent_history': list(data['sent_history']),
                            'recv_history': list(data['recv_history'])
                        }
                
                if stats:
                    print(f"📊 Enviando estadísticas: {len(stats)} interfaces")
                    self.socketio.emit('stats_update', stats)
                else:
                    print("⚠️  No hay estadísticas para enviar")
                
                time.sleep(1)
            except Exception as e:
                print(f"❌ Error en bucle de monitoreo: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(1)
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        print(f"🌐 Iniciando interfaz web en http://{host}:{port}")
        
        # Mostrar información adicional para acceso de red
        if host == '0.0.0.0':
            import socket
            try:
                # Obtener IP local
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                print(f"🌐 Acceso local: http://localhost:{port}")
                print(f"🌐 Acceso desde red local: http://{local_ip}:{port}")
                print(f"🌐 Acceso desde cualquier dispositivo en la red: http://{local_ip}:{port}")
            except Exception:
                print(f"🌐 Acceso desde red local: http://[IP_LOCAL]:{port}")
        else:
            print(f"🌐 Solo acceso local: http://localhost:{port}")
        
        print("🔥 Presiona Ctrl+C para detener el servidor")
        
        # Silenciar warning de desarrollo
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        # Configuración especial para Linux/systemd para evitar error de Werkzeug
        import sys
        import os
        
        # Detectar si estamos en un entorno tipo producción (Linux con host 0.0.0.0)
        is_production_like = (
            sys.platform.startswith('linux') and 
            host == '0.0.0.0'
        )
        
        if is_production_like:
            # Para Linux en modo red, usar configuración que evite el error de Werkzeug
            os.environ['WERKZEUG_RUN_MAIN'] = 'true'
            debug = False
        
        # Ejecutar con allow_unsafe_werkzeug para versiones nuevas de Werkzeug
        try:
            self.socketio.run(
                self.app, 
                host=host, 
                port=port, 
                debug=debug, 
                use_reloader=False,
                allow_unsafe_werkzeug=True
            )
        except TypeError:
            # Fallback para versiones más antiguas de socketio que no soportan allow_unsafe_werkzeug
            self.socketio.run(self.app, host=host, port=port, debug=debug, use_reloader=False)

if __name__ == '__main__':
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from monitor import NetworkMonitor
    
    monitor = NetworkMonitor()
    web_interface = WebInterface(monitor)
    web_interface.run(debug=True)

def main():
    """Entry point for console script"""
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from monitor import NetworkMonitor
    
    monitor = NetworkMonitor()
    web_interface = WebInterface(monitor)
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='NetWatch Web Interface')
    parser.add_argument('--host', default='127.0.0.1', help='Host to bind to (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000, help='Port to bind to (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print(f"🌐 Iniciando NetWatch Web Interface...")
    print(f"🔗 URL: http://{args.host}:{args.port}")
    print(f"🔧 Debug: {args.debug}")
    
    web_interface.run(host=args.host, port=args.port, debug=args.debug)
