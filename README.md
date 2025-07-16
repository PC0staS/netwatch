# NetWatch - Professional Network Monitor 🌐

An elegant network monitoring tool with modern console and web interfaces, designed with a professional pastel color palette.

## ✨ Features

### 🖥️ Console Interface
- 🎯 **Interface Selection**: Choose specific interfaces or monitor all
- 📊 **Real-time Traffic**: Live monitoring of sent/received bytes per second
- 📈 **Cumulative Statistics**: Total bytes sent and received
- 🎨 **ASCII Graphs**: Colorful real-time traffic history graphs
- 🌈 **Colorful Interface**: Rich terminal colors with emojis and visual elements

### 🌐 Web Interface
- 🎨 **Professional Pastel Palette**: Modern design with soft and elegant colors
- 📱 **Responsive**: Perfectly adapted for mobile and desktop
- 📊 **Interactive Charts**: Advanced visualization with Chart.js
- 🔄 **Real-time Data**: Automatic updates without simulations
- 🚫 **No Fake Data**: Shows disconnected state when no real data is available
- 🎯 **REST API**: Endpoints for integration with other systems

### 🔧 Technical Features
- 🔄 **Cross-platform**: Works on Windows, Linux and macOS
- ⚡ **Easy Installation**: Simple pip installation
- 🐍 **Python 3.7+**: Support for modern Python versions
- 📦 **Professional Packaging**: Ready for distribution

## 🚀 Installation

### Method 1: Install from PyPI (Recommended)

```bash
pip install netwatch-monitor
```

### Method 2: Install from Source

1. Clone the repository:
```bash
git clone https://github.com/PC0staS/netwatch.git
cd netwatch
```

2. Install in development mode:
```bash
pip install -e .
```

## 🎮 Usage

### 🖥️ Console Interface

After installation, simply run:

```bash
netwatch
```

The tool will:
1. Show all available network interfaces
2. Let you select which interfaces to monitor:
   - `0` - Monitor ALL interfaces
   - `1,2,3` - Monitor specific interfaces (comma-separated)
3. Start real-time monitoring with ASCII graphs

### 🌐 Web Interface

To start the web interface:

```bash
netwatch-web
```

For network access (accessible from other devices on your local network):

```bash
netwatch-web --network
```

Or with custom options:

```bash
netwatch-web --host 0.0.0.0 --port 8080 --debug
```

**Alternative method using main command:**

```bash
netwatch --web --network --port 8080
```

Then open your browser at `http://localhost:5000` (or the port you specify).

**For network access:** Use your computer's IP address from other devices, e.g., `http://192.168.1.100:5000`

#### Web Interface Features:
- 🎨 **Professional Pastel Palette**: Soft and elegant colors
- 📱 **Responsive Design**: Works perfectly on mobile devices
- 📊 **Interactive Charts**: Advanced data visualization
- 🔄 **Real-time Updates**: Automatic refresh every 2 seconds
- 🚫 **No Simulated Data**: Shows disconnected state when no data available
- 🎯 **Intuitive Controls**: Easy interface selection and monitoring control

### Example Usage - Console

```bash
$ netwatch

🌐 NetWatch - Network Monitor
══════════════════════════════════════════════════
🚀 Starting network monitoring...
📊 Gathering interface data...

═══════════════════════════════════════════════════════════════════════════
🌐 AVAILABLE NETWORK INTERFACES
═══════════════════════════════════════════════════════════════════════════

1. Ethernet
2. Wi-Fi
3. Loopback

═══════════════════════════════════════════════════════════════════════════
🎯 SELECTION OPTIONS:
0 - Monitor ALL interfaces
1,2,3 - Monitor specific interfaces (comma-separated)
Example: '1,3' to monitor interfaces 1 and 3
═══════════════════════════════════════════════════════════════════════════

🔍 Enter your selection: 1

✅ Selected interfaces:
   - Ethernet

🔄 Monitoring started for 1 interface(s)
⏱️  Updates every second - Press Ctrl+C to stop
```

## 📊 Interface Display

For each selected interface, you'll see:

- **Real-time Traffic**: Current bytes per second (sent/received)
- **Cumulative Traffic**: Total bytes since monitoring started
- **ASCII Graphs**: Beautiful colored graphs showing traffic history
- **Visual Elements**: Emojis, colors, and borders for better readability

## 🎨 Features Details

### ASCII Graphs
- **Width**: 65 characters wide
- **Height**: 6 rows of data
- **Colors**: Different color schemes for sent (blue) and received (green) traffic
- **Intensity**: Multiple intensity levels based on traffic volume
- **Scale**: Automatic scaling with max value display

