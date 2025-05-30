#!/usr/bin/env python3
"""
Basic Interference Example
==========================

This example demonstrates the fundamental concepts of the bright/dark photon model
by showing how interference patterns emerge from the superposition of bright and 
dark states with different phase relationships.

Key Concepts Illustrated:
- Basic wavefunction superposition
- Phase-dependent interference
- Amplitude ratio effects
- Visibility measurements

Author: David Coldeira
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path to import the simulator
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def basic_interference_demo():
    """
    Demonstrate basic interference between bright and dark states.
    """
    print("🌟 Basic Bright/Dark Interference Demo")
    print("=" * 50)
    
    # Define spatial coordinates
    x = np.linspace(-4, 4, 800)
    
    # Define bright and dark state wavefunctions
    def psi_bright(x, center=0.8, width=0.6):
        """Bright state: right-shifted Gaussian"""
        return np.exp(-((x - center)**2) / (2 * width**2))
    
    def psi_dark(x, center=-0.8, width=0.6):
        """Dark state: left-shifted Gaussian"""
        return np.exp(-((x + center)**2) / (2 * width**2))
    
    def total_wavefunction(x, alpha, beta_magnitude, beta_phase):
        """Combined bright + dark state"""
        beta = beta_magnitude * np.exp(1j * beta_phase)
        return alpha * psi_bright(x) + beta * psi_dark(x)
    
    def calculate_visibility(intensity):
        """Calculate fringe visibility V = (I_max - I_min)/(I_max + I_min)"""
        I_max, I_min = np.max(intensity), np.min(intensity)
        return (I_max - I_min) / (I_max + I_min) if I_max + I_min > 0 else 0
    
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Basic Bright/Dark Photon Interference', fontsize=16, fontweight='bold')
    
    # 1. Individual wavefunctions
    ax1 = axes[0, 0]
    psi_b = psi_bright(x)
    psi_d = psi_dark(x)
    
    ax1.plot(x, np.abs(psi_b)**2, 'cyan', linewidth=2, label='Bright State |ψ_B|²')
    ax1.plot(x, np.abs(psi_d)**2, 'magenta', linewidth=2, label='Dark State |ψ_D|²')
    ax1.plot(x, 0.5 * (np.abs(psi_b)**2 + np.abs(psi_d)**2), 'gray', 
             linewidth=2, linestyle='--', label='Classical Sum')
    
    ax1.set_title('Individual State Components')
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Probability Density')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Phase-dependent interference
    ax2 = axes[0, 1]
    phases = [0, np.pi/2, np.pi, 3*np.pi/2]
    colors = ['lime', 'orange', 'red', 'yellow']
    visibilities = []
    
    for phase, color in zip(phases, colors):
        psi_total = total_wavefunction(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
        intensity = np.abs(psi_total)**2
        visibility = calculate_visibility(intensity)
        visibilities.append(visibility)
        
        ax2.plot(x, intensity, color=color, linewidth=2,
                label=f'φ = {phase:.2f}, V = {visibility:.3f}')
    
    ax2.set_title('Phase-Dependent Interference')
    ax2.set_xlabel('Position')
    ax2.set_ylabel('Intensity')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Amplitude ratio effects
    ax3 = axes[1, 0]
    dark_amplitudes = np.linspace(0, 1, 5)
    
    for i, beta_mag in enumerate(dark_amplitudes):
        alpha = np.sqrt(1 - beta_mag**2)
        psi_total = total_wavefunction(x, alpha, beta_mag, np.pi/4)
        intensity = np.abs(psi_total)**2
        visibility = calculate_visibility(intensity)
        
        color = plt.cm.viridis(i / (len(dark_amplitudes) - 1))
        ax3.plot(x, intensity, color=color, linewidth=2,
                label=f'β = {beta_mag:.2f}, V = {visibility:.3f}')
    
    ax3.set_title('Effect of Dark State Amplitude')
    ax3.set_xlabel('Position')
    ax3.set_ylabel('Intensity')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Visibility vs phase relationship
    ax4 = axes[1, 1]
    phase_range = np.linspace(0, 4*np.pi, 100)
    visibility_curve = []
    
    for phase in phase_range:
        psi_total = total_wavefunction(x, 1/np.sqrt(2), 1/np.sqrt(2), phase)
        intensity = np.abs(psi_total)**2
        visibility_curve.append(calculate_visibility(intensity))
    
    ax4.plot(phase_range, visibility_curve, 'lime', linewidth=3)
    ax4.axhline(y=np.mean(visibility_curve), color='orange', linestyle='--',
               label=f'Average V = {np.mean(visibility_curve):.3f}')
    
    ax4.set_title('Visibility vs Dark State Phase')
    ax4.set_xlabel('Phase (radians)')
    ax4.set_ylabel('Fringe Visibility')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # Print key results
    print("\n📊 Key Results:")
    print(f"Average visibility across all phases: {np.mean(visibility_curve):.3f}")
    print(f"Maximum visibility: {np.max(visibility_curve):.3f}")
    print(f"Minimum visibility: {np.min(visibility_curve):.3f}")
    print("\n✨ Observation: Even when dark states can't be detected directly,")
    print("   they significantly influence the observable interference pattern!")

def theoretical_summary():
    """Print theoretical background for this example."""
    print("\n🔬 Theoretical Background")
    print("=" * 50)
    print("The bright/dark photon model proposes that:")
    print("• Photons exist as |ψ⟩ = α|B⟩ + β|D⟩")
    print("• Only |B⟩ states are directly detectable")
    print("• |D⟩ states influence interference through phase relationships")
    print("• Observable intensity: I(x) ∝ |α⟨x|B⟩ + β⟨x|D⟩|²")
    print("\nKey Predictions:")
    print("1. Interference visibility depends on both α and β")
    print("2. Dark state phase shifts affect observable patterns")
    print("3. Maximum visibility occurs at optimal α/β ratios")
    print("4. Some interference persists even with bright state decoherence")

if __name__ == "__main__":
    theoretical_summary()
    basic_interference_demo()
    print("\n🎯 Next Steps:")
    print("• Try double_slit_analysis.py for more complex interference")
    print("• Explore weak_measurement_demo.py for partial detection scenarios")
    print("• Modify parameters in this script to test your own ideas!")
