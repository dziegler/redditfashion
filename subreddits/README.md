This bot will autopost recurring threads.

Setup
=============

1. In the same directory as `modbot.py` create a `password.py` file that contains:

        PASSWORD = "your password here"

2. Add the `cronjob` file to `cron.d` or copy and paste it into crontab using `crontab -e`. Make sure the paths in `cronjob` are correct for your server.

Adding a new recurring thread
=============

1. Add a new entry to `POST_CONTENTS` in `modbot.py`:

        POST_CONTENTS = {
            ...
            "new_thread": {
                "title": "This is a new thread - {today}",
                "template": os.path.join(TEMPLATE_DIR, "a_new_template.md"),
                "distinguish": True,
            },
        }


    Required:

    * `title` - Title of the post, recognizes variables {today} and {one_week_later}. Subclass the bot to add more.
    * `template` - Path to the file containing the body of the post.

    Optional:

    * `distinguish` - (Boolean: default False) - Distinguishes the post, requires mod status
    * `sticky` - (Boolean: defaule False) - Stickies the post, requires mod status
    * `flair` - (String tuple: default None) - First entry is the flair, second is the css class

2. Create a new template in the templates directory called `a_new_template.md` or whatever you named it in `modbot.py`and fill in the contents of your post.

3. Edit the `cronjob` file for when you'd like this thread to be posted. Remember to check the timezone of your server and take that into account.

4. Push your changes to the server.
