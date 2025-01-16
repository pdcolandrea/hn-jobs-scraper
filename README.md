# HN Hiring Crawler (wip)

A Python-based tool for crawling and parsing Hacker News "Who is Hiring?" monthly threads. This project helps developers and job seekers easily extract and analyze job postings from Hacker News' monthly hiring threads.

## Features

- Automated crawling of HN "Who is Hiring?" threads
- Structured data extraction from job postings
- Data parsing and cleaning
- Easy-to-use command line interface

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pdcolandrea/hn-jobs-scraper.git
cd hn-hiring
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your OpenAI API key:

Create a `.env` file in the root directory and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

This API key is required for the AI-powered parsing functionality of job postings. Will be improved later - couldn't find any safe, quick way to extract programmatically.

## Usage

Run the main script:

```bash
python main.py
```

## Project Structure

- `main.py` - Entry point of the application
- `parse.py` - Contains parsing logic for job posts
- `extract.py` - Handles data extraction from HN threads
- `schemas.py` - Data models and schemas
- `files.py` - Handles file operations

## Contributing

Feel free to open issues or submit pull requests if you have suggestions for improvements.

## License

MIT License - feel free to use this project as you wish.