### Web Interface Color Palette
- **Primary**: Soft purple (#8B7EC8)
- **Secondary**: Mint green (#A8D5BA)
- **Accent**: Soft pink (#FFB6C1)
- **Success**: Aqua mint (#98E4D6)
- **Warning**: Soft yellow (#F4D03F)
- **Danger**: Soft coral (#F1948A)

## 🛠️ Requirements

- Python 3.7+
- psutil (automatically installed)
- Flask & Flask-SocketIO (for web interface)
- Works on Windows, Linux, and macOS
- Terminal with ANSI color support (most modern terminals)

## 🔧 Development

### Project Structure
```
netwatch/
├── netwatch/
│   ├── __init__.py
│   ├── monitor.py      # Core monitoring logic
│   ├── cli.py          # Command line interface
│   ├── web.py          # Web interface
│   ├── static/         # CSS, JS, and assets
│   └── templates/      # HTML templates
├── setup.py            # Package setup
├── pyproject.toml      # Modern Python packaging
├── requirements.txt    # Dependencies
└── README.md          # This file
```

### Building from Source
```bash
# Clone the repository
git clone https://github.com/PC0staS/netwatch.git
cd netwatch

# Install in development mode
pip install -e .

# Run the console version
netwatch

# Run the web version
netwatch-web
```

## 🎯 Use Cases

- **Network Debugging**: Monitor interface activity during troubleshooting
- **Performance Monitoring**: Track bandwidth usage on specific interfaces
- **Development**: Monitor network activity during application development
- **System Administration**: Quick network interface overview
- **Educational**: Learn about network interfaces and traffic patterns
- **Remote Monitoring**: Use web interface for remote network monitoring

## 🚀 Cross-Platform Support

### Windows
- Full support with PowerShell and Command Prompt
- Colorful interface with emoji support
- All network interfaces detected
- Web interface works with all browsers

### Linux
- Native terminal support
- Works with all major distributions
- Systemd service compatible
- Web interface accessible remotely

### macOS
- Terminal.app and iTerm2 support
- Full color and emoji support
- Works with all network interfaces
- Safari and Chrome compatible

## 📝 Commands

### Console Commands
- **Start Console**: `netwatch`
- **Stop**: `Ctrl+C`
- **Interface Selection**: Follow on-screen prompts

### Web Commands
- **Start Web Interface (localhost only)**: `netwatch-web`
- **Start Web Interface (network access)**: `netwatch-web --network`
- **Custom Host/Port**: `netwatch-web --host 0.0.0.0 --port 8080`
- **Network + Custom Port**: `netwatch-web --network --port 8080`
- **Debug Mode**: `netwatch-web --debug`
- **Help**: `netwatch-web --help`

### Network Access
- **Localhost only**: `netwatch-web` (default)
- **Network access**: `netwatch-web --network` or `netwatch-web --host 0.0.0.0`
- **Access from other devices**: Use your computer's IP address (e.g., `http://192.168.1.100:5000`)

## 🌐 API Endpoints

The web interface provides REST API endpoints:

- `GET /api/interfaces` - List available network interfaces
- `GET /api/stats` - Get current network statistics
- `POST /api/start_monitoring` - Start monitoring selected interfaces
- `POST /api/stop_monitoring` - Stop monitoring

## 🎉 Examples

### Monitor All Interfaces
```bash
netwatch
# Select: 0
```

### Monitor Specific Interfaces
```bash
netwatch
# Select: 1,3,5
```

### Monitor Single Interface
```bash
netwatch
# Select: 1
```

### Start Web Interface on Custom Port
```bash
netwatch-web --port 8080
```

## 🐛 Troubleshooting

### Common Issues

1. **No interfaces shown**: Make sure you have network interfaces configured
2. **Colors not working**: Ensure your terminal supports ANSI colors
3. **Permission errors**: Some systems may require elevated privileges for network monitoring
4. **Import errors**: Make sure all dependencies are installed: `pip install -r requirements.txt`
5. **Web interface not accessible**: Check if port is available and firewall settings

### Requirements
- Minimum Python 3.7
- psutil, Flask, Flask-SocketIO libraries
- Terminal with ANSI color support
- Modern web browser for web interface

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or report issues.

## 🔮 Future Features

- [ ] Export data to CSV/JSON
- [ ] Historical data storage
- [ ] Network alerts/notifications
- [ ] Bandwidth usage graphs
- [ ] Custom refresh intervals
- [ ] Multiple monitoring modes
- [ ] User authentication for web interface
- [ ] Dark/Light theme toggle

---

Made with ❤️ for network monitoring enthusiasts!
