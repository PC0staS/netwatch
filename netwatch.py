import psutil
import time
from collections import deque
from datetime import datetime
import os

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
        
    def select_interfaces(self):
        """Allow user to select which interfaces to monitor"""
        available_interfaces = self.get_available_interfaces()
        
        print("\n" + "="*60)
        print("AVAILABLE NETWORK INTERFACES")
        print("="*60)
        
        for i, interface in enumerate(available_interfaces, 1):
            print(f"{i}. {interface}")
        
        print("\n" + "="*60)
        print("SELECTION OPTIONS:")
        print("0 - Monitor ALL interfaces")
        print("1,2,3 - Monitor specific interfaces (comma-separated)")
        print("Example: '1,3' to monitor interfaces 1 and 3")
        print("="*60)
        
        while True:
            try:
                choice = input("\nEnter your selection: ").strip()
                
                if choice == "0":
                    self.selected_interfaces = available_interfaces
                    print(f"\n✅ Selected ALL interfaces ({len(available_interfaces)} total)")
                    break
                elif choice:
                    # Parse comma-separated values
                    indices = [int(x.strip()) for x in choice.split(",")]
                    selected = []
                    
                    for idx in indices:
                        if 1 <= idx <= len(available_interfaces):
                            selected.append(available_interfaces[idx - 1])
                        else:
                            print(f"❌ Invalid interface number: {idx}")
                            continue
                    
                    if selected:
                        self.selected_interfaces = selected
                        print(f"\n✅ Selected interfaces:")
                        for interface in selected:
                            print(f"   - {interface}")
                        break
                    else:
                        print("❌ No valid interfaces selected. Please try again.")
                else:
                    print("❌ Please enter a valid selection.")
                    
            except ValueError:
                print("❌ Invalid input. Please enter numbers separated by commas.")
            except KeyboardInterrupt:
                print("\n\nProgram cancelled by user.")
                self.running = False
                return False
                
        return True
        
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
    
    def create_ascii_graph(self, data_history, width=50, height=8):
        """Create a simple ASCII graph from data history"""
        if len(data_history) < 2:
            return ["No data yet..." + " " * (width - 14)]
        
        # Get the data points
        data = list(data_history)
        
        # Find min and max for scaling
        max_val = max(data) if data else 1
        min_val = min(data) if data else 0
        
        # Avoid division by zero
        if max_val == min_val:
            max_val = min_val + 1
        
        # Create the graph
        graph = []
        
        # Top border
        graph.append("┌" + "─" * width + "┐")
        
        # Graph lines
        for i in range(height):
            line = "│"
            threshold = min_val + (max_val - min_val) * (height - i - 1) / (height - 1)
            
            for j in range(min(width, len(data))):
                if data[j] >= threshold:
                    line += "█"
                else:
                    line += " "
            
            # Fill remaining space
            line += " " * (width - min(width, len(data)))
            line += "│"
            graph.append(line)
        
        # Bottom border with scale
        graph.append("└" + "─" * width + "┘")
        
        # Add scale info
        if max_val > 0:
            scale_info = f"Max: {bytesToHuman(max_val)}/s"
        else:
            scale_info = "No activity"
        
        graph.append(scale_info)
        
        return graph
    
    def print_stats(self):
        """Print current network statistics for selected interfaces with ASCII graphs"""
        # Clear terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print(f"NetWatch - Network Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Monitoring {len(self.selected_interfaces)} interface(s)")
        print("=" * 80)
        
        # Only show selected interfaces
        for interface in self.selected_interfaces:
            if interface in self.interface_data and len(self.interface_data[interface]['sent_history']) > 0:
                data = self.interface_data[interface]
                current_sent = data['sent_history'][-1]
                current_recv = data['recv_history'][-1]
                
                print(f"\n📡 Interface: {interface}")
                print(f"   Real-time:")
                print(f"     ⬆️  Sent: {bytesToHuman(current_sent)}/s")
                print(f"     ⬇️  Recv: {bytesToHuman(current_recv)}/s")
                print(f"   Cumulative:")
                print(f"     ⬆️  Total Sent: {bytesToHuman(data['sent_total'])}")
                print(f"     ⬇️  Total Recv: {bytesToHuman(data['recv_total'])}")
                
                # Show ASCII graphs if we have enough data
                if len(data['sent_history']) >= 2:
                    print(f"\n   📊 Sent Traffic (last {len(data['sent_history'])} seconds):")
                    sent_graph = self.create_ascii_graph(data['sent_history'], width=60, height=6)
                    for line in sent_graph:
                        print(f"     {line}")
                    
                    print(f"\n   📊 Received Traffic (last {len(data['recv_history'])} seconds):")
                    recv_graph = self.create_ascii_graph(data['recv_history'], width=60, height=6)
                    for line in recv_graph:
                        print(f"     {line}")
        
        print("\n" + "=" * 80)
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)
    
    def run_console_mode(self):
        """Run in console mode with text output"""
        print("\n🚀 Starting network monitoring...")
        print("📊 Gathering interface data...")
        
        # Let user select interfaces
        if not self.select_interfaces():
            return
        
        print(f"\n🔄 Monitoring started for {len(self.selected_interfaces)} interface(s)")
        print("⏱️  Updates every second - Press Ctrl+C to stop")
        
        # Wait a moment before starting
        time.sleep(2)
        
        try:
            while self.running:
                self.update_data()
                self.print_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n🛑 Network monitoring stopped by user.")
            self.running = False

def get_net_io():
    """Legacy function for backward compatibility"""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def main():
    """Main function"""
    print("🌐 NetWatch - Network Monitor")
    print("=" * 50)
    
    try:
        monitor = NetworkMonitor()
        monitor.run_console_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Program terminated by user.")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()