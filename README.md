# Walmart Canada Store Data

This repository includes a script to query Walmart store locations in Canada using the OpenStreetMap Overpass API. The script fetches store names, addresses, coordinates, and a placeholder image URL. Results are saved to a CSV file and displayed as a pandas DataFrame.

## Requirements

- Python 3
- packages listed in `requirements.txt`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script:

```bash
python walmart_canada.py
```

This will attempt to query the Overpass API for Canadian Walmart stores and write `walmart_canada_stores.csv`.

If you cannot access the Overpass API from your environment, you can test the script with the included `sample_walmart_canada.csv`.
