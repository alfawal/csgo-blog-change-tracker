import logging
import time
from collections import defaultdict
from itertools import count
from datetime import datetime
import requests
import difflib

now_capture = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
logging_format = "%(asctime)s [%(levelname)s]: %(message)s"
logging_level = logging.INFO

logging.basicConfig(
    level=logging_level,
    format=logging_format,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=f"changes-{now_capture}.log",
)

print_handler = logging.StreamHandler()
print_handler.setLevel(logging_level)
print_handler.setFormatter(logging.Formatter(logging_format))

logging.getLogger().addHandler(print_handler)


CSGO_BLOG_URLS = {
    "home": "https://blog.counter-strike.net/",
    "updates": "https://blog.counter-strike.net/index.php/category/updates/",
}


def main(timeout: int):
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
    raise SystemExit(main(5))
