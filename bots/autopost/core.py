import argparse
import sys
from datetime import date, timedelta

import praw

from autopost.helpers import custom_strftime

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
        reddit.login(self.author, self.password)
        submission = reddit.submit(self.subreddit, submission_title, text=submission_content)

        if distinguish:
            submission.distinguish()
        if sticky:
            submission.sticky()
        # submission.set_flair(submission['flair'], submission['class'])
        return submission


def submit_post(post_content, author=None, password=None, subreddit=None, stdout=False):
    bot = AutoPostingBot(author=author, password=password, subreddit=subreddit)
    bot.post(stdout=stdout, **post_content)

def console_run(post_contents, author=None, password=None, subreddit=None):

    parser = argparse.ArgumentParser(description='Auto posting bot')
    parser.add_argument('post_type', metavar="post_type", help="Post type")
    parser.add_argument(
        '-t',
        '--test',
        help='Test run that prints to console, does not post',
        dest="test_run",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '-b',
        '--b',
        help='Post to the bottesting subreddit',
        dest="bot_test",
        default=False,
        action='store_true'
    )
    parser.add_argument(
        '-p',
        '--post_type',
        help='Prints what Post Types are available',
        dest="print_post_types",
        default=False,
        action='store_true'
    )
    args = parser.parse_args()

    if args.print_post_types:
        print "\nAvailable Post Types: \n"
        for key in post_contents.keys():
            print key
        sys.exit(0)

    post_kwargs = {
        'author': author,
        'password': password,
        'subreddit': subreddit,
    }
    if args.test_run:
        post_kwargs['stdout'] = True
    elif args.bot_test:
        post_kwargs['subreddit'] = "bottesting"

    submit_post(
        post_contents[args.post_type],
        **post_kwargs
    )
