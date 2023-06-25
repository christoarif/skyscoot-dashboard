This repository is for airline staff to monitor in-flight sales data for different destinations and flights. This is important for inventory management, minimise waste and maximise revenue.

To reproduce:

1. To install required packages, Conda is used. Run `conda env create -f environment.yml` to create environment and `conda activate skyscoot_dashboard` to activate it.
2. Run `python3 gen_data.py` to generate data that will be used for the dashboard.
3. Run `python3 dashboard.py` to start the dashboard in http://127.0.0.1:8050/.
