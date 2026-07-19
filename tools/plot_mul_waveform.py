# -*- coding: utf-8 -*-
import os
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_vcd(vcd_path):
    signals = {
        '#': 'clk',
        '%': 'rst_n',
        '8': 'pc',
        '@': 'instruction',
        ':': 'opcode',
        '9': 'operand',
        '_': 'r0',
        '`': 'r1',
        'a': 'r2',
        'b': 'r3',
        '!': 'out_port',
        '"': 'halt_out'
    }
    
    # Store history of changes: time -> signal_name -> value
    data = {}
    current_time = 0
    current_vals = {name: 0 for name in signals.values()}
    
    # Initialize values
    time_series = []
    val_history = {name: [] for name in signals.values()}
    
    with open(vcd_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Time stamp
            if line.startswith('#'):
                new_time = int(line[1:])
                # Record state at current_time before moving to new_time
                time_series.append(current_time)
                for name, val in current_vals.items():
                    val_history[name].append(val)
                current_time = new_time
                continue
            
            # Signal changes
            if line.startswith('b'):
                # Vector value: e.g. "b0011 :" or "b111111111 @"
                parts = line.split()
                if len(parts) == 2:
                    val_str, sym = parts
                    val_bin = val_str[1:]
                    if 'x' in val_bin or 'z' in val_bin or 'X' in val_bin or 'Z' in val_bin:
                        val = 0
                    else:
                        val = int(val_bin, 2)
                    if sym in signals:
                        current_vals[signals[sym]] = val
            elif line[0] in ('0', '1', 'x', 'z') and len(line) == 2:
                # 1-bit value: e.g. "0#" or "1#"
                val_char, sym = line[0], line[1]
                if sym in signals:
                    if val_char in ('0', '1'):
                        current_vals[signals[sym]] = int(val_char)
                    else:
                        current_vals[signals[sym]] = 0 # Default for x/z
                        
    # Append final state
    time_series.append(current_time)
    for name, val in current_vals.items():
        val_history[name].append(val)
        
    return np.array(time_series), {k: np.array(v) for k, v in val_history.items()}

def plot_mul():
    vcd_path = 'cpu_top.vcd'
    if not os.path.exists(vcd_path):
        print("VCD file not found!")
        return
        
    time_series, val_history = parse_vcd(vcd_path)
    
    # Convert ps to ns (1ps = 0.001ns)
    time_ns = time_series * 0.001
    
    # Find the end of MUL program: first time halt_out goes to 1
    halt_out = val_history['halt_out']
    halt_indices = np.where(halt_out == 1)[0]
    if len(halt_indices) > 0:
        end_idx = halt_indices[0]
        # Keep 2 more steps after halt for visualization
        end_idx = min(end_idx + 4, len(time_ns) - 1)
        end_time = time_ns[end_idx]
    else:
        end_time = 250.0 # fallback
        
    # Crop data to the MUL execution window (0 to end_time)
    mask = time_ns <= end_time
    t = time_ns[mask]
    
    cropped_vals = {}
    for name, vals in val_history.items():
        cropped_vals[name] = vals[mask]
        
    # Set up matplotlib figure
    # We want to plot: clk, rst_n, pc, instruction, r0, r1, r2, r3, out_port, halt_out
    signals_to_plot = [
        ('clk', 'Clock', 'step'),
        ('rst_n', 'Reset_n', 'step'),
        ('pc', 'PC', 'step_value'),
        ('r0', 'R0 (Accumulator)', 'step_value'),
        ('r1', 'R1 (Counter)', 'step_value'),
        ('r2', 'R2 (Product)', 'step_value'),
        ('r3', 'R3 (Addend)', 'step_value'),
        ('out_port', 'Out Port', 'step_value'),
        ('halt_out', 'Halt', 'step')
    ]
    
    fig, axes = plt.subplots(len(signals_to_plot), 1, figsize=(12, 10), sharex=True)
    plt.subplots_adjust(hspace=0.3)
    
    # Use standard styles
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    
    for idx, (sig_name, label, plot_type) in enumerate(signals_to_plot):
        ax = axes[idx]
        vals = cropped_vals[sig_name]
        
        # Grid
        ax.grid(True, which='both', color='#e2e8f0', linestyle='--', linewidth=0.5)
        
        if plot_type == 'step':
            # Binary signal
            # To draw a step function properly, we use where='post'
            ax.step(t, vals, where='post', color='#1a365d', linewidth=1.5)
            ax.set_ylim(-0.2, 1.2)
            ax.set_yticks([0, 1])
        elif plot_type == 'step_value':
            # Value signal (like PC, Registers)
            ax.step(t, vals, where='post', color='#2b6cb0', linewidth=1.5)
            # Add text values above the steps
            # Filter unique time steps to avoid overlap
            last_val = None
            for i in range(len(t) - 1):
                if vals[i] != last_val:
                    ax.text(t[i] + 1, vals[i] + 0.1, str(vals[i]), fontsize=8, color='#4a5568')
                    last_val = vals[i]
            ax.set_ylim(-0.5, 16.5)
            ax.set_yticks([0, 4, 8, 12, 16])
            
        ax.set_ylabel(label, fontsize=9, fontweight='bold', color='#2d3748', rotation=0, labelpad=15, ha='right')
        ax.tick_params(axis='y', labelsize=8)
        
        # Highlight background during active execution (rst_n == 1)
        # Find where rst_n changes from 0 to 1
        rst_n_vals = cropped_vals['rst_n']
        active_starts = t[np.where(rst_n_vals == 1)[0]]
        if len(active_starts) > 0:
            start_active = active_starts[0]
            # Find where halt_out goes to 1
            halt_starts = t[np.where(cropped_vals['halt_out'] == 1)[0]]
            end_active = halt_starts[0] if len(halt_starts) > 0 else t[-1]
            ax.axvspan(start_active, end_active, color='#f7fafc', alpha=0.5, zorder=-1)
            
    # Set x-axis labels
    axes[-1].set_xlabel('Time (ns)', fontsize=10, fontweight='bold', color='#2d3748')
    axes[-1].tick_params(axis='x', labelsize=9)
    axes[-1].set_xlim(0, end_time)
    
    # Title
    fig.suptitle('DẠNG SÓNG CHI TIẾT PHÉP NHÂN (MUL PROGRAM SIMULATION) - TKVM 4-BIT CPU', fontsize=12, fontweight='bold', color='#1a365d', y=0.96)
    
    # Add vertical dashed lines for each clock cycle (every 10ns starting from 12ns reset release)
    cycle_time = 12.0
    while cycle_time < end_time:
        for ax in axes:
            ax.axvline(cycle_time, color='#cbd5e0', linestyle=':', linewidth=0.8)
        cycle_time += 10.0
        
    # Save the plot
    os.makedirs('report_assets', exist_ok=True)
    os.makedirs('sim', exist_ok=True)
    plt.savefig('report_assets/waveform_cpu_top.png', dpi=300, bbox_inches='tight')
    plt.savefig('sim/waveform_cpu_top.png', dpi=300, bbox_inches='tight')
    print("Waveform plotted and saved to report_assets/waveform_cpu_top.png and sim/waveform_cpu_top.png")

if __name__ == '__main__':
    plot_mul()
