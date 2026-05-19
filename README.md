## EnSight Haemodynamics

Automate the post-processing of haemodynamic simulations in ANSYS EnSight. Scripted based on the syntax standard published in ANSYS EnSight Interface Manual 23R2. 

## `Shear.py`

Calculating wall shear related haemodynamic matrices.

| **Quantity**         | **Equation** | **Dimension** | **Description** |
|----------------------|--------------|--------------|--------------|
| **Time Averaged Wall Shear Stress** | $$\displaystyle \mathrm{TAWSS} = \dfrac{1}{T} \int_{0}^{T} \lvert \vec{\tau}_{w} \rvert \mathrm{d}t$$ | [Pa] | Shear stress averaged over the cardiac cycle |
| **Oscillatory Shear Index** | $$\displaystyle \mathrm{OSI} = \frac{1}{2}  \left( 1 - \dfrac{\lvert \int_{0}^{T} \vec{\tau_{w}} \mathrm{d}t \rvert}{ \int_{0}^{T} \lvert \vec{\tau}_{w} \rvert \ \mathrm{d}t} \right)$$ | non-dim | Change of direction of the wall shear stress vector from the primary direction of flow. |
| **Transverse Wall Shear Stress** | $$\displaystyle \mathrm{TransWSS} = \frac{1}{T} \int_{0}^{T} \left \lvert {\vec{\tau_{w}}} \cdot \left( \hat{n} \times \frac{\int_{0}^{T} {\vec{\tau_{w}}} \cdot \mathrm{d}t}{\lvert \int_{0}^{T}  {\vec{\tau_{w}}} \cdot \mathrm{d}t \rvert} \right) \right \rvert \mathrm{d}t$$ | [Pa] | Shear stress vector in perpendicular direction to the main flow direction |
| **Endothelial Cell Activation Potential** | $$\displaystyle \mathrm{ECAP} = \frac{\mathrm{OSI}}{\mathrm{TAWSS}}$$ | [Pa<sup>-1</sup>] | Synthetic metric to identify regions at a higher risk of thrombus formation |
| **Relative Residence Time** | $$\displaystyle \mathrm{RRT} = \frac{1}{(1 - 2 \cdot \mathrm{OSI}) \cdot \mathrm{TAWSS}}.$$ | [Pa<sup>-1</sup>] | Relative time that a blood particle resides at a certain location at the vessel wall |
| **Cross Flow Index** | $$\displaystyle \mathrm{CFI} = \frac{1}{T} \int_{0}^{T} \left \lvert \frac{{\vec{\tau_{w}}}}{{\lvert \vec{\tau_{w}} \rvert}} \cdot \left( \hat{n} \times \frac{\int_{0}^{T} {\vec{\tau_{w}}} \cdot \mathrm{d}t}{\lvert \int_{0}^{T}  {\vec{\tau_{w}}} \cdot \mathrm{d}t \rvert} \right) \right \rvert \mathrm{d}t$$ | non-dim | The TransWSS normalized for the time-averaged wall shear stress |

Reference
> Sengupta, S.; Zhu, Y.; Hamady, M.; Xu, X.Y. Evaluating the Haemodynamic Performance of Endografts for Complex Aortic Arch Repair. Bioengineering 2022, 9, 573. [https://doi.org/10.3390/bioengineering9100573](https://doi.org/10.3390/bioengineering9100573)

### `DispForces.py`
| **Quantity**         | **Equation** | **Dimension** | **Description** |
|----------------------|--------------|--------------|--------------|
| **Displacement Force** | $$\displaystyle F_{d, i} = F_{p, i} + F_{\mathrm{wss}, i} = \int \limits_{S} p \cdot n_i \ \mathrm{d}S + \int \limits_{S} \left( - \mu \frac{\partial u}{\partial n_i} \right) \ \mathrm{d}S$$ | [N] | Time dependent displacement force due to pressure and friction exerted by the flow of blood on the walls |


### `Vmax15.py`
| **Quantity**         | **Equation** | **Dimension** | **Description** |
|----------------------|--------------|--------------|--------------|
| **Flow Asymmetry** | $$\displaystyle \mathrm{Flow_{asymmetry}} = 100 \times {\lVert \vec{x}_ {v_{\rm max, 15}} - \vec{x}_{\rm plane}\rVert} / R _{\rm eq}$$ | non-dim | Level of flow eccentricity quantified by the Euclidian distance between the centroid of a plane and the centroid of top 15% of velocity of on that plane, normalised by the equivalant radius  |
| **Flow Dispersion** | $$\displaystyle \mathrm{Flow_{dispersion}} = 100 \times A_ {v_{\rm max, 15}} / A_ {\rm plane}$$ | non-dim | Level of flow dispersion quantified by the ratio of area of top 15% of velocity on a plane and the plane area  |

>Zhu, Y., Armour, C., Li, B. et al. A combined 4D flow MR imaging and fluid–structure interaction analysis of ascending thoracic aortic aneurysms. Biomech Model Mechanobiol 24, 829–844 (2025). [https://doi.org/10.1007/s10237-025-01939-6](https://doi.org/10.1007/s10237-025-01939-6)

