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
            return "1.0.1"  # Fallback version

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        prog='netwatch-monitor',
        description='🌐 NetWatch - A beautiful console-based network monitoring tool with ASCII graphs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  netwatch-monitor              # Start network monitoring
  netwatch-monitor --version    # Show version
  netwatch-monitor --help       # Show this help message
  netwatch-monitor --all        # Monitor all interfaces
  netwatch-monitor -i eth0      # Monitor specific interface

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
        help='Specify interface to monitor (optional)',
        metavar='INTERFACE'
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='Monitor all interfaces without selection menu'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    print(f"{Colors.BOLD}{Colors.CYAN}🌐 NetWatch - Network Monitor{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
    
    try:
        # Create monitor instance
        monitor = NetworkMonitor()
        
        # Handle different argument combinations
        if args.all:
            # Monitor all interfaces
            monitor.selected_interfaces = monitor.get_available_interfaces()
            print(f"🌐 Monitoring ALL interfaces ({len(monitor.selected_interfaces)} total)")
        elif args.interface:
            # Monitor specific interface
            available = monitor.get_available_interfaces()
            if args.interface in available:
                monitor.selected_interfaces = [args.interface]
                print(f"🎯 Monitoring interface: {args.interface}")
            else:
                print(f"❌ Interface '{args.interface}' not found!")
                print(f"Available interfaces: {', '.join(available)}")
                sys.exit(1)
        else:
            # Normal interactive mode
            if not monitor.select_interfaces():
                sys.exit(1)
        
        # Start monitoring
        monitor.run_console_mode()
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BOLD}{Colors.YELLOW}👋 Program terminated by user.{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BOLD}{Colors.RED}❌ Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
