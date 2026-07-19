# -*- coding: utf-8 -*-
import os
import matplotlib.pyplot as plt
import numpy as np

def parse_vcd(vcd_path):
    signals = {
        '#': 'clk',
        '%': 'rst_n',
        '8': 'pc',
        '@': 'instruction',
        ':': 'opcode',
        '1': 'reg_write',
        '<': 'mem_write',
        '?': 'mem_read',
        '=': 'mem_to_reg',
        'D': 'alu_src',
        'F': 'alu_op',
        '6': 'pc_src',
        'B': 'halt',
        '.': 'zero',
        'C': 'carry',
        ';': 'negative'
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

def plot_control():
    vcd_path = 'cpu_top.vcd'
    if not os.path.exists(vcd_path):
        print("VCD file not found!")
        return
        
    time_series, val_history = parse_vcd(vcd_path)
    time_ns = time_series * 0.001
    
    # We want to plot a portion of the MUL program to show control and memory changes
    # Let's crop from 0 to 100ns (first 10 clock cycles)
    end_time = 100.0
    mask = time_ns <= end_time
    t = time_ns[mask]
    
    cropped_vals = {}
    for name, vals in val_history.items():
        cropped_vals[name] = vals[mask]
        
    signals_to_plot = [
        ('clk', 'Clk', 'step'),
        ('rst_n', 'Rst_n', 'step'),
        ('pc', 'PC', 'step_value'),
        ('reg_write', 'RegWrite', 'step'),
        ('mem_read', 'MemRead', 'step'),
        ('mem_write', 'MemWrite', 'step'),
        ('mem_to_reg', 'Mem2Reg', 'step'),
        ('alu_src', 'ALUSrc', 'step'),
        ('alu_op', 'ALUOp', 'step_value_3'),
        ('pc_src', 'PCSrc', 'step'),
        ('zero', 'ZeroFlag', 'step'),
        ('carry', 'CarryFlag', 'step'),
        ('negative', 'NegFlag', 'step'),
    ]
    
    fig, axes = plt.subplots(len(signals_to_plot), 1, figsize=(12, 11), sharex=True)
    plt.subplots_adjust(hspace=0.35)
    
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    
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
                    ax.text(t[i] + 0.5, vals[i] + 0.1, str(vals[i]), fontsize=8, color='#2d3748')
                    last_val = vals[i]
            ax.set_ylim(-0.5, 16.5)
            ax.set_yticks([0, 4, 8, 12, 16])
        elif plot_type == 'step_value_3':
            ax.step(t, vals, where='post', color='#319795', linewidth=1.5)
            last_val = None
            for i in range(len(t) - 1):
                if vals[i] != last_val:
                    ax.text(t[i] + 0.5, vals[i] + 0.1, bin(vals[i])[2:].zfill(3), fontsize=8, color='#2d3748')
                    last_val = vals[i]
            ax.set_ylim(-0.2, 7.5)
            ax.set_yticks([0, 2, 4, 6])
            
        ax.set_ylabel(label, fontsize=9, fontweight='bold', color='#2d3748', rotation=0, labelpad=15, ha='right')
        ax.tick_params(axis='y', labelsize=8)
        
    axes[-1].set_xlabel('Time (ns)', fontsize=10, fontweight='bold', color='#2d3748')
    axes[-1].tick_params(axis='x', labelsize=9)
    axes[-1].set_xlim(0, end_time)
    
    fig.suptitle('SÓNG CHI TIẾT TÍN HIỆU ĐIỀU KHIỂN & BỘ NHỚ (CONTROL & MEMORY WAVEFORM) - TKVM 4-BIT CPU', fontsize=12, fontweight='bold', color='#1a365d', y=0.96)
    
    cycle_time = 12.0
    while cycle_time < end_time:
        for ax in axes:
            ax.axvline(cycle_time, color='#cbd5e0', linestyle=':', linewidth=0.8)
        cycle_time += 10.0
        
    os.makedirs('report_assets', exist_ok=True)
    os.makedirs('sim', exist_ok=True)
    plt.savefig('report_assets/waveform_control.png', dpi=300, bbox_inches='tight')
    plt.savefig('sim/waveform_control.png', dpi=300, bbox_inches='tight')
    print("Control waveform plotted and saved to report_assets/waveform_control.png and sim/waveform_control.png")

if __name__ == '__main__':
    plot_control()
