#!/bin/zsh

# Working directory
cd /Users/tetsu/cursor_for_stocks_info || exit 1

# Run the daily market analysis (time gate inside script ensures after 17:00)
python /Users/tetsu/cursor_for_stocks_info/tw_market_analysis.py



