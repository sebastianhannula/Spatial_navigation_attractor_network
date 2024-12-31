# Spatial_navigation_attractor_network
Here I implement a discrete time, low number of neuron- version of attractor network model introduced in Ocko et al. Emergent elasticity in the neural code for space.

The animations in this project were created using the Manim library, a community-driven Python framework for creating mathematical animations. For more information on Manim, visit their GitHub repository: [Manim GitHub](https://github.com/ManimCommunity/manim).

## Insect Central Complex Model for Spatial Navigation

The insect central complex (CX) is a region in the brain of arthropods that plays a crucial role in spatial navigation and orientation. Acting like a compass, the CX integrates sensory inputs with self-motion cues, enabling insects to navigate complex environments efficiently. Studies have shown that the CX is responsible for encoding the insect’s heading direction, which aligns with their ability to maintain a stable course even in the absence of prominent external cues. This navigational ability is akin to how mammals use grid cells in the entorhinal cortex to map space, but the CX achieves this with a simpler and more compact neural architecture.

In this project, I have implemented a discrete-time model inspired by Ocko et al.’s (2018) paper. The paper explores how attractor dynamics, path integration, and Hebbian plasticity can create self-consistent internal maps of an environment, solving a fundamental problem of spatial navigation. The model demonstrates how neural circuits integrate self-motion (path integration) with sensory landmarks to update and maintain spatial representations. 

This repository contains a simplified, discrete-time version of the model with a reduced neuron count, designed primarily for pedagogical purposes. The goal is to provide a conceptual understanding of the principles behind the model while making the system computationally lightweight and easy to visualize. Along with the model, I have created Manim animations to illustrate how the system evolves during navigation, highlighting key aspects such as attractor dynamics and path-dependent deformations.

Below an example animation is included that shows the full process of learning a simple one dimensional environment. The brown ball at the bottom represents the learner that moves along the environment as shown and above it the ring attractor neural network activations are shown. In the beginning the connections are randomly initialized and during the animation the learning can be seen. For a more detailed explanation of the simulation and animation, refer to [this PowerPoint presentation](documents/presentation.pptx).

![Simulation Animation](documents/simulation.gif)

## References

- Original Paper: Ocko SA, Hardcastle K, Giocomo LM, Ganguli S. Emergent elasticity in the neural code for space. Proc Natl Acad Sci, 115(50):E11798-E11806, doi: 10.1073/pnas.1805959115. 2018 Dec 11.


