import psutil
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.ticker as ticker
from collections import defaultdict, deque
import threading
from datetime import datetime

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
        """Update network data for all interfaces"""
        current_time = datetime.now()
        self.time_history.append(current_time)
        
        net_io = self.get_net_io_per_interface()
        
        for interface, stats in net_io.items():
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
    
    def print_stats(self):
        """Print current network statistics"""
        print("\n" + "="*80)
        print(f"Network Monitor - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        for interface, data in self.interface_data.items():
            if len(data['sent_history']) > 0:
                current_sent = data['sent_history'][-1]
                current_recv = data['recv_history'][-1]
                
                print(f"\n📡 Interface: {interface}")
                print(f"   Real-time:")
                print(f"     ⬆️  Sent: {bytesToHuman(current_sent)}/s")
                print(f"     ⬇️  Recv: {bytesToHuman(current_recv)}/s")
                print(f"   Cumulative:")
                print(f"     ⬆️  Total Sent: {bytesToHuman(data['sent_total'])}")
                print(f"     ⬇️  Total Recv: {bytesToHuman(data['recv_total'])}")
                
                # Show mini graph (text-based)
                if len(data['sent_history']) > 1:
                    sent_trend = "📈" if current_sent > data['sent_history'][-2] else "📉" if current_sent < data['sent_history'][-2] else "➡️"
                    recv_trend = "📈" if current_recv > data['recv_history'][-2] else "📉" if current_recv < data['recv_history'][-2] else "➡️"
                    print(f"   Trend: ⬆️ {sent_trend} | ⬇️ {recv_trend}")
    
    def create_plots(self):
        """Create matplotlib plots for network interfaces"""
        active_interfaces = [iface for iface, data in self.interface_data.items() 
                           if len(data['sent_history']) > 0 and (data['sent_history'][-1] > 0 or data['recv_history'][-1] > 0)]
        
        if not active_interfaces:
            return
            
        # Create subplots
        fig, axes = plt.subplots(len(active_interfaces), 2, figsize=(15, 4*len(active_interfaces)))
        fig.suptitle('Network Interface Monitoring', fontsize=16)
        
        if len(active_interfaces) == 1:
            axes = [axes]
        
        for i, interface in enumerate(active_interfaces):
            data = self.interface_data[interface]
            
            # Prepare time data
            time_points = list(range(len(data['sent_history'])))
            sent_data = list(data['sent_history'])
            recv_data = list(data['recv_history'])
            
            # Sent data plot
            axes[i][0].clear()
            axes[i][0].plot(time_points, sent_data, 'b-', linewidth=2, label='Sent')
            axes[i][0].set_title(f'{interface} - Bytes Sent/sec')
            axes[i][0].set_ylabel('Bytes/sec')
            axes[i][0].grid(True, alpha=0.3)
            axes[i][0].legend()
            
            # Format y-axis labels
            if sent_data:
                max_sent = max(sent_data) if sent_data else 0
                if max_sent > 0:
                    axes[i][0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: bytesToHuman(x)))
            
            # Received data plot
            axes[i][1].clear()
            axes[i][1].plot(time_points, recv_data, 'r-', linewidth=2, label='Received')
            axes[i][1].set_title(f'{interface} - Bytes Received/sec')
            axes[i][1].set_ylabel('Bytes/sec')
            axes[i][1].grid(True, alpha=0.3)
            axes[i][1].legend()
            
            # Format y-axis labels
            if recv_data:
                max_recv = max(recv_data) if recv_data else 0
                if max_recv > 0:
                    axes[i][1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: bytesToHuman(x)))
        
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)
    
    def run_console_mode(self):
        """Run in console mode with text output"""
        print("Starting network monitoring (Console Mode)... Press Ctrl+C to stop")
        
        try:
            while self.running:
                self.update_data()
                self.print_stats()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\nNetwork monitoring stopped.")
            self.running = False
    
    def run_gui_mode(self):
        """Run in GUI mode with matplotlib graphs"""
        print("Starting network monitoring (GUI Mode)... Close the plot window to stop")
        
        plt.ion()  # Interactive mode
        
        def update_plot():
            while self.running:
                self.update_data()
                self.create_plots()
                time.sleep(1)
        
        # Start data collection in a separate thread
        data_thread = threading.Thread(target=update_plot)
        data_thread.daemon = True
        data_thread.start()
        
        try:
            # Keep the main thread alive
            while self.running:
                plt.pause(0.1)
        except KeyboardInterrupt:
            print("\nNetwork monitoring stopped.")
            self.running = False
        finally:
            plt.ioff()

def get_net_io():
    """Legacy function for backward compatibility"""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def main():
    """Main function with mode selection"""
    import sys
    
    print("Network Monitor - Enhanced Edition")
    print("Choose mode:")
    print("1. Console Mode (text-based with emojis)")
    print("2. GUI Mode (graphical plots)")
    
    try:
        if len(sys.argv) > 1:
            mode = sys.argv[1]
        else:
            mode = input("Enter mode (1 or 2): ").strip()
        
        monitor = NetworkMonitor()
        
        if mode == "1" or mode.lower() == "console":
            monitor.run_console_mode()
        elif mode == "2" or mode.lower() == "gui":
            monitor.run_gui_mode()
        else:
            print("Invalid mode. Using console mode by default.")
            monitor.run_console_mode()
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"Error: {e}")
        print("Falling back to console mode...")
        monitor = NetworkMonitor()
        monitor.run_console_mode()

if __name__ == "__main__":
    main()