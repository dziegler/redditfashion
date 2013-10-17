import os
from password import PASSWORD

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(ROOT_PATH, "templates")

AUTHOR = "malefashionmodbot"
SUBREDDIT = "malefashion"

POST_CONTENTS = {
    "shopping_list": {
        "title": "Shopping List - {today}",
        "template": os.path.join(TEMPLATE_DIR, "shopping_list.md"),
        "distinguish": True,
    },
    "whewt": {
        "title": "WHeWT - {today}",
        "template": os.path.join(TEMPLATE_DIR, "whewt.md"),
        "distinguish": True,
    },
    "wiwt": {
        "title": "WIWT - {today} - {one_week_later}",
        "template": os.path.join(TEMPLATE_DIR, "wiwt.md"),
        "add_sort_by_new": True,
        "distinguish": True,
        "sticky": True,
    },
    "general_discussion": {
        "title": "General Discussion - {today}",
        "template": os.path.join(TEMPLATE_DIR, "general_discussion.md"),
        "distinguish": True,
    }
}

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(ROOT_PATH, "..", ".."))

    from reddit_bots.autopost import console_run
    console_run(POST_CONTENTS, author=AUTHOR, password=PASSWORD, subreddit=SUBREDDIT)
