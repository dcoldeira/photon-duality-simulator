#!/usr/bin/env python3
"""
Weak Measurement Demonstration
==============================

This example explores how weak measurements interact differently with bright 
and dark photon states, providing a potential experimental pathway to test 
the bright/dark model.

Key Concepts:
- Weak measurement theory in bright/dark framework
- Selective state collapse scenarios
- Post-selection effects
- Anomalous weak values
- Experimental design implications

Author: David Coldeira
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class WeakMeasurementSimulator:
    """
    Simulate weak measurements in the bright/dark photon framework.
    """
    
    def __init__(self, x_range=(-5, 5), num_points=1000):
        self.x = np.linspace(x_range[0], x_range[1], num_points)
        self.dx = self.x[1] - self.x[0]
        
    def initial_state(self, alpha=1/np.sqrt(2), beta=1/np.sqrt(2), beta_phase=0):
        """Create initial bright/dark superposition state."""
        # Bright state: right-localized
        psi_bright = np.exp(-((self.x - 1.5)**2) / (2 * 0.5**2))
        
        # Dark state: left-localized with phase
        psi_dark = np.exp(-((self.x + 1.5)**2) / (2 * 0.5**2)) * \
                  np.exp(1j * beta_phase)
        
        # Total state
        psi_total = alpha * psi_bright + beta * psi_dark
        
        # Normalize
        norm = np.sqrt(np.trapz(np.abs(psi_total)**2, self.x))
        psi_total /= norm
        
        return {
            'psi_total': psi_total,
            'psi_bright': alpha * psi_bright / norm,
            'psi_dark': beta * psi_dark / norm,
            'alpha': alpha,
            'beta': beta
        }
    
    def weak_measurement_operator(self, coupling_strength=0.1, measurement_position=0.0,
                                 measurement_width=1.0, only_bright=True):
        """
        Create weak measurement operator.
        
        Args:
            coupling_strength: How strongly the measurement disturbs the state
            measurement_position: Where the measurement apparatus is located
            measurement_width: Spatial extent of measurement interaction
            only_bright: Whether measurement only affects bright states
        """
        # Gaussian measurement operator
        measurement_profile = np.exp(-((self.x - measurement_position)**2) / 
                                    (2 * measurement_width**2))
        
        # Weak measurement causes phase shifts proportional to position
        phase_shift = coupling_strength * measurement_profile * self.x
        
        return {
            'operator': np.exp(1j * phase_shift),
            'profile': measurement_profile,
            'only_bright': only_bright
        }
    
    def apply_weak_measurement(self, state, measurement):
        """Apply weak measurement to the state."""
        if measurement['only_bright']:
            # Only bright states interact with measurement apparatus
            psi_bright_after = state['psi_bright'] * measurement['operator']
            psi_dark_after = state['psi_dark']  # Unchanged
        else:
            # Both components interact (standard quantum mechanics)
            psi_bright_after = state['psi_bright'] * measurement['operator']
            psi_dark_after = state['psi_dark'] * measurement['operator']
        
        # Total wavefunction after measurement
        psi_total_after = psi_bright_after + psi_dark_after
        
        # Renormalize
        norm = np.sqrt(np.trapz(np.abs(psi_total_after)**2, self.x))
        if norm > 0:
            psi_total_after /= norm
            psi_bright_after /= norm
            psi_dark_after /= norm
        
        return {
            'psi_total': psi_total_after,
            'psi_bright': psi_bright_after,
            'psi_dark': psi_dark_after
        }
    
    def post_selection(self, state, selection_region):
        """
        Perform post-selection on measurement outcomes.
        
        Args:
            state: quantum state after measurement
            selection_region: (x_min, x_max) for post-selection
        """
        x_min, x_max = selection_region
        mask = (self.x >= x_min) & (self.x <= x_max)
        
        # Calculate selection probability
        selection_prob = np.trapz(np.abs(state['psi_total'][mask])**2, 
                                 self.x[mask])
        
        # Post-selected state (renormalized to selected region)
        psi_selected = state['psi_total'].copy()
        psi_selected[~mask] = 0
        
        if selection_prob > 0:
            psi_selected /= np.sqrt(selection_prob)
        
        return {
            'psi_selected': psi_selected,
            'selection_probability': selection_prob
        }
    
    def calculate_weak_value(self, pre_state, post_state, observable):
        """
        Calculate anomalous weak value.
        
        Weak value = ⟨ψ_f|A|ψ_i⟩ / ⟨ψ_f|ψ_i⟩
        """
        # Overlap between post and pre states
        overlap = np.trapz(np.conj(post_state) * pre_state, self.x)
        
        # Expectation value of observable
        expectation = np.trapz(np.conj(post_state) * observable * pre_state, self.x)
        
        if np.abs(overlap) > 1e-12:
            weak_value = expectation / overlap
        else:
            weak_value = complex(np.inf)
        
        return weak_value
    
    def momentum_operator(self, psi):
        """Calculate action of momentum operator -i*d/dx on wavefunction."""
        # Finite difference approximation
        dpsi_dx = np.gradient(psi, self.dx)
        return -1j * dpsi_dx

def run_weak_measurement_demo():
    """Run comprehensive weak measurement demonstration."""
    print("🔬 Weak Measurement in Bright/Dark Framework")
    print("=" * 60)
    
    sim = WeakMeasurementSimulator()
    
    # Create figure
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Weak Measurement: Bright vs Dark State Interactions', 
                 fontsize=16, fontweight='bold')
    
    # Initial state
    initial = sim.initial_state(alpha=1/np.sqrt(2), beta=1/np.sqrt(2), 
                               beta_phase=np.pi/4)
    
    # 1. Initial state components
    ax1 = axes[0, 0]
    ax1.plot(sim.x, np.abs(initial['psi_total'])**2, 'lime', 
             linewidth=2, label='Total State')
    ax1.plot(sim.x, np.abs(initial['psi_bright'])**2, 'cyan', 
             linewidth=2, alpha=0.7, label='Bright Component')
    ax1.plot(sim.x, np.abs(initial['psi_dark'])**2, 'magenta', 
             linewidth=2, alpha=0.7, label='Dark Component')
    
    ax1.set_title('Initial State Preparation')
    ax1.set_xlabel('Position')
    ax1.set_ylabel('Probability Density')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. Weak measurement operators
    ax2 = axes[0, 1]
    
    