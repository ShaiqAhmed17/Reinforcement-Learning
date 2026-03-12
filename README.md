# Reinforcement-Learning (4G3 Coursework I — 2026)

Coursework repository for **4G3 Reinforcement Learning** (2026). The main work lives in the `4G3/` folder and focuses on simulating **temporal-difference (TD) learning** with different stimulus representations, plus analysis/plotting utilities.

## Repository structure

- `4G3/RL.py`  
  Core simulation code:
  - Defines a reward time course (Gaussian-shaped) and a single stimulus “spike”.
  - Implements TD learning over multiple trials.
  - Runs multiple experiments:
    - **Tapped delay line** representation
    - **Boxcar** representation
    - **Partial reinforcement** (fixed probability and varying probability)
  - Stores intermediate results (value function `V`, TD term, and prediction error `delta`) for selected trials.

- `4G3/plots.py`  
  Plotting/analysis utilities (Matplotlib) for:
  - stimulus vs time, reward vs time
  - value function / temporal difference / delta over trials
  - averages over last trials under partial reinforcement
  - a simple “dopamine activity” transform of prediction error and comparisons across reinforcement probabilities

- `4G3/Reinforcement Learning.ipynb`  
  Notebook version of the work (interactive exploration / results).

- `4G3/py_to_pdf.py`  
  Utility script to convert one or more `.py` files into a syntax-highlighted PDF (uses `pygments` + `reportlab`).

- `4G3/*.pdf`, `4G3/*.png`  
  Coursework write-up / exported code / figures and supporting documents.

## Running (basic)

From the `4G3` directory:

```bash
python plots.py
