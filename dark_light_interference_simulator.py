#!/usr/bin/env python3
"""
Dark/Light Interference Simulator
A simplified version based on your original code with enhancements.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Configuration
plt.style.use('dark_background')  # Dark theme for better visibility

def main():
    print("🌟 Starting Dark/Light Photon Interference Simulator...")
    
    try:
        # Define spatial range
        x = np.linspace(-5, 5, 1000)
        print("✓ Spatial grid initialized")

        # Bright and dark state wavefunctions
        def psi_bright(x, d=1.0, sigma=0.5):
            return np.exp(-((x - d)**2) / (2 * sigma**2))

        def psi_dark(x, d=1.0, sigma=0.5):
            return np.exp(-((x + d)**2) / (2 * sigma**2))

        # Superposition of bright and dark components
        def total_wavefunction(x, alpha=1/np.sqrt(2), beta_mag=1/np.sqrt(2), beta_phase=0.0):
            beta = beta_mag * np.exp(1j * beta_phase)
            return alpha * psi_bright(x) + beta * psi_dark(x)

        # Calculate observable intensity
        def intensity(x, alpha, beta_mag, beta_phase):
            psi = total_wavefunction(x, alpha, beta_mag, beta_phase)
            return np.abs(psi)**2

        print("✓ Wavefunction models defined")

        # Create static analysis first
        create_static_analysis(x, intensity)
        
        # Create animation
        create_animation(x, intensity)
        
        print("✓ Simulation complete!")
        
    except ImportError as e:
        print(f"❌ Missing package: {e}")
        print("Please install: pip install numpy matplotlib")
    except Exception as e:
        print(f"❌ Error: {e}")

def create_static_analysis(x, intensity_func):
    """Create static plots showing different aspects of the model."""
    print("📊 Creating static analysis plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Bright/Dark Photon Interference Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Different phase values
    ax1 = axes[0, 0]
    phases = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
    colors = ['cyan', 'yellow', 'magenta', 'lime', 'orange']
    
    for phase, color in zip(phases, colors):
        y = intensity_func(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
        ax1.plot(x, y, color=color, label=f'φ = {phase:.2f}', linewidth=2)
    
    ax1.set_title('Interference vs Dark State Phase')
    ax1.set_xlabel('Position (x)')
    ax1.set_ylabel('Intensity')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Different amplitude ratios
    ax2 = axes[0, 1]
    dark_amplitudes = [0.1, 0.3, 0.5, 0.7, 0.9]
    
    for dark_amp in dark_amplitudes:
        bright_amp = np.sqrt(1 - dark_amp**2)
        y = intensity_func(x, bright_amp, dark_amp, np.pi/4)
        ax2.plot(x, y, label=f'β = {dark_amp:.1f}', linewidth=2)
    
    ax2.set_title('Effect of Dark State Amplitude')
    ax2.set_xlabel('Position (x)')
    ax2.set_ylabel('Intensity')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Component analysis
    ax3 = axes[1, 0]
    
    # Individual components
    psi_b = np.exp(-((x - 1)**2) / (2 * 0.5**2))
    psi_d = np.exp(-((x + 1)**2) / (2 * 0.5**2))
    
    ax3.plot(x, np.abs(psi_b)**2, 'cyan', label='Bright State |ψ_B|²', linewidth=2)
    ax3.plot(x, np.abs(psi_d)**2, 'magenta', label='Dark State |ψ_D|²', linewidth=2)
    ax3.plot(x, intensity_func(x, 1/np.sqrt(2), 1/np.sqrt(2), 0), 
             'lime', label='Combined |ψ_total|²', linewidth=2)
    
    ax3.set_title('Individual vs Combined States')
    ax3.set_xlabel('Position (x)')
    ax3.set_ylabel('Probability Density')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Visibility analysis
    ax4 = axes[1, 1]
    phases_fine = np.linspace(0, 4*np.pi, 200)
    visibilities = []
    
    for phase in phases_fine:
        y = intensity_func(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
        visibility = (np.max(y) - np.min(y)) / (np.max(y) + np.min(y))
        visibilities.append(visibility)
    
    ax4.plot(phases_fine, visibilities, 'lime', linewidth=2)
    ax4.set_title('Fringe Visibility vs Dark Phase')
    ax4.set_xlabel('Dark State Phase (rad)')
    ax4.set_ylabel('Visibility')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    print("✓ Static analysis displayed")

def create_animation(x, intensity_func):
    """Create the animated visualization."""
    print("🎬 Creating phase animation...")
    
    # Plot setup
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    line, = ax.plot(x, intensity_func(x, 1/np.sqrt(2), 1/np.sqrt(2), 0.0), 
                   'cyan', linewidth=3)
    ax.set_ylim(0, 2)
    ax.set_xlim(-5, 5)
    ax.set_xlabel('Position (x)', fontsize=12, color='white')
    ax.set_ylabel('Intensity', fontsize=12, color='white')
    ax.grid(True, alpha=0.3)
    ax.tick_params(colors='white')
    
    # Animation update function
    def update(frame):
        phase = 2 * np.pi * frame / 100
        y = intensity_func(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
        line.set_ydata(y)
        ax.set_title(f"Bright/Dark Interference | Dark Phase = {phase:.2f} rad", 
                    fontsize=14, color='white', fontweight='bold')
        return line,

    # Create animation
    anim = FuncAnimation(fig, update, frames=100, interval=100, blit=True)
    
    print("✓ Animation created! Close the window to continue...")
    
    # Show animation
    plt.show()
    
    # Option to save as GIF
    print("\n💾 Save animation as GIF? (y/n): ", end="")
    try:
        save_choice = input().lower().strip()
        if save_choice == 'y':
            print("Saving animation... (this may take a moment)")
            anim.save("bright_dark_interference.gif", writer=PillowWriter(fps=10))
            print("✓ Animation saved as 'bright_dark_interference.gif'")
    except:
        print("Skipping save option")

def print_theory_summary():
    """Print a summary of the theoretical framework."""
    print("\n" + "="*70)
    print("🔬 BRIGHT/DARK PHOTON INTERFERENCE MODEL")
    print("="*70)
    print("Theory: Photons exist as superpositions of:")
    print("  • Bright states |B⟩: Detectable by measurement apparatus")
    print("  • Dark states |D⟩: Undetectable but influence interference")
    print()
    print("Mathematical Framework:")
    print("  |ψ⟩ = α|B⟩ + β|D⟩")
    print("  Detection probability: P = |α|²")
    print("  Interference: I(x) ∝ |α⟨x|B⟩ + β⟨x|D⟩|²")
    print()
    print("Key Predictions:")
    print("  1. Interference persists even with bright state decoherence")
    print("  2. Dark state phase shifts affect observable patterns")
    print("  3. Optimal visibility at specific α/β ratios")
    print("="*70)

if __name__ == "__main__":
    print_theory_summary()
    main()
    print("\n✨ Simulation complete! Thank you for exploring quantum interference!")