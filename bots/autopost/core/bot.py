from datetime import date, timedelta
from helpers import custom_strftime

import praw

class AutoPostingBot(object):

    DATE_FORMAT = "%b. %d{day_suffix}"
    version = "0.1"

    def __init__(self, author=None, password=None, subreddit=None):
        self.author = author
        self.password = password
        self.subreddit = subreddit
        self.user_agent = 'AutoPostingBot {} v{}'.format(self.author, self.version)

    @property
    def today(self):
        return custom_strftime(self.DATE_FORMAT, date.today())

    @property
    def one_week_later(self):
        return custom_strftime(self.DATE_FORMAT, date.today() - timedelta(days=6))

    def get_context(self, **kwargs):
        kwargs.update({
            'today': self.today,
            'one_week_later': self.one_week_later,
        })
        return kwargs

    def post(self, title=None, content=None, template=None, flair=None, distinguish=False, sticky=False, stdout=False):

        # Get the title
        submission_title = title.format(**self.get_context())

        # Get the body of the post
        if template:
            with open(template, 'r') as f_in:
                content = f_in.read()
        elif not content:
            raise Exception("Must specify content or template for this post")
        submission_content = content.format(**self.get_context())

        # Post it
        if stdout:
            print submission_title
            print "\n==============="
            print submission_content
            return

        reddit = praw.Reddit(user_agent=self.user_agent)
        reddit.login()
        submission = reddit.submit(self.subreddit, submission_title, text=submission_content)

        if distinguish:
            submission.distinguish()
        if sticky:
            submission.sticky()
        # submission.set_flair(submission['flair'], submission['class'])
        return submission

def submit_post(post_contents, author=None, password=None, subreddit=None, stdout=False):
    bot = AutoPostingBot(author=author, password=password, subreddit=subreddit)
    bot.post(stdout=stdout, **post_contents)
