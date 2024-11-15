# Quo_Vadis_COP_2024

## Overview

This repository contains the data and analysis codes used for evaluating Conference of Parties (COP) participant figures for the report *"Quo Vadis COP? 2024 Update"* by Benito Müller, Jen Allan, Matthias Roesti, and and Luis Gomez-Echeverri.

The goal of this analysis is to extract, clean, and analyze participant data from the COP and Subsidiary Body (SB) sessions, visualizing trends and key insights into country delegations and high-level representation.

---

## Pipeline Overview

The analysis pipeline consists of the following key steps:

1. **Collect Participant Data**: Gather the final list of participants from the COP and SB sessions, converting these lists into `.txt` format for processing.
   
2. **Extract Information via GPT-3.5 API**: Use the GPT-3.5 API to extract key information from the participant lists. The Python script `GPT_meets_UNFCCC.py` automates this extraction process.

3. **Clean, Aggregate, and Harmonize Data**: Process the extracted data, aggregate it, and assign high-level participant roles (such as head of government status). This step is managed through the R-Markdown script `COP_analysis_V2.rmd`.

4. **Analyze and Visualize**: Analyze the cleaned data and generate visualizations to represent key findings. This is also performed within the `COP_analysis_V2.rmd` script.

---

## Folder Structure

The repository is organized as follows:

```plaintext
├── GPT_meets_UNFCCC.py     # Python script for extracting data using GPT-3.5 API
├── COP_analysis_V2.rmd     # R-Markdown script for data cleaning, aggregation, analysis, and visualization
├── df_COP.RData            # Cleaned and processed data for COP sessions
├── df_SB.RData             # Cleaned and processed data for SB sessions
├── df_tot.RData            # Combined dataset (COP + SB)
├── data/                   # Contains raw and processed data files
├── plots/                  # Generated plots and figures from the R-Markdown script
└── README.md               # This README file
```


## How to Use

### Prerequisites

- **Python 3.9**: Suitable Python version required for running the `GPT_meets_UNFCCC.py` script.
- **R**: Required for running the R-Markdown script (`COP_analysis_V2.rmd`).
- **GPT-3.5 API Access**: You will need access credentials to OpenAI's GPT-3.5 API for extracting participant information.


## License
This project is licensed under the GNU General Public License - see LICENSE.md for more information.
