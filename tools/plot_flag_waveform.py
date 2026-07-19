# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np

def parse_vcd(vcd_path):
    signals = {
        '#': 'clk',
        '%': 'rst_n',
        '8': 'pc',
        ':': 'opcode',
        'C': 'flag_write',
        '.': 'zero',
        'K': 'zero_r',
        'B': 'halt'
    }
    
    # Store history of changes: time -> signal_name -> value
    time_series = []
    current_vals = {name: 0 for name in signals.values()}
    val_history = {name: [] for name in signals.values()}
    current_time = 0
    
    with open(vcd_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Time stamp
            if line.startswith('#'):
                new_time = int(line[1:])
                time_series.append(current_time)
                for name, val in current_vals.items():
                    val_history[name].append(val)
                current_time = new_time
                continue
            
            # Signal changes
            if line.startswith('b'):
                parts = line.split()
                if len(parts) == 2:
                    val_str, sym = parts
                    val_bin = val_str[1:]
                    if any(x in val_bin for x in ('x', 'z', 'X', 'Z')):
                        val = 0
                    else:
                        val = int(val_bin, 2)
                    if sym in signals:
                        current_vals[signals[sym]] = val
            elif line[0] in ('0', '1', 'x', 'z') and len(line) == 2:
                val_char, sym = line[0], line[1]
                if sym in signals:
                    if val_char in ('0', '1'):
                        current_vals[signals[sym]] = int(val_char)
                    else:
                        current_vals[signals[sym]] = 0
                        
    # Append final state
    time_series.append(current_time)
    for name, val in current_vals.items():
        val_history[name].append(val)
        
    return np.array(time_series), {k: np.array(v) for k, v in val_history.items()}

def plot_flag_test():
    vcd_path = 'cpu_top.vcd'
    if not os.path.exists(vcd_path):
        print("VCD file not found!")
        return
        
    time_series, val_history = parse_vcd(vcd_path)
    time_ns = time_series * 0.001  # Convert ps to ns
    
    # Find the start of the FLAG test (the 4th rising edge of rst_n)
    rst_n = val_history['rst_n']
    rising_edges = []
    for i in range(1, len(rst_n)):
        if rst_n[i-1] == 0 and rst_n[i] == 1:
            rising_edges.append(time_ns[i])
            
    if len(rising_edges) < 4:
        print(f"Could not find 4th rising edge of rst_n! Found: {rising_edges}")
        return
        
    start_time = rising_edges[3] - 12.0  # Show 12ns before rising edge (reset period)
    end_time = start_time + 120.0       # Plot 120ns total
    
    mask = (time_ns >= start_time) & (time_ns <= end_time)
    t = time_ns[mask] - start_time       # Offset time to start at 0
    
    cropped_vals = {}
    for name, vals in val_history.items():
        cropped_vals[name] = vals[mask]
        
    signals_to_plot = [
        ('clk', 'Clk', 'step'),
        ('rst_n', 'Rst_n', 'step'),
        ('pc', 'PC', 'step_value'),
        ('opcode', 'Opcode', 'step_value_4'),
        ('flag_write', 'FlagWrite', 'step'),
        ('zero', 'Zero (ALU)', 'step'),
        ('zero_r', 'Zero_r (Arch)', 'step'),
        ('halt', 'Halt', 'step')
    ]
    
    fig, axes = plt.subplots(len(signals_to_plot), 1, figsize=(11, 8.5), sharex=True)
    plt.subplots_adjust(hspace=0.4)
    
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    
    # Opcode mnemonics for the flag_test.asm program:
    # 0: LDI #5, 1: MOV R1, R0, 2: LDI #1, 3: DEC R0, 4: MOV R2, R1, 5: JZ TARGET
    # Target is at 9: LDI #12, 10: OUT R0, 11: HALT
    op_names = {
        0: 'NOP', 1: 'LOAD', 2: 'STORE', 3: 'LDI/MOV', 4: 'ADD', 5: 'SUB',
        6: 'AND', 7: 'OR', 8: 'XOR', 9: 'INC', 10: 'DEC', 11: 'JMP',
        12: 'JZ', 13: 'JN', 14: 'OUT', 15: 'HALT'
    }
    
    for idx, (sig_name, label, plot_type) in enumerate(signals_to_plot):
        ax = axes[idx]
        vals = cropped_vals[sig_name]
        
        ax.grid(True, which='both', color='#e2e8f0', linestyle='--', linewidth=0.5)
        
        if plot_type == 'step':
            ax.step(t, vals, where='post', color='#2b6cb0', linewidth=1.5)
            ax.set_ylim(-0.2, 1.2)
            ax.set_yticks([0, 1])
        elif plot_type == 'step_value':
            ax.step(t, vals, where='post', color='#1a365d', linewidth=1.5)
            last_val = None
            for i in range(len(t) - 1):
                if vals[i] != last_val:
                    ax.text(t[i] + 0.3, vals[i] + 0.1, str(vals[i]), fontsize=8, color='#2d3748')
                    last_val = vals[i]
            ax.set_ylim(-0.5, 12.5)
            ax.set_yticks([0, 3, 6, 9, 12])
        elif plot_type == 'step_value_4':
            ax.step(t, vals, where='post', color='#319795', linewidth=1.5)
            last_val = None
            for i in range(len(t) - 1):
                if vals[i] != last_val:
                    name = op_names.get(vals[i], str(vals[i]))
                    ax.text(t[i] + 0.3, vals[i] + 0.1, name, fontsize=8, color='#2d3748')
                    last_val = vals[i]
            ax.set_ylim(-0.5, 15.5)
            ax.set_yticks([3, 10, 12, 14, 15])
            
        ax.set_ylabel(label, fontsize=8, fontweight='bold', color='#2d3748', rotation=0, labelpad=15, ha='right')
        ax.tick_params(axis='y', labelsize=8)
        
    axes[-1].set_xlabel('Time offset from start of FLAG test (ns)', fontsize=9, fontweight='bold', color='#2d3748')
    axes[-1].tick_params(axis='x', labelsize=9)
    axes[-1].set_xlim(0, 120.0)
    
    fig.suptitle('DẠNG SÓNG KIỂM THỬ TÍNH NĂNG CHỐT CỜ CÓ ĐIỀU KIỆN (flag_write WAVEFORM)', fontsize=12, fontweight='bold', color='#1a365d', y=0.96)
    
    # Draw vertical lines at clock edges
    cycle_time = 12.0
    while cycle_time < 120.0:
        for ax in axes:
            ax.axvline(cycle_time, color='#cbd5e0', linestyle=':', linewidth=0.8)
        cycle_time += 10.0
        
    os.makedirs('report_assets', exist_ok=True)
    plt.savefig('report_assets/waveform_flag.png', dpi=300, bbox_inches='tight')
    print("FLAG test waveform plotted and saved to report_assets/waveform_flag.png")

if __name__ == '__main__':
    plot_flag_test()
