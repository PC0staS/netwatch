"""
Command Line Interface for NetWatch
"""

import argparse
import sys
from .monitor import NetworkMonitor, Colors

def get_version():
    """Get the version from setup.py"""
    try:
        # Try to get version from package metadata (Python 3.8+)
        from importlib.metadata import version
        return version('netwatch-monitor')
    except ImportError:
        # Fallback for older Python versions
        try:
            import pkg_resources
            return pkg_resources.get_distribution('netwatch-monitor').version
        except ImportError:
            return "1.1.0"  # Fallback version

def web_main():
    """Entry point for web interface"""
    parser = argparse.ArgumentParser(
        prog='netwatch-web',
        description='🌐 NetWatch - Web Interface for Network Monitoring',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
🌐 NETWORK ACCESS MODES:
  localhost only    : netwatch-web (default - only accessible from this computer)
  network access    : netwatch-web --network (accessible from other devices on your network)
  
📱 COMMON USAGE EXAMPLES:
  netwatch-web                          # Start on localhost:5000 (local access only)
  netwatch-web --network                # Enable network access (accessible from phones/tablets)
  netwatch-web --network --port 8080    # Network access on custom port 8080
  netwatch-web --host 0.0.0.0           # Same as --network (explicit host setting)
  
🔧 ADVANCED OPTIONS:
  netwatch-web --debug                  # Enable debug mode for development
  netwatch-web --network --debug        # Network access with debug information
  
📞 ACCESS INFORMATION:
  • localhost only: http://localhost:5000 (only this computer can access)
  • network access: http://192.168.1.x:5000 (any device on your network can access)
  • The tool will show you the exact URLs when it starts
'''
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1 for localhost only, use 0.0.0.0 for network access)'
    )
    
    parser.add_argument(
        '--network', '-n',
        action='store_true',
        help='Enable network access (allows access from other devices on your network)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=5000,
        help='Port to run the web server on (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode for development (shows detailed error messages)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'netwatch-web {get_version()}'
    )
    
    args = parser.parse_args()
    
    try:
        monitor = NetworkMonitor()
        
        # Check if network access is requested
        host = args.host
        if args.network:
            host = '0.0.0.0'
            print(f"{Colors.CYAN}🌐 Acceso de red habilitado - Accesible desde toda la red local{Colors.RESET}")
        
        print(f"{Colors.GREEN}🌐 Iniciando NetWatch Web Interface...{Colors.RESET}")
        
        try:
            from .web import WebInterface
            web_interface = WebInterface(monitor)
            web_interface.run(host=host, port=args.port, debug=args.debug)
        except ImportError as e:
            print(f"{Colors.RED}❌ Error: Flask no está instalado. Instala con: pip install flask flask-socketio{Colors.RESET}")
            print(f"{Colors.YELLOW}💡 O reinstala el paquete: pip install --upgrade netwatch-monitor{Colors.RESET}")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 ¡Hasta luego!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error inesperado: {e}{Colors.RESET}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='netwatch',
        description='🌐 NetWatch - A beautiful network monitoring tool with console and web interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
🖥️ CONSOLE MODE (default):
  netwatch              # Interactive interface selection
  netwatch --all        # Monitor all interfaces
  netwatch -i eth0      # Monitor specific interface
  
🌐 WEB INTERFACE MODE:
  netwatch --web        # Start web interface (localhost only)
  netwatch --web --network  # Enable network access (phones/tablets)
  netwatch --web --network --port 8080  # Network access on port 8080
  
📱 NETWORK ACCESS EXAMPLES:
  Local only  : netwatch --web
  Network     : netwatch --web --network
  Custom port : netwatch --web --network --port 8080
  Debug mode  : netwatch --web --network --debug
  
ℹ️ INFORMATION:
  netwatch --version    # Show version
  netwatch --help       # Show this help message
  
📞 When using --web --network, the tool will show you the exact URLs for:
  • Local access: http://localhost:5000
  • Network access: http://192.168.1.x:5000 (accessible from any device on your network)
  
For more information, visit: https://github.com/PC0staS/netwatch
        '''
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'NetWatch {get_version()}'
    )
    
    parser.add_argument(
        '--interface', '-i',
        help='Specify interface to monitor directly (console mode only)',
        metavar='INTERFACE'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Monitor all interfaces without selection menu (console mode only)'
    )
    
    parser.add_argument(
        '--web', '-w',
        action='store_true',
        help='Start web interface instead of console mode'
    )
    
    parser.add_argument(
        '--host',
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1 for localhost only, use 0.0.0.0 for network access)'
    )
    
    parser.add_argument(
        '--network', '-n',
        action='store_true',
        help='Enable network access (allows access from other devices on your network)'
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=5000,
        help='Port to run the web server on (default: 5000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode for development (shows detailed error messages)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.CYAN}🌐 NetWatch - Network Monitor{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
    
    try:
        # Create monitor instance
        monitor = NetworkMonitor()
        
        if args.web:
            # Web interface mode
            print(f"{Colors.GREEN}🌐 Iniciando interfaz web...{Colors.RESET}")
            
            # Check if network access is requested
            host = args.host
            if args.network:
                host = '0.0.0.0'
                print(f"{Colors.CYAN}🌐 Acceso de red habilitado - Accesible desde toda la red local{Colors.RESET}")
            
            try:
                from .web import WebInterface
                web_interface = WebInterface(monitor)
                web_interface.run(host=host, port=args.port, debug=args.debug)
            except ImportError as e:
                print(f"{Colors.RED}❌ Error: Flask no está instalado. Instala con: pip install flask flask-socketio{Colors.RESET}")
                print(f"{Colors.YELLOW}💡 O reinstala el paquete: pip install --upgrade netwatch-monitor{Colors.RESET}")
                sys.exit(1)
        else:
            # Console mode
            if args.all:
                monitor.selected_interfaces = monitor.get_available_interfaces()
                print(f"🌐 Monitoring ALL interfaces ({len(monitor.selected_interfaces)} total)")
            elif args.interface:
                available = monitor.get_available_interfaces()
                if args.interface in available:
                    monitor.selected_interfaces = [args.interface]
                    print(f"🎯 Monitoring interface: {args.interface}")
                else:
                    print(f"❌ Interface '{args.interface}' not found!")
                    print(f"Available interfaces: {', '.join(available)}")
                    sys.exit(1)
            else:
                if not monitor.select_interfaces():
                    sys.exit(1)
            
            monitor.run_console_mode()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 ¡Hasta luego!{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()
