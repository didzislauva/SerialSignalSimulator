# Serial Signal Simulator

## Overview
The Serial Signal Simulator is a web-based application that allows users to visualize and simulate serial communication signals. It provides interactive controls to modify data values, CRC type, start bit, parity bit, and stop bits, and displays the corresponding signal waveform along with a clock signal using Chart.js.

## Features
- **Interactive UI**: Easily adjust serial communication parameters.
- **Real-time Visualization**: Displays both clock and serial signals dynamically.
- **Custom Data Input**: Users can enter custom 8-bit data and CRC values.
- **Legend for Bit Types**: Different colors for idle, start, data, parity, CRC, and stop bits.
- **Responsive Design**: Works across different screen sizes and devices.

## Technologies Used
- **HTML, CSS**: For UI layout and styling.
- **JavaScript**: Handles data processing and chart updates.
- **Chart.js**: Visualizes clock and serial signals.

## How to Use
1. Open the `index.html` file in a browser.
2. Adjust parameters such as data bits, CRC bits, start bit, parity bit, and stop bits.
3. Click **"Generate Signal"** to update the charts.
4. The clock signal and serial signal will be visualized in real-time.
5. Use the legend to understand different bit types.

## Controls
| Control | Description |
|---------|-------------|
| **Data Bits** | Input 8-bit binary data |
| **CRC Bits** | Input 8-bit CRC value |
| **Start Bit** | Fixed at 0 |
| **Parity Bit** | Choose between 0 and 1 |
| **Stop Bits** | Choose 1 or 2 |
| **Generate Signal** | Updates the charts with entered values |

## Example
### Input:
- Data: `00110001`
- CRC: `10110011`
- Start Bit: `0`
- Parity Bit: `1`
- Stop Bit: `1`

### Output:
A signal waveform displaying each bit with corresponding time intervals and clock signal overlay.

## Future Enhancements
- Add more CRC calculation methods.
- Implement additional parity checking mechanisms.
- Save and export generated signals as images.

## License
This project is open-source and available for modification and redistribution under the MIT License.

