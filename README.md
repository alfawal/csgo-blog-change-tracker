# CS:GO Blog Changes Tracker

![Heading for the Source](https://i.imgur.com/XapY1BW.png)

This simple Python script tracks changes on the [Counter-Strike: Global Offensive (CS:GO) blog](https://blog.counter-strike.net/) and alerts you when new change are occurred to it's HTML.

## Why?

This script is pretty useful for the gigachad players who want to know when the any tiny tweaks about the source 2.

## Prerequisites

- Python 3.10 or higher
- `requests` module (you can install it by running `pip3 install -r requirements.txt` in the script's directory or `pip3 install requests` to install it globally)

## Usage

To run the script, simply execute the `csgo_blog_changes_tracker.py` file with the following options:

`python3 csgo_blog_changes_tracker.py [options]`

Options:

- `--timeout <seconds>`: The amount of seconds to wait between checks. Defaults to 5.
- `--print-log`: Whether to print the log to the console.
- `--print-log-level <level>`: The level of the log to print to the console (e.g. INFO, ERROR, CRITICAL etc.). Defaults to INFO.

Example usage:

```sh
python3 csgo_blog_changes_tracker.py --timeout 10 --print-log --print-log-level ERROR
```

This will run the script with a timeout of 10 seconds between checks, print the log to the console, and only print log messages with an ERROR level or higher.

## Output

When a change is detected, the script will print a message to the console (if `--print-log` was given) and log file indicating which lines were changed on the CS:GO blog. The log file is saved in the same directory as the script with a filename in the format `changes-YYYY-MM-DD-HH-MM-SS.log`.

## Disclaimer

This script is not affiliated with Valve or any of its subsidiaries. This script is provided as-is and is not guaranteed to work. Use at your own risk.
