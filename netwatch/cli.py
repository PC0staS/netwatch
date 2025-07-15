"""
Command Line Interface for NetWatch
"""

from .monitor import NetworkMonitor, Colors

def main():
    """Main function"""
    print(f"{Colors.BOLD}{Colors.CYAN}🌐 NetWatch - Network Monitor{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.MAGENTA}{'═' * 50}{Colors.RESET}")
    
    try:
        monitor = NetworkMonitor()
        monitor.run_console_mode()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.BOLD}{Colors.YELLOW}👋 Program terminated by user.{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.BOLD}{Colors.RED}❌ Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    main()
