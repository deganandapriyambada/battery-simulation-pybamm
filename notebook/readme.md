# Data Set Consideration for Battery SDBMS SOC Prediction

## Q - Battery Capacity

SOC is measured using **Coulomb counting** approach where Battery Capacity (Q) is one of the key parameter. Below is the formula of SOC measurement using Coulomb counting

$$ SOC_{t} = SOC_{t_0} \pm \frac{1}{Q_{nominal}} \int_{t_0}^{t} I(\tau) \, d\tau $$


Q is one of the computation variable. Hence, Generated dataset from pybamm should specific for a target battery model capacity. Each variant of Q need to have dedicated dataset. 

    Q (Battery Capacity) is changing based on the battery aging**. capacity will  be gradually reduced from 100% to 90% .. 80% etc. 

Each scenario might need dedicated dataset.

## I - Current

Power-Current relationship

$$ P = V \cdot I \quad \Rightarrow \quad I = \frac{P}{V} $$

C-Rate Definition

$$ C\text{-rate} = \frac{I}{Q} \quad \Rightarrow \quad I = C\text{-rate} \cdot Q $$


Based on above equation, The higher charging rate (C-Rate) will resulting in higher Current(I) and finally increase the eletricity drained from battery. Simulating Charging rate (C-Rate) and Current (I) would be quite difficult as its depend on several variables such as Voltage (V), Power (P) and Capacity (C)

## Use Cases Scope

SoC Prediction will based Chen2020 battery Model for 5.0 Ah Battery.

## Paramter

    Battery Model is Lithium Ion SPM with Chen2020 Model Input parameter

Below is the updated / Overrided Parameter

| No | Parameter | Type |  Sources   |
|:--------:|:-------:|:------:|:------:|
| 1 | Battery Capacity (Q)  | Model Input | Set to 5 | 
| 2 | SoC  | Model Output | Computed using Coulomb Counting | 

## Variation

a total of 40 dataset are generated to cater battery aging scenario up to 40% loss or 60% battery capacity. 

    Dataset is generated per 1% capacity decrease from the initial value  

Major EV OEM suggest to replace the battery at 70~80% capacity.

| Variant | Capacity (%) | Q (Ah) |
|---------|---------------|--------|
| 1       | 100           | 5.00   |
| 2       | 99            | 4.95   |
| 3       | 98            | 4.90   |
| 4       | 97            | 4.85   |
| 5       | 96            | 4.80   |
| 6       | 95            | 4.75   |
| 7       | 94            | 4.70   |
| 8       | 93            | 4.65   |
| 9       | 92            | 4.60   |
| 10      | 91            | 4.55   |
| 11      | 90            | 4.50   |
| 12      | 89            | 4.45   |
| 13      | 88            | 4.40   |
| 14      | 87            | 4.35   |
| 15      | 86            | 4.30   |
| 16      | 85            | 4.25   |
| 17      | 84            | 4.20   |
| 18      | 83            | 4.15   |
| 19      | 82            | 4.10   |
| 20      | 81            | 4.05   |
| 21      | 80            | 4.00   |
| 22      | 79            | 3.95   |
| 23      | 78            | 3.90   |
| 24      | 77            | 3.85   |
| 25      | 76            | 3.80   |
| 26      | 75            | 3.75   |
| 27      | 74            | 3.70   |
| 28      | 73            | 3.65   |
| 29      | 72            | 3.60   |
| 30      | 71            | 3.55   |
| 31      | 70            | 3.50   |
| 32      | 69            | 3.45   |
| 33      | 68            | 3.40   |
| 34      | 67            | 3.35   |
| 35      | 66            | 3.30   |
| 36      | 65            | 3.25   |
| 37      | 64            | 3.20   |
| 38      | 63            | 3.15   |
| 39      | 62            | 3.10   |
| 40      | 61            | 3.05   |
