import os
from password import PASSWORD

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(ROOT_PATH, "templates")

AUTHOR = "FFA_Moderator"
SUBREDDIT = "femalefashionadvice"

POST_CONTENTS = {
    "recent_purchases": {
        "title": "Recent Purchases - {today}",
        "template": os.path.join(TEMPLATE_DIR, "recent_purchases.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "simple_questions": {
        "title": "Simple Questions - {today}",
        "template": os.path.join(TEMPLATE_DIR, "simple_questions.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "hair_makeup": {
        "title": "Hair, Makeup, Skincare, Fitness, and Fragrance Thread - {today}",
        "template": os.path.join(TEMPLATE_DIR, "hair_makeup.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "general_discussion": {
        "title": "General Discussion - {today}",
        "template": os.path.join(TEMPLATE_DIR, "general_discussion.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "waywt": {
        "title": "WAYWT - {today}",
        "template": os.path.join(TEMPLATE_DIR, "waywt.md"),
        "distinguish": True,
        "add_sort_by_new": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "random_fashion": {
        "title": "Random Fashion Thoughts - {today}",
        "template": os.path.join(TEMPLATE_DIR, "random_fashion.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "outfit_feedback": {
        "title": "Outfit Advice & Feedback - {today}",
        "template": os.path.join(TEMPLATE_DIR, "outfit_feedback.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "need_want_love": {
        "title": "Should I or Shouldn't I Buy... - {today}",
        "template": os.path.join(TEMPLATE_DIR, "need_want_love.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
    "find_fashion_friday": {
        "title": "Find Fashion Friday - {today}",
        "template": os.path.join(TEMPLATE_DIR, "find_fashion_friday.md"),
        "distinguish": True,
        "flair": ("[Weekly]", "scheduled")
    },
}

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.join(ROOT_PATH, "..", ".."))

    from reddit_bots.autopost import console_run
    console_run(POST_CONTENTS, author=AUTHOR, password=PASSWORD, subreddit=SUBREDDIT)
