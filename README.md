# SteamRip-scraper-

A Python-based web scraper for SteamRip that collects game data and generates JSON files.

## Features

- Scrapes game information from SteamRip
- Stores data in a SQLite database
- Generates two JSON files:
  - `All.Games.json` - Contains all games in the database
  - `New.Games.json` - Contains only newly added games
- Automated via GitHub Actions

## Usage

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the scraper:
```bash
python steamrip_scrape_db.py
```

The script will:
- Scrape game data
- Update the database (`steamrip.db`)
- Generate `All.Games.json` and `New.Games.json`

### GitHub Actions

The scraper runs automatically:
- On pushes to the `add-python-github-action` branch
- On pull requests to the `main` branch

Generated files are available as workflow artifacts.

## Output Files

- **All.Games.json**: Contains all games with metadata (title, URL, size, dates)
- **New.Games.json**: Contains only games added in the current run
- **steamrip.db**: SQLite database with all game data
