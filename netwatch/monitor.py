"""
Network Monitor Core Module
"""

import psutil
import time
from collections import deque
from datetime import datetime

# ANSI Color codes for terminal colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

def bytesToHuman(num):
    """
    Convert bytes to a human-readable format.
    """
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
    step = 1024.0
    for symbol in symbols:
        if num < step:
            return f"{num:.2f} {symbol}"
        num /= step
    return f"{num:.2f} YB"

class NetworkMonitor:
    def __init__(self):
        self.interface_data = {}
        self.time_history = deque(maxlen=60)
        self.running = True
        self.selected_interfaces = []
        
    def get_available_interfaces(self):
        """Get all available network interfaces"""
        net_io = psutil.net_io_counters(pernic=True)
        return list(net_io.keys())
        
    def get_interface_data(self, interface):
        """Get or create interface data structure"""
        if interface not in self.interface_data:
            self.interface_data[interface] = {
                'sent_history': deque(maxlen=60),  # Keep last 60 seconds
                'recv_history': deque(maxlen=60),
                'sent_total': 0,
                'recv_total': 0,
                'last_sent': 0,
                'last_recv': 0
            }
        return self.interface_data[interface]
        
    def get_net_io_per_interface(self):
        """Get network I/O stats for each interface"""
        net_io = psutil.net_io_counters(pernic=True)
        return net_io
    
    def update_data(self):
        """Update network data for selected interfaces only"""
        current_time = datetime.now()
        self.time_history.append(current_time)
        
        net_io = self.get_net_io_per_interface()
        
        # Only process selected interfaces
        for interface in self.selected_interfaces:
            if interface in net_io:
                stats = net_io[interface]
                data = self.get_interface_data(interface)
                
                # Calculate rate (bytes per second)
                if data['last_sent'] > 0:
                    sent_rate = stats.bytes_sent - data['last_sent']
                    recv_rate = stats.bytes_recv - data['last_recv']
                else:
                    sent_rate = 0
                    recv_rate = 0
                    
                # Update histories
                data['sent_history'].append(sent_rate)
                data['recv_history'].append(recv_rate)
                
                # Update totals
                data['sent_total'] = stats.bytes_sent
                data['recv_total'] = stats.bytes_recv
                
                # Update last values
                data['last_sent'] = stats.bytes_sent
                data['last_recv'] = stats.bytes_recv
    
    def create_ascii_graph(self, data_history, width=50, height=8, color_scheme="blue"):
        """Create a beautiful ASCII graph from data history"""
        if len(data_history) < 2:
            empty_graph = []
            empty_graph.append(f"{Colors.CYAN}╭{'─' * width}╮{Colors.RESET}")
            for i in range(height):
                empty_graph.append(f"{Colors.CYAN}│{Colors.YELLOW}{'No data yet...'.center(width)}{Colors.CYAN}│{Colors.RESET}")
            empty_graph.append(f"{Colors.CYAN}╰{'─' * width}╯{Colors.RESET}")
            return empty_graph
        
        # Get the data points
        data = list(data_history)
        
        # Find min and max for scaling
        max_val = max(data) if data else 1
        min_val = min(data) if data else 0
        
        # Avoid division by zero
        if max_val == min_val:
            max_val = min_val + 1
        
        # Color schemes
        colors = {
            "blue": [Colors.BLUE, Colors.CYAN, Colors.WHITE],
            "green": [Colors.GREEN, Colors.YELLOW, Colors.WHITE],
            "red": [Colors.RED, Colors.MAGENTA, Colors.WHITE],
            "sent": [Colors.BLUE, Colors.CYAN, Colors.WHITE],
            "recv": [Colors.GREEN, Colors.YELLOW, Colors.WHITE]
        }
        
        color_set = colors.get(color_scheme, colors["blue"])
        
        # Create the graph
        graph = []
        
        # Top border with gradient
        top_border = f"{Colors.BOLD}{Colors.CYAN}╭{'─' * width}╮{Colors.RESET}"
        graph.append(top_border)
        
        # Graph lines with gradient effect
        for i in range(height):
            line = f"{Colors.CYAN}│{Colors.RESET}"
            threshold = min_val + (max_val - min_val) * (height - i - 1) / (height - 1)
            
            for j in range(min(width, len(data))):
                if data[j] >= threshold:
                    # Use different intensity based on value
                    intensity = (data[j] - min_val) / (max_val - min_val) if max_val > min_val else 0
                    
                    if intensity > 0.8:
                        line += f"{Colors.BOLD}{color_set[2]}█{Colors.RESET}"
                    elif intensity > 0.5:
                        line += f"{color_set[1]}█{Colors.RESET}"
                    elif intensity > 0.2:
                        line += f"{color_set[0]}▓{Colors.RESET}"
                    else:
                        line += f"{color_set[0]}▒{Colors.RESET}"
                else:
                    line += " "
            
            # Fill remaining space
            line += " " * (width - min(width, len(data)))
            line += f"{Colors.CYAN}│{Colors.RESET}"
            graph.append(line)
        
        # Bottom border with gradient
        bottom_border = f"{Colors.BOLD}{Colors.CYAN}╰{'─' * width}╯{Colors.RESET}"
        graph.append(bottom_border)
        
        # Add scale info with colors
        if max_val > 0:
            scale_info = f"{Colors.BOLD}{Colors.YELLOW}📊 Max: {Colors.GREEN}{bytesToHuman(max_val)}/s{Colors.RESET}"
        else:
            scale_info = f"{Colors.BOLD}{Colors.WHITE}💤 No activity{Colors.RESET}"
        
        graph.append(scale_info)
        
        return graph
    
    def select_interfaces(self):
        """Allow user to select which interfaces to monitor"""
        available_interfaces = self.get_available_interfaces()
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}🌐 AVAILABLE NETWORK INTERFACES{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        
        for i, interface in enumerate(available_interfaces, 1):
            print(f"{Colors.BOLD}{Colors.YELLOW}{i}.{Colors.RESET} {Colors.CYAN}{interface}{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}🎯 SELECTION OPTIONS:{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}0{Colors.RESET} - Monitor {Colors.BOLD}{Colors.YELLOW}ALL{Colors.RESET} interfaces")
        print(f"{Colors.BOLD}{Colors.GREEN}1,2,3{Colors.RESET} - Monitor {Colors.BOLD}{Colors.YELLOW}specific{Colors.RESET} interfaces (comma-separated)")
        print(f"{Colors.BOLD}{Colors.BLUE}Example:{Colors.RESET} {Colors.YELLOW}'1,3'{Colors.RESET} to monitor interfaces 1 and 3")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 70}{Colors.RESET}")
        
        while True:
            try:
                choice = input(f"\n{Colors.BOLD}{Colors.MAGENTA}🔍 Enter your selection: {Colors.RESET}").strip()
                
                if choice == "0":
                    self.selected_interfaces = available_interfaces
                    print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Selected ALL interfaces ({len(available_interfaces)} total){Colors.RESET}")
                    break
                elif choice:
                    # Parse comma-separated values
                    indices = [int(x.strip()) for x in choice.split(",")]
                    selected = []
                    
                    for idx in indices:
                        if 1 <= idx <= len(available_interfaces):
                            selected.append(available_interfaces[idx - 1])
                        else:
                            print(f"{Colors.BOLD}{Colors.RED}❌ Invalid interface number: {idx}{Colors.RESET}")
                            continue
                    
                    if selected:
                        self.selected_interfaces = selected
                        print(f"\n{Colors.BOLD}{Colors.GREEN}✅ Selected interfaces:{Colors.RESET}")
                        for interface in selected:
                            print(f"   {Colors.BOLD}{Colors.CYAN}- {interface}{Colors.RESET}")
                        break
                    else:
                        print(f"{Colors.BOLD}{Colors.RED}❌ No valid interfaces selected. Please try again.{Colors.RESET}")
                else:
                    print(f"{Colors.BOLD}{Colors.RED}❌ Please enter a valid selection.{Colors.RESET}")
                    
            except ValueError:
                print(f"{Colors.BOLD}{Colors.RED}❌ Invalid input. Please enter numbers separated by commas.{Colors.RESET}")
            except KeyboardInterrupt:
                print(f"\n\n{Colors.BOLD}{Colors.RED}Program cancelled by user.{Colors.RESET}")
                self.running = False
                return False
                
        return True
    
    def print_stats(self):
        """Print current network statistics for selected interfaces with beautiful ASCII graphs"""
        import os
        from datetime import datetime
        
        # Clear terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Beautiful header
        header_line = "═" * 85
        print(f"{Colors.BOLD}{Colors.CYAN}{header_line}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.WHITE}🌐 NetWatch - Network Monitor{Colors.RESET} {Colors.YELLOW}⚡ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}📊 Monitoring {len(self.selected_interfaces)} interface(s){Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{header_line}{Colors.RESET}")
        
        # Only show selected interfaces
        for interface in self.selected_interfaces:
            if interface in self.interface_data and len(self.interface_data[interface]['sent_history']) > 0:
                data = self.interface_data[interface]
                current_sent = data['sent_history'][-1]
                current_recv = data['recv_history'][-1]
                
                # Interface header with decorative elements
                print(f"\n{Colors.BOLD}{Colors.MAGENTA}╭─────────────────────────────────────────────────────────────────────────────────╮{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.MAGENTA}│{Colors.RESET} {Colors.BOLD}{Colors.CYAN}📡 Interface: {Colors.YELLOW}{interface}{Colors.RESET}" + " " * (79 - len(interface)) + f"{Colors.BOLD}{Colors.MAGENTA}│{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.MAGENTA}╰─────────────────────────────────────────────────────────────────────────────────╯{Colors.RESET}")
                
                # Real-time stats with icons and colors
                print(f"\n   {Colors.BOLD}{Colors.WHITE}⚡ Real-time Traffic:{Colors.RESET}")
                print(f"     {Colors.BOLD}{Colors.BLUE}⬆️  Sent:    {Colors.GREEN}{bytesToHuman(current_sent)}/s{Colors.RESET}")
                print(f"     {Colors.BOLD}{Colors.RED}⬇️  Recv:    {Colors.GREEN}{bytesToHuman(current_recv)}/s{Colors.RESET}")
                
                print(f"\n   {Colors.BOLD}{Colors.WHITE}📈 Cumulative Traffic:{Colors.RESET}")
                print(f"     {Colors.BOLD}{Colors.BLUE}⬆️  Total Sent: {Colors.CYAN}{bytesToHuman(data['sent_total'])}{Colors.RESET}")
                print(f"     {Colors.BOLD}{Colors.RED}⬇️  Total Recv: {Colors.CYAN}{bytesToHuman(data['recv_total'])}{Colors.RESET}")
                
                # Show beautiful ASCII graphs if we have enough data
                if len(data['sent_history']) >= 2:
                    print(f"\n   {Colors.BOLD}{Colors.BLUE}📊 Sent Traffic History {Colors.WHITE}(last {len(data['sent_history'])} seconds):{Colors.RESET}")
                    sent_graph = self.create_ascii_graph(data['sent_history'], width=65, height=6, color_scheme="sent")
                    for line in sent_graph:
                        print(f"     {line}")
                    
                    print(f"\n   {Colors.BOLD}{Colors.RED}📊 Received Traffic History {Colors.WHITE}(last {len(data['recv_history'])} seconds):{Colors.RESET}")
                    recv_graph = self.create_ascii_graph(data['recv_history'], width=65, height=6, color_scheme="recv")
                    for line in recv_graph:
                        print(f"     {line}")
                
                # Add a separator between interfaces
                print(f"\n{Colors.BOLD}{Colors.WHITE}{'─' * 85}{Colors.RESET}")
        
        # Footer
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 85}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}⚠️  Press Ctrl+C to stop monitoring{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 85}{Colors.RESET}")
    
    def run_console_mode(self):
        """Run in console mode with text output"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🚀 Starting network monitoring...{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}📊 Gathering interface data...{Colors.RESET}")
        
        # Let user select interfaces only if not already selected
        if not hasattr(self, 'selected_interfaces') or not self.selected_interfaces:
            if not self.select_interfaces():
                return
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}🔄 Monitoring started for {len(self.selected_interfaces)} interface(s){Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}⏱️  Updates every second - Press Ctrl+C to stop{Colors.RESET}")
        
        # Wait a moment before starting
        time.sleep(2)
        
        try:
            while self.running:
                self.update_data()
                self.print_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"\n\n{Colors.BOLD}{Colors.RED}🛑 Network monitoring stopped by user.{Colors.RESET}")
            self.running = False
