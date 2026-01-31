#!/usr/bin/env python3
"""
SteamRip Scraper - Scrapes game data from SteamRip and generates JSON files
"""

import json
import os
import sqlite3
from datetime import datetime
from typing import List, Dict
import requests
from bs4 import BeautifulSoup


class SteamRipScraper:
    """Scraper for SteamRip game data"""
    
    def __init__(self, db_path: str = "steamrip.db"):
        self.db_path = db_path
        self.base_url = "https://steamrip.com"
        self.init_database()
        
    def init_database(self):
        """Initialize the SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create games table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                url TEXT UNIQUE,
                size TEXT,
                date_added TEXT,
                last_updated TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def scrape_games(self) -> List[Dict]:
        """
        Scrape game data from SteamRip
        For demonstration purposes, returns mock data
        In production, this would scrape the actual website
        """
        # Mock data for demonstration and testing
        # In production, this would use requests and BeautifulSoup to scrape
        mock_games = [
            {
                "title": "Cyberpunk 2077",
                "url": "https://steamrip.com/cyberpunk-2077",
                "size": "70 GB",
                "date_added": datetime.now().isoformat()
            },
            {
                "title": "Elden Ring",
                "url": "https://steamrip.com/elden-ring",
                "size": "50 GB",
                "date_added": datetime.now().isoformat()
            },
            {
                "title": "Red Dead Redemption 2",
                "url": "https://steamrip.com/rdr2",
                "size": "150 GB",
                "date_added": datetime.now().isoformat()
            }
        ]
        
        print(f"Scraped {len(mock_games)} games")
        return mock_games
        
    def update_database(self, games: List[Dict]) -> List[Dict]:
        """
        Update database with scraped games
        Returns list of new games added
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        new_games = []
        current_time = datetime.now().isoformat()
        
        for game in games:
            # Check if game already exists
            cursor.execute('SELECT id FROM games WHERE url = ?', (game['url'],))
            existing = cursor.fetchone()
            
            if existing:
                # Update existing game
                cursor.execute('''
                    UPDATE games 
                    SET title = ?, size = ?, last_updated = ?
                    WHERE url = ?
                ''', (game['title'], game['size'], current_time, game['url']))
            else:
                # Insert new game
                cursor.execute('''
                    INSERT INTO games (title, url, size, date_added, last_updated)
                    VALUES (?, ?, ?, ?, ?)
                ''', (game['title'], game['url'], game['size'], 
                      game['date_added'], current_time))
                new_games.append(game)
                
        conn.commit()
        conn.close()
        
        print(f"Added {len(new_games)} new games to database")
        return new_games
        
    def get_all_games(self) -> List[Dict]:
        """Get all games from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT title, url, size, date_added, last_updated FROM games')
        rows = cursor.fetchall()
        
        games = [
            {
                "title": row[0],
                "url": row[1],
                "size": row[2],
                "date_added": row[3],
                "last_updated": row[4]
            }
            for row in rows
        ]
        
        conn.close()
        return games
        
    def generate_json_files(self, all_games: List[Dict], new_games: List[Dict]):
        """Generate All.Games.json and New.Games.json files"""
        
        # Generate All.Games.json
        with open('All.Games.json', 'w', encoding='utf-8') as f:
            json.dump({
                "total_games": len(all_games),
                "generated_at": datetime.now().isoformat(),
                "games": all_games
            }, f, indent=2, ensure_ascii=False)
        print(f"Generated All.Games.json with {len(all_games)} games")
        
        # Generate New.Games.json
        with open('New.Games.json', 'w', encoding='utf-8') as f:
            json.dump({
                "new_games_count": len(new_games),
                "generated_at": datetime.now().isoformat(),
                "games": new_games
            }, f, indent=2, ensure_ascii=False)
        print(f"Generated New.Games.json with {len(new_games)} new games")
        
    def run(self):
        """Main execution method"""
        print("Starting SteamRip scraper...")
        
        # Scrape games
        scraped_games = self.scrape_games()
        
        # Update database and get new games
        new_games = self.update_database(scraped_games)
        
        # Get all games from database
        all_games = self.get_all_games()
        
        # Generate JSON files
        self.generate_json_files(all_games, new_games)
        
        print("SteamRip scraper completed successfully!")


if __name__ == "__main__":
    scraper = SteamRipScraper()
    scraper.run()
