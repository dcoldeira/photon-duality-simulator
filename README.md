# Photon Duality Simulator: Bright/Dark State Interference Model

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Overview

This project presents a novel theoretical framework and computational simulator for quantum interference patterns based on **bright/dark photon states**. The model proposes that photons exist as superpositions of:

- **Bright states** (|B⟩): Directly detectable by measurement apparatus
- **Dark states** (|D⟩): Undetectable but influence interference through coherent evolution

This framework bridges multiple quantum mechanical interpretations while providing testable predictions for experimental validation.

## Theoretical Foundation

### Core Hypothesis

**Interference patterns arise from the interaction between "bright" (detectable) and "dark" (undetectable) photon states, where only bright states contribute directly to measurement outcomes.**

### Mathematical Formulation

The total photon state is expressed as:
```
|ψ⟩ = α|B⟩ + β|D⟩
```

Where:
- `α, β ∈ ℂ` with `|α|² + |β|² = 1` (normalization)
- Detection probability: `P_detect = |α|²`
- Interference intensity: `I(x) ∝ |α⟨x|B⟩ + β⟨x|D⟩|²`

The cross-term `α*β⟨x|B⟩*⟨x|D⟩` generates interference patterns even when only the bright component is directly measurable.

### Theoretical Connections

1. **Quantum Superposition**: Dark states represent unmeasured components of the wavefunction
2. **Pilot-Wave Theory**: Dark states act as guiding fields for bright particle detection
3. **Decoherence Theory**: Environmental interactions selectively affect bright vs. dark components
4. **Weak Measurement**: Partial collapse scenarios naturally emerge from this formalism

## Features

### Core Simulation Capabilities

- **Spatial Wavefunction Modeling**: Gaussian envelope functions with momentum components
- **Interference Pattern Generation**: Real-time computation of bright/dark state interactions  
- **Phase Relationship Analysis**: Dynamic visualization of how dark state phases affect observable patterns
- **Double-Slit Experiments**: Full simulation including path differences and fringe visibility
- **Weak Measurement Effects**: Modeling partial wavefunction collapse scenarios
- **Decoherence Modeling**: Environmental interaction effects on coherence

### Advanced Analysis Tools

- **Fringe Visibility Calculations**: Quantitative measure of interference quality
- **Phase Sweep Analysis**: Systematic study of parameter space
- **Component Decomposition**: Separate analysis of bright/dark contributions
- **Animated Visualizations**: Real-time parameter variation studies

## Installation & Usage

### Requirements
```bash
pip install numpy matplotlib scipy seaborn
```

### Quick Start
```python
from photon_simulator import PhotonDualitySimulator

# Initialize simulator
sim = PhotonDualitySimulator()

# Generate comprehensive analysis
fig = sim.create_comprehensive_plot()

# Run double-slit experiment
results = sim.double_slit_experiment(slit_separation=2.0)
print(f"Fringe visibility: {results['visibility']:.3f}")

# Create phase animation
anim, fig = sim.create_animation('phase')
```

## Experimental Predictions & Testable Hypotheses

### 1. Modified Interferometer Experiments

**Prediction**: Introduce selective decoherence that only affects bright states while preserving dark state coherence. Residual interference should persist even when bright paths are decohered.

**Test Setup**: Mach-Zehnder interferometer with polarization-selective weak measurement in one arm.

### 2. Dark-Channel Phase Control

**Prediction**: Controllable phase delays applied only to dark components should shift interference fringes in detectable patterns.

**Test Setup**: Encode dark states in orthogonal polarization or frequency modes outside detector bandwidth, then apply controlled phase shifts.

### 3. Post-Selection Experiments

**Prediction**: Weak measurement followed by post-selection should reveal dark state influence on detected photon statistics.

**Test Setup**: Use quantum eraser techniques to reconstruct dark path contributions through correlation analysis.

### 4. Visibility Scaling Laws

**Prediction**: Interference visibility should scale with the coherent product |α·β| rather than individual bright/dark amplitudes.

**Test Setup**: Systematically vary bright/dark amplitude ratios while maintaining total normalization.

## Current Simulation Results

The simulator demonstrates several key phenomena:

1. **Phase-Dependent Interference**: Dark state phase variations produce observable fringe shifts
2. **Visibility Enhancement**: Optimal bright/dark ratios maximize interference contrast
3. **Decoherence Resistance**: Dark states show differential robustness to environmental noise
4. **Weak Measurement Signatures**: Partial collapse scenarios produce characteristic distortions

## Planned Extensions

### Near-term Development
- [ ] **Entanglement Support**: Multi-photon bright/dark state correlations
- [ ] **Realistic Detector Models**: Quantum efficiency and noise characteristics  
- [ ] **3D Spatial Dynamics**: Full vectorial electromagnetic field treatment
- [ ] **Temporal Evolution**: Time-dependent Schrödinger equation integration

### Long-term Research Directions
- [ ] **Field Theory Extension**: Second-quantized bright/dark field operators
- [ ] **Bell Test Scenarios**: Bright/dark state non-locality experiments
- [ ] **Cavity QED**: Bright/dark state interactions with optical resonators
- [ ] **Machine Learning**: Pattern recognition for dark state signatures

## Contributing

We welcome contributions from the quantum optics, foundations of quantum mechanics, and computational physics communities. Areas of particular interest:

- **Experimental Design**: Proposals for bright/dark state detection schemes
- **Theoretical Extensions**: Mathematical refinements and new predictions  
- **Code Optimization**: Performance improvements for large-scale simulations
- **Visualization**: Enhanced plotting and animation capabilities

## Literature & Related Work

This model connects to several established areas:

- **Bohmian Mechanics**: Pilot-wave guidance mechanisms
- **Consistent Histories**: Alternative quantum interpretation frameworks  
- **Quantum Darwinism**: Environment-induced superselection rules
- **Weak Measurement Theory**: Partial information extraction protocols

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Citation

If you use this simulator in your research, please cite:

```bibtex
@software{photon_duality_simulator,
  title={Photon Duality Simulator: Bright/Dark State Interference Model},
  author={[Your Name]},
  year={2025},
  url={https://github.com/[username]/photon-duality-simulator}
}
```

## Contact

[For questions, collaborations, or experimental proposals, please open an issue or contact me](dcoldeira@tuta.io).

---

*"The dark states guide the bright, creating patterns in the observable world through their invisible dance."*