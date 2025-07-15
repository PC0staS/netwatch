# Ne## Features

- 📡 Real-time network statistics for all interfaces
- 📊 Cumulative bytes sent/received tracking
- 📈 ASCII graphs showing traffic variation over time
- 🎨 Clean terminal output with automatic clearing
- 🔄 Updates every second
- 💻 Lightweight console-only interface
- 🎯 Interface selection (all or specific interfaces) Network Monitor

A comprehensive console-based network monitoring tool with real-time statistics and visual indicators.

## Features

- 📡 Real-time network statistics for all interfaces
- 📊 Cumulative bytes sent/received tracking
- 📈 Trend indicators (📈 increasing, 📉 decreasing, ➡️ stable)
- 🎨 Clean terminal output with automatic clearing
- 🔄 Updates every second
- � Lightweight console-only interface

## Usage

```bash
python netwatch.py
```

When you run the program, you'll be prompted to select which network interfaces to monitor:
- Enter `0` to monitor ALL interfaces
- Enter specific numbers separated by commas (e.g., `1,3,5`) to monitor specific interfaces
- Example: `1,2` to monitor interfaces 1 and 2

## Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python netwatch.py
```

## Requirements

- Python 3.6+
- psutil

## Interface Information

The tool monitors all network interfaces including:
- Physical Ethernet adapters
- WiFi adapters
- Virtual network adapters (VMware, VirtualBox, etc.)
- Bluetooth network connections
- Loopback interfaces

## Data Displayed

### Real-time Data
- **Sent**: Bytes sent per second
- **Recv**: Bytes received per second

### Cumulative Data
- **Total Sent**: Total bytes sent since system boot
- **Total Recv**: Total bytes received since system boot

### Visual Graphs
- **ASCII Graphs**: Real-time visualization of traffic patterns
- **Traffic History**: Shows the last 60 seconds of activity
- **Automatic Scaling**: Graphs adjust to current traffic levels

## Controls

- **Ctrl+C**: Stop monitoring

## Tips

- Lightweight and fast console-only monitoring
- Select specific interfaces to reduce clutter
- Monitor multiple interfaces simultaneously
- Data is formatted in human-readable units (B, KB, MB, GB, etc.)
- Use `0` to monitor all interfaces or comma-separated numbers for specific ones
- ASCII graphs provide visual feedback of traffic patterns and spikes
