import logging
import time
from itertools import count
from datetime import datetime
import requests
import difflib
import sys


CSGO_BLOG_URLS = {
    "home": "https://blog.counter-strike.net/",
    "updates": "https://blog.counter-strike.net/index.php/category/updates/",
}


def main(
    *,
    timeout: int,
    print_log: bool,
    print_log_level: int | str,
):
    print("Running CSGO Blog Changes Tracker... (Press Ctrl+C to stop)")
    now_capture = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    logging_format = "%(asctime)s [%(levelname)s]: %(message)s"

    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        filename=f"changes-{now_capture}.log",
    )

    if print_log:
        print_handler = logging.StreamHandler()
        print_handler.setLevel(print_log_level)
        print_handler.setFormatter(logging.Formatter(logging_format))

        logging.getLogger().addHandler(print_handler)

    session = requests.Session()
    responses = {label: None for label in CSGO_BLOG_URLS}
    check_counter = count(1)
    differ = difflib.Differ()

    while True:
        check_no = next(check_counter)
        logging.info(f"Check #{check_no} starting...")

        for label, url in CSGO_BLOG_URLS.items():
            res = session.get(url)

            if not res.ok:
                logging.error(
                    f"Got status code {res.status_code} while trying to access"
                    f" the {label!r} page on check #{check_no}."
                )
                continue

            if not responses[label]:
                responses[label] = res.content
                continue

            if (old_content := responses[label]) != (new_content := res.content):
                diff = differ.compare(
                    old_content.decode("utf-8").splitlines(),
                    new_content.decode("utf-8").splitlines(),
                )

                if changed_lines := tuple(
                    line
                    for line in diff
                    if "seconds" not in line.lower()
                    and (line.startswith("+") or line.startswith("-"))
                ):
                    logging.critical("!!! CHANGE DETECTED !!!")
                    logging.critical(
                        f"The following lines were changed on {label!r}:\n"
                        + ("\n".join(changed_lines))
                    )

            responses[label] = new_content

        logging.info(f"Check #{check_no} complete.")
        time.sleep(timeout)


if __name__ == "__main__":
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print(
            "CSGO Blog Changes Tracker by @alfawal\n"
            "Usage: python csgo_blog_changes_tracker.py [options]\n"
            "Options:\n"
            "  --timeout <seconds> - The amount of seconds to wait between"
            " checks. Defaults to 5.\n"
            "  --print-log - Whether to print the log to the console.\n"
            "  --print-log-level <level> - The level of the log to print to"
            " the console (e.g. INFO, ERROR, CRITICAL etc.)."
            " Defaults to INFO.\n"
        )
        raise SystemExit

    try:
        main(
            timeout=int(args[args.index("--timeout") + 1])
            if "--timeout" in args
            else 5,
            print_log="--print-log" in args,
            print_log_level=str(args[args.index("--print-log-level") + 1])
            if "--print-log-level" in args
            else logging.INFO,
        )
    except KeyboardInterrupt:
        print("Stopping CSGO Blog Changes Tracker...")
        raise SystemExit
