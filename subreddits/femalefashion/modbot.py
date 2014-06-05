import os
from password import PASSWORD

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(ROOT_PATH, "templates")

AUTHOR = "femalefashion"
SUBREDDIT = "femalefashion"

POST_CONTENTS = {
    "outfit_feedback": {
        "title": "Outfit Feedback Thread - {today}",
        "template": os.path.join(TEMPLATE_DIR, "outfit_feedback.md"),
        "distinguish": True,
    },
    "recent_purchases": {
        "title": "Recent Purchases and Keep/Return Thread - {today}",
        "template": os.path.join(TEMPLATE_DIR, "recent_purchases.md"),
        "distinguish": True,
    },
    "general_discussions": {
        "title": "General Discussions - {today}",
        "template": os.path.join(TEMPLATE_DIR, "general_discussions.md"),
        "distinguish": True,
    },
    "find_fashion": {
        "title": "Find Fashion Thread - {today}",
        "template": os.path.join(TEMPLATE_DIR, "find_fashion.md"),
        "distinguish": True,
    },
    "buy_sell_trade": {
        "title": "Buy/Sell/Trade Thread - {today}",
        "template": os.path.join(TEMPLATE_DIR, "buy_sell_trade.md"),
        "distinguish": True,
    },
    "random_thoughts": {
        "title": "Random Fashion Thoughts - {today}",
        "template": os.path.join(TEMPLATE_DIR, "random_thoughts.md"),
        "distinguish": True,
    }
}

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(ROOT_PATH, "..", ".."))

    from reddit_bots.autopost import console_run
    console_run(POST_CONTENTS, author=AUTHOR, password=PASSWORD, subreddit=SUBREDDIT)
