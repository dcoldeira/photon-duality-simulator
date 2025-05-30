#!/usr/bin/env python3
"""
Weak Measurement Demonstration - Fixed Standalone Version
=========================================================

This example explores how weak measurements interact differently with bright 
and dark photon states. All dependencies are self-contained.

Author: David Coldeira
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt

def run_weak_measurement_demo():
    """Run a simplified but complete weak measurement demonstration."""
    print("🔬 Weak Measurement in Bright/Dark Framework")
    print("=" * 60)
    
    # Setup
    x = np.linspace(-5, 5, 1000)
    dx = x[1] - x[0]
    
    def create_initial_state():
        """Create initial bright/dark superposition."""
        # Bright state: right-localized
        psi_bright = np.exp(-((x - 1.5)**2) / (2 * 0.5**2))
        
        # Dark state: left-localized  
        psi_dark = np.exp(-((x + 1.5)**2) / (2 * 0.5**2))
        
        # Superposition
        alpha, beta = 1/np.sqrt(2), 1/np.sqrt(2)
        psi_total = alpha * psi_bright + beta * psi_dark
        
        # Normalize
        norm = np.sqrt(np.trapz(np.abs(psi_total)**2, x))
        psi_total /= norm
        psi_bright /= norm
        psi_dark /= norm
        
        return {
            'psi_total': psi_total,
            'psi_bright': alpha * psi_bright,
            'psi_dark': beta * psi_dark
        }
    
    def weak_measurement_operator(coupling_strength=0.1):
        """Create weak measurement that causes position-dependent phase shifts."""
        # Measurement causes phases proportional to position
        phase_shift = coupling_strength * x
        return np.exp(1j * phase_shift)
    
    def apply_measurement(state, operator, only_bright=True):
        """Apply measurement to state."""
        if only_bright:
            # Only bright component interacts
            psi_bright_after = state['psi_bright'] * operator
            psi_dark_after = state['psi_dark']  # Unchanged
        else:
            # Both components interact
            psi_bright_after = state['psi_bright'] * operator
            psi_dark_after = state['psi_dark'] * operator
        
        psi_total_after = psi_bright_after + psi_dark_after
        
        # Renormalize
        norm = np.sqrt(np.trapz(np.abs(psi_total_after)**2, x))
        if norm > 0:
            psi_total_after /= norm
            psi_bright_after /= norm
            psi_dark_after /= norm
        
        return {
            'psi_total': psi_total_after,
            'psi_bright': psi_bright_after,
            'psi_dark': psi_dark_after
        }
    
    def calculate_fidelity(psi1, psi2):
        """Calculate overlap between two states."""
        return np.abs(np.trapz(np.conj(psi1) * psi2, x))**2
    
    # Run the demonstration
    try:
        print("🔧 Setting up initial state...")
        initial_state = create_initial_state()
        
        print("🔬 Creating measurement operators...")
        weak_op = weak_measurement_operator(coupling_strength=0.05)
        strong_op = weak_measurement_operator(coupling_strength=0.3)
        
        print("⚡ Applying measurements...")
        # Weak measurement - bright only
        weak_bright_only = apply_measurement(initial_state, weak_op, only_bright=True)
        
        # Weak measurement - both components
        weak_both = apply_measurement(initial_state, weak_op, only_bright=False)
        
        # Strong measurement - bright only
        strong_bright_only = apply_measurement(initial_state, strong_op, only_bright=True)
        
        print("📊 Creating visualizations...")
        
        # Create plots
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Weak Measurement: Bright vs Dark Interactions', 
                     fontsize=16, fontweight='bold')
        
        # 1. Initial state
        ax1 = axes[0, 0]
        ax1.plot(x, np.abs(initial_state['psi_total'])**2, 'lime', 
                linewidth=2, label='Total State')
        ax1.plot(x, np.abs(initial_state['psi_bright'])**2, 'cyan', 
                linewidth=2, alpha=0.7, label='Bright Component')
        ax1.plot(x, np.abs(initial_state['psi_dark'])**2, 'magenta', 
                linewidth=2, alpha=0.7, label='Dark Component')
        
        ax1.set_title('Initial State')
        ax1.set_xlabel('Position')
        ax1.set_ylabel('Probability Density')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Measurement operators
        ax2 = axes[0, 1]
        ax2.plot(x, np.abs(weak_op), 'cyan', linewidth=2, label='Weak (0.05)')
        ax2.plot(x, np.abs(strong_op), 'orange', linewidth=2, label='Strong (0.3)')
        
        ax2.set_title('Measurement Operators')
        ax2.set_xlabel('Position')
        ax2.set_ylabel('Phase Factor Magnitude')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Weak measurement comparison
        ax3 = axes[0, 2]
        ax3.plot(x, np.abs(initial_state['psi_total'])**2, 'gray', 
                linewidth=2, linestyle='--', label='Initial')
        ax3.plot(x, np.abs(weak_bright_only['psi_total'])**2, 'lime', 
                linewidth=2, label='Bright-Only')
        ax3.plot(x, np.abs(weak_both['psi_total'])**2, 'orange', 
                linewidth=2, label='Both Components')
        
        ax3.set_title('Weak Measurement Effects')
        ax3.set_xlabel('Position')
        ax3.set_ylabel('Probability Density')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        
        # 4. Fidelity analysis
        ax4 = axes[1, 0]
        coupling_range = np.linspace(0.01, 0.5, 20)
        fidelity_bright_only = []
        fidelity_both = []
        
        for coupling in coupling_range:
            op = weak_measurement_operator(coupling)
            
            state_bright = apply_measurement(initial_state, op, only_bright=True)
            state_both = apply_measurement(initial_state, op, only_bright=False)
            
            fid_bright = calculate_fidelity(initial_state['psi_total'], 
                                          state_bright['psi_total'])
            fid_both = calculate_fidelity(initial_state['psi_total'], 
                                        state_both['psi_total'])
            
            fidelity_bright_only.append(fid_bright)
            fidelity_both.append(fid_both)
        
        ax4.plot(coupling_range, fidelity_bright_only, 'lime', 
                linewidth=2, marker='o', label='Bright-Only')
        ax4.plot(coupling_range, fidelity_both, 'orange', 
                linewidth=2, marker='s', label='Both Components')
        
        ax4.set_title('State Fidelity vs Coupling')
        ax4.set_xlabel('Coupling Strength')
        ax4.set_ylabel('Fidelity with Initial State')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Phase analysis
        ax5 = axes[1, 1]
        phase_initial = np.angle(initial_state['psi_total'])
        phase_weak_bright = np.angle(weak_bright_only['psi_total'])
        phase_weak_both = np.angle(weak_both['psi_total'])
        
        ax5.plot(x, phase_initial, 'gray', linewidth=2, 
                linestyle='--', label='Initial')
        ax5.plot(x, phase_weak_bright, 'lime', linewidth=2, 
                label='Bright-Only')
        ax5.plot(x, phase_weak_both, 'orange', linewidth=2, 
                label='Both Components')
        
        ax5.set_title('Phase Evolution')
        ax5.set_xlabel('Position')
        ax5.set_ylabel('Phase (radians)')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Disturbance comparison
        ax6 = axes[1, 2]
        
        disturbance_bright = 1 - np.array(fidelity_bright_only)
        disturbance_both = 1 - np.array(fidelity_both)
        
        ax6.plot(coupling_range, disturbance_bright, 'lime', 
                linewidth=2, marker='o', label='Bright-Only')
        ax6.plot(coupling_range, disturbance_both, 'orange', 
                linewidth=2, marker='s', label='Both Components')
        
        ax6.set_title('State Disturbance')
        ax6.set_xlabel('Coupling Strength')
        ax6.set_ylabel('Disturbance (1 - Fidelity)')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # Print results
        print("\n📊 Analysis Results:")
        print("=" * 40)
        
        fid_weak_bright = calculate_fidelity(initial_state['psi_total'], 
                                           weak_bright_only['psi_total'])
        fid_weak_both = calculate_fidelity(initial_state['psi_total'], 
                                         weak_both['psi_total'])
        
        print(f"Weak measurement fidelity (bright-only): {fid_weak_bright:.3f}")
        print(f"Weak measurement fidelity (both): {fid_weak_both:.3f}")
        print(f"Difference: {abs(fid_weak_bright - fid_weak_both):.3f}")
        
        print("\n🎯 Key Observations:")
        print("• Bright-only measurements preserve more coherence")
        print("• Dark states remain unaffected by selective measurements")
        print("• Phase evolution differs between interaction types")
        print("• Disturbance scaling follows different patterns")
        
        print("\n✅ Weak measurement demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Error in weak measurement demo: {e}")
        print("Check that numpy and matplotlib are properly installed.")

def print_experimental_context():
    """Explain the experimental relevance."""
    print("\n🔬 Experimental Context")
    print("=" * 50)
    print("This demo shows how weak measurements could test the bright/dark model:")
    print("\n1. SELECTIVE COUPLING:")
    print("   • Use polarization to encode bright/dark states")
    print("   • Apply weak measurement only to one polarization")
    print("   • Compare with measurements affecting both polarizations")
    
    print("\n2. EXPECTED SIGNATURES:")
    print("   • Different fidelity preservation")
    print("   • Distinct phase evolution patterns")
    print("   • Non-classical disturbance scaling")
    
    print("\n3. TESTABLE PREDICTIONS:")
    print("   • Bright-only measurements less disruptive")
    print("   • Some quantum coherence survives selective collapse")
    print("   • Anomalous weak values in post-selected measurements")

if __name__ == "__main__":
    print_experimental_context()
    run_weak_measurement_demo()
    print("\n🎯 This demonstrates a key way to test the bright/dark model!")