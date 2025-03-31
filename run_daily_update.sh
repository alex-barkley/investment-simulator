#!/bin/bash

cd ~/investment_simulator
source venv/bin/activate

echo "🔁 Running daily investment simulator update..."

# 1. Update index values
python update_index_history.py

# 2. Save daily client portfolio snapshot
python save_daily_portfolio_snapshot.py

# 3. Notify RMs of alerts
python notify_rms.py

echo "✅ All daily update tasks complete."
