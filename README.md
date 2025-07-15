# NetWatch - Network Monitor 🌐

A beautiful console-based network monitoring tool with real-time ASCII graphs and colorful interface.

## ✨ Features

- 🎯 **Interface Selection**: Choose specific network interfaces to monitor or monitor all
- 📊 **Real-time Traffic**: Live monitoring of sent/received bytes per second
- 📈 **Cumulative Stats**: Total bytes sent and received since monitoring started
- 🎨 **Beautiful ASCII Graphs**: Colorful real-time traffic history graphs
- 🌈 **Colorful Interface**: Rich terminal colors with emojis and visual elements
- 🔄 **Cross-platform**: Works on Windows, Linux, and macOS
- ⚡ **Easy Installation**: Simple pip install from anywhere

## 🚀 Installation

### Method 1: Install from Source (Recommended)

1. Clone or download the project
2. Navigate to the project directory
3. Install in development mode:

```bash
pip install -e .
```

### Method 2: Install from PyPI

```bash
pip install netwatch-monitor
```

## 🎮 Usage

After installation, simply run:

```bash
netwatch
```

The tool will:
1. Show all available network interfaces
2. Let you select which interfaces to monitor:
   - `0` - Monitor ALL interfaces
   - `1,2,3` - Monitor specific interfaces (comma-separated)
3. Start real-time monitoring with beautiful ASCII graphs

### Example Usage

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
- **Width**: 65 characters
- **Height**: 6 rows
- **Colors**: Different color schemes for sent (blue) and received (green) traffic
- **Intensity**: Multiple intensity levels based on traffic volume
- **Scale**: Automatic scaling with max value display

### Interface Selection
- **Smart Selection**: Easy number-based selection
- **Multiple Interfaces**: Monitor several interfaces simultaneously
- **All Interfaces**: Quick option to monitor everything
- **Validation**: Input validation with helpful error messages

## 🛠️ Requirements

- Python 3.6+
- psutil (automatically installed)
- Works on Windows, Linux, and macOS
- Terminal with ANSI color support (most modern terminals)

## 🔧 Development

### Project Structure
```
netwatch/
├── netwatch/
│   ├── __init__.py
│   ├── monitor.py      # Core monitoring logic
│   └── cli.py          # Command line interface
├── setup.py            # Package setup
├── pyproject.toml      # Modern Python packaging
├── requirements.txt    # Dependencies
└── README.md          # This file
```

### Building from Source
```bash
# Clone the repository
git clone <repository-url>
cd netwatch

# Install in development mode
pip install -e .

# Run the tool
netwatch
```

## 🎯 Use Cases

- **Network Debugging**: Monitor interface activity during troubleshooting
- **Performance Monitoring**: Track bandwidth usage on specific interfaces
- **Development**: Monitor network activity during application development
- **System Administration**: Quick network interface overview
- **Educational**: Learn about network interfaces and traffic patterns

## 🚀 Cross-Platform Support

### Windows
- Full support with PowerShell and Command Prompt
- Colorful interface with emoji support
- All network interfaces detected

### Linux
- Native terminal support
- Works with all major distributions
- Systemd service compatible

### macOS
- Terminal.app and iTerm2 support
- Full color and emoji support
- Works with all network interfaces

## 📝 Commands

- **Start**: `netwatch`
- **Stop**: `Ctrl+C`
- **Interface Selection**: Follow on-screen prompts

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

## 🐛 Troubleshooting

### Common Issues

1. **No interfaces shown**: Make sure you have network interfaces configured
2. **Colors not working**: Ensure your terminal supports ANSI colors
3. **Permission errors**: Some systems may require elevated privileges for network monitoring
4. **Import errors**: Make sure psutil is installed: `pip install psutil`

### Requirements
- Minimum Python 3.6
- psutil library
- Terminal with ANSI color support

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or report issues.

## 🔮 Future Features

- [ ] Export data to CSV/JSON
- [ ] Historical data storage
- [ ] Web interface
- [ ] Network alerts/notifications
- [ ] Bandwidth usage graphs
- [ ] Custom refresh intervals
- [ ] Multiple monitoring modes

---

Made with ❤️ for network monitoring enthusiasts!
