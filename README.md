# Entropia Universe Loot Tracker

A simple, real-time loot tracking tool for Entropia Universe that reads directly from your `chat.log` file.

## Features

*   **Live Tracking:** Updates automatically as you play.
*   **Loot Breakdown:** Separates pure TT value (Shrapnel) from other items (potential markup).
*   **Efficiency Calculator:** Calculates your Return % based on ammo usage.
*   **Shot Estimator:** Estimates how many shots you've fired based on your weapon's ammo burn.

## How It Works

The tool monitors your `chat.log` file for specific system messages:
1.  **Loot:** `[System] [] You received ... Value: X.XX PED`
2.  **Ammo Input:** `[System] [] You received Universal Ammo ...`

## Important: How Efficiency is Calculated

**To track your costs and efficiency, you must convert Shrapnel to Universal Ammo in-game.**

The tool does not know how much ammo you bought from the Trade Terminal. Instead, it tracks the **Universal Ammo** you receive (usually from converting Shrapnel) as your "Ammo In" (Cost).

*   **Ammo In:** Increases when you see "You received Universal Ammo".
    *   *Note: These messages are explicitly excluded from the "Total Loot Value" to prevent double-counting.*
*   **Return %:** Calculated as `(Total Loot / Ammo In) * 100`.
*   **Est. Shots:** Calculated by dividing the total Universal Ammo units received by your weapon's **Ammo Burn**.

**Note:** If you are using tradeable ammo bought from the TT, the efficiency and shot counters will remain at 0 until you convert some shrapnel.

## Usage

1.  Ensure you have Python installed.
2.  Run the script:
    ```bash
    python loot_tracker.py
    ```
3.  The tool will attempt to automatically find your `chat.log` in the default location (`Documents\Entropia Universe\chat.log`). If not found, click **Select Log File** to locate it manually.
4.  **Ammo Burn:** Enter your weapon's ammo consumption (in units) in the input box to see estimated shots fired.
5.  **Reset:** Click the Reset button to clear the current session's stats.

## Requirements

*   Python 3.x
*   Tkinter (usually included with Python)
