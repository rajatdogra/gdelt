# GDELT Metal Supply Chain Analysis

Analysis of metal supply chain disruptions using GDELT news data, focusing on lead, nickel, zinc, copper, and aluminum.

## Overview

This project analyzes news articles from the GDELT database to identify mentions of metals and their associated supply chain issues (shortages, disruptions, bottlenecks, etc.). The analysis compares two approaches:

1. **Product Names Only**: Searching for direct metal names (e.g., "lead", "copper")
2. **Product + Ores**: Including related ore and mineral names (e.g., "galena" for lead, "chalcopyrite" for copper)

## Key Features

- **Proximity Analysis**: Identifies articles where metal names appear within 10 words of shortage-related keywords
- **Ore Inclusion**: Expands search to include mineral ores for more comprehensive coverage
- **Time Series Analysis**: Tracks mentions and shortage contexts over time
- **Comparative Metrics**: Shows improvement in detection when including ore names

## Data Structure

### Metals Analyzed
- **Lead**: galena, anglesite, cerussite, pyromorphite
- **Nickel**: pentlandite, pyrrhotite, garnierite, laterite
- **Zinc**: sphalerite, smithsonite, hemimorphite, franklinite
- **Copper**: chalcopyrite, bornite, azurite, malachite, chrysocolla, cuprite
- **Aluminum**: bauxite, gibbsite, boehmite, diaspore

### Shortage Keywords
scarcity, shortage, shortages, bottleneck, bottlenecks, disruption, disruptions, constraint, constraints, lack, deficit, crisis, problem, problems, delay, delays, stuck, blocked, halt, halted

## Files

- `product_analysis_full.ipynb`: Main analysis notebook with visualizations
- `scraped_data/`: Directory containing GDELT JSON data files

## Results Summary

The ore-inclusive approach significantly improves detection:
- **Lead**: 1,828 → 1,830 mentions (+2)
- **Aluminum**: 113 → 121 mentions (+8)
- **Copper**: 92 → 93 mentions (+1)

## Usage

1. Place GDELT JSON files in `scraped_data/` directory
2. Run `product_analysis_full.ipynb` to perform analysis
3. View comparative results and time series visualizations

## Requirements

- pandas
- matplotlib
- numpy
- json
- glob
- re