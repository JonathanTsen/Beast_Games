# Beast Games Contestant Video Analyzer

This tool extracts text from contestant videos using OpenAI's Whisper API, then analyzes the content using Google's Gemini API to extract structured information into an Excel file.

## Features

- Transcribes video content using OpenAI's Whisper API
- Analyzes transcription using Google's Gemini API
- Extracts structured data with Pydantic models
- Exports results to Excel format

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys (see `.env.example`)
4. Place contestant videos in the `data/input` directory

## Usage

Run the main script:

```
python src/main.py
```

Results will be saved in `data/output/contestant_data.xlsx`

## Data Structure

The program extracts the following information:
- Name
- Age
- Location
- Occupation
- Strategist type
- Favorite challenge in Beast Games Season 1
- Favorite contestant from Beast Games Season 1
- Uniqueness factors
- Plans for the $5,000,000 prize

## Requirements

- Python 3.8+
- OpenAI API key
- Google Gemini API key 