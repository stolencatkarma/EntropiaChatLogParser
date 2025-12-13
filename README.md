# Entropia Universe Loot Tracker

A real-time loot and skill tracking tool for Entropia Universe that reads directly from your `chat.log` file.

## Features

*   **Live Tracking:** Updates automatically as you play.
*   **Loot Breakdown:** 
    *   Tracks **Total Loot Value**.
    *   Separates **Shrapnel** from **Items**.
    *   Calculates **Average Shrapnel** amount per drop.
*   **Skill Tracker:** Automatically tracks and sums up all Skill and Attribute gains in a dedicated tab.
*   **Hourly Rates:** Displays your "Loot/Hr" based on the current session duration.
*   **Mini Mode:** A compact, always-on-top overlay (128x32px) that displays your total loot value. Perfect for keeping track while playing in windowed mode.
    *   **Draggable:** Click and drag to position it anywhere.
    *   **Toggle:** Double-click to return to the full interface.

## How It Works

The tool monitors your `chat.log` file for specific system messages:

### Loot Logic
1.  **Loot:** `[System] [] You received ... Value: X.XX PED` -> Adds to Total and Breakdown.
2.  **Shrapnel Conversion:** When you convert Shrapnel to Universal Ammo, the game logs a "You received Universal Ammo" message. 
    *   The tool detects this and **subtracts** the original Shrapnel value from your Total Loot and Shrapnel count.
    *   *Calculation:* `Deduction = Universal Ammo Value / 1.01` (Since conversion gives 101% value).
    *   *Reasoning:* Converting Shrapnel consumes a looted asset, so it is removed from your "Realized Loot" total to keep the session value accurate to what you currently hold.

### Skill Logic
*   Tracks `You have gained X experience in your Y skill` and `You have gained X Attribute`.
*   Aggregates gains for the session (e.g., if you gain Rifle 5 times, it shows the total sum).

## Usage

1.  Ensure you have Python installed.
2.  Run the script:
    ```bash
    python loot_tracker.py
    ```
3.  The tool will attempt to automatically find your `chat.log` in the default location (`Documents\Entropia Universe\chat.log`). If not found, click **Select Log File** to locate it manually.
4.  **Mini Mode:** Click the "Mini Mode" button to switch to the overlay. Double-click the overlay to switch back.
5.  **Reset:** Click the Reset button to clear the current session's stats.

## Requirements

*   Python 3.x
*   Tkinter (usually included with Python)
