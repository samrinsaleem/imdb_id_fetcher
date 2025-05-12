# IMDb ID Finder for Movies & TV Shows

A Streamlit app to quickly fetch IMDb IDs for a list of movie/TV show titles from a CSV or Excel file. It uses fuzzy search and manual review options to help match even the trickiest of titles.

## How It Works

1. Upload your file with a `Title` column (and optionally `Year`).
2. The app searches IMDb for each title and retrieves top matches.
3. You can either auto-pick the top result or manually review matches.
4. The updated file with IMDb IDs is ready to download!

## Features

- Works with `.csv` or `.xlsx`
- Optional year filtering for better accuracy
- Manual review toggle for precise matching
- Automatically adds a new `IMDb ID` column
- Exports as Excel file for easy integration

## Requirements
- Python 3.7+
- Internet connection (to reach IMDb)

## License
This project is licensed under the CC BY-NC 4.0 License.
You can use and modify it for non-commercial purposes, but not for profit. Attribution is required.


### Built with caffeine and curiosity.
