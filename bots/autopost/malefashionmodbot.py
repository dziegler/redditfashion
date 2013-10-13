from core.bot import submit_post

AUTHOR = ""
PASSWORD = ""
SUBREDDIT = "malefashion"


POST_CONTENTS = {
    "shopping_list": {
        "title": "Shopping List - {today}",
        "template": "templates/malefashion/shopping_list.md",
        "distinguish": True,
    },
    "whewt": {
        "title": "WHeWT - {today}",
        "template": "templates/malefashion/whewt.md",
        "distinguish": True,
    },
    "wiwt": {
        "title": "WIWT - {today} - {one_week_later}",
        "template": "templates/malefashion/wiwt.md",
        "distinguish": True,
        "sticky": True,
    },
    "general_discussion": {
        "title": "General Discussion - {today}",
        "template": "templates/malefashion/general_discussion.md",
        "distinguish": True,
        "sticky": True,
    }
}

if __name__ == "__main__":
    import sys
    key = sys.argv[1]
    submit_post(stdout=True, **POST_CONTENTS[key])
