# SteamRip-scraper-

A web scraper for SteamRip.com that collects game information and stores it in a SQLite database.

## Features

- Scrapes game data from SteamRip.com
- Stores game information in SQLite database
- Tracks new games across runs
- Generates JSON output files (`All.Games.json` and `New.Games.json`)
- Automated CI/CD testing with GitHub Actions

## Requirements

- Python 3.11+
- Chrome browser (for Selenium WebDriver)
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Koriebonx98/SteamRip-scraper-.git
cd SteamRip-scraper-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the scraper:
```bash
python Scrape.steamrip.py
```

On first run, the script will:
- Install required dependencies from `requirements.txt`
- Create a SQLite database (`steamrip_games.db`)
- Generate `All.Games.json` with all discovered games
- Create a marker file (`first_run_success`) to indicate completion

On subsequent runs, the script will:
- Update the database with new games
- Update `All.Games.json` with all games
- Append new games to `New.Games.json`

## CI/CD Testing

This repository includes a GitHub Actions workflow (`.github/workflows/test-scraper.yml`) that:
- Tests the script in a clean Ubuntu environment
- Verifies first-run dependency installation
- Validates database creation and population
- Checks JSON output file generation
- Tests subsequent run behavior
- Uploads artifacts for inspection

The workflow runs on:
- Pushes to `main` or `copilot/test-scrape-steamrip-script` branches
- Pull requests to `main`
- Manual workflow dispatch

## Output Files

- `All.Games.json` - Contains all games discovered (sorted alphabetically)
- `New.Games.json` - Contains only new games discovered since first run
- `steamrip_games.db` - SQLite database with game history and run metadata
- `first_run_success` - Marker file indicating first-run setup completion
