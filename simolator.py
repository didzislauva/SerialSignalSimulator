import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Test data
test_data = pd.DataFrame([{
    'timestamp': 1739448494.2427788,
    'start_bit': 0,
    'bits': '00110001',
    'parity_bit': 1,
    'crc': 10327,
    'stop_bit': 1
}])

def int_to_bits(n, width=16):
    """Convert an integer to a list of bits with specified width"""
    return [int(b) for b in format(n, f'0{width}b')]

def generate_clock_signal(times, clock_freq=9600):
    """Generate clock signal points"""
    period = 1/clock_freq
    clock_signal = []
    
    for t in times:
        cycles = t / (period/2)
        clock_signal.append(1 if int(cycles) % 2 == 0 else 0)
    
    return clock_signal

def expand_bits_to_signal(row, clock_freq=9600):
    """Convert a single row of serial data into signal points"""
    # Convert CRC to bits
    crc_bits = int_to_bits(int(row['crc']), width=16)  # 16-bit CRC
    
    # Add idle state (high)
    idle_bits = [1]
    
    # Get all bits
    start_bit = [int(row['start_bit'])]
    data_bits = [int(b) for b in str(row['bits']).strip()]
    parity_bit = [int(row['parity_bit'])]
    stop_bit = [int(row['stop_bit'])]
    
    # Combine all bits
    all_bits = idle_bits + start_bit + data_bits + parity_bit + crc_bits + stop_bit
    total_bits = len(all_bits)
    
    # Create time points based on clock frequency
    bit_period = 1/clock_freq
    samples_per_bit = 20  # Number of points to plot per bit for smooth visualization
    dt = bit_period / samples_per_bit
    
    base_time = 0
    times = []
    signals = []
    types = []
    
    for i, bit in enumerate(all_bits):
        bit_times = np.linspace(i*bit_period, (i+1)*bit_period, samples_per_bit)
        times.extend(bit_times)
        signals.extend([bit] * samples_per_bit)
        
        # Determine bit type
        if i < len(idle_bits):
            bit_type = 'idle'
        elif i < len(idle_bits) + 1:
            bit_type = 'start'
        elif i < len(idle_bits) + 1 + len(data_bits):
            bit_type = 'data'
        elif i < len(idle_bits) + 1 + len(data_bits) + 1:
            bit_type = 'parity'
        elif i < len(idle_bits) + 1 + len(data_bits) + 1 + len(crc_bits):
            bit_type = 'crc'
        else:
            bit_type = 'stop'
        types.extend([bit_type] * samples_per_bit)
    
    # Generate clock signal
    clock = generate_clock_signal(times, clock_freq)
    
    return pd.DataFrame({
        'time': times,
        'signal': signals,
        'clock': clock,
        'type': types
    })

# Process the test data
signal_data = expand_bits_to_signal(test_data.iloc[0])

# Plotting
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

# Plot clock signal on top subplot
ax1.step(signal_data['time'], signal_data['clock'], where='post', 
         label='Clock', color='red', linewidth=1.5)
ax1.set_ylabel('Clock')
ax1.grid(True, which='both', linestyle='--', alpha=0.7)
ax1.set_title('Serial Signal with Clock')
ax1.legend()

# Plot data signal on bottom subplot
ax2.step(signal_data['time'], signal_data['signal'], where='post', 
         label='Serial Signal', linewidth=2, color='blue')

# Color coding for different parts
colors = {
    'idle': 'gray',
    'start': 'red',
    'data': 'blue',
    'parity': 'green',
    'crc': 'orange',
    'stop': 'purple'
}

for bit_type in colors:
    mask = signal_data['type'] == bit_type
    if bit_type == 'data':  # Skip data as it's already plotted in main signal
        continue
    ax2.scatter(signal_data[mask]['time'], signal_data[mask]['signal'], 
               color=colors[bit_type], alpha=0.5, label=f'{bit_type.capitalize()} bit')

# Add bit labels
bit_sections = ['Idle', 'Start'] + ['Data']*8 + ['Parity'] + ['CRC']*16 + ['Stop']
for i, bit_type in enumerate(bit_sections):
    ax2.text(i/clock_freq + 0.5/clock_freq, -0.2, bit_type, 
             horizontalalignment='center', verticalalignment='top', 
             rotation=45 if bit_type == 'CRC' else 0)

# Customize bottom subplot
ax2.set_xlabel('Time (seconds)')
ax2.set_ylabel('Signal Level')
ax2.grid(True, which='both', linestyle='--', alpha=0.7)
ax2.set_ylim(-0.5, 1.5)
ax2.legend()

plt.tight_layout()
plt.show()
