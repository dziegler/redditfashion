import argparse
import sys
import time
from datetime import date, timedelta, datetime

import praw

from reddit_bots.helpers import custom_strftime

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
        return custom_strftime(self.DATE_FORMAT, date.today() + timedelta(days=6))

    def get_context(self, **kwargs):
        kwargs.update({
            'today': self.today,
            'one_week_later': self.one_week_later,
        })
        return kwargs

    def add_sort_by_new(submission):
        url = submission.url + "?sort=new"
        text_to_append = "\n\n[**Click here to sort by new posts!**]({})\n".format(url)
        if submission.selftext.find(url) != -1:
            text = submission.selftext + text_to_append
            submission.edit(text)

    def _submit_post(self, submission_title, submission_content, max_retries=10):
        reddit = praw.Reddit(user_agent=self.user_agent)
        n_tries = 0

        while n_tries < max_retries:
            try:
                reddit.login(self.author, self.password)
                submission = reddit.submit(self.subreddit, submission_title, text=submission_content)
                break
            except praw.errors.RateLimitExceeded, e:
                print "Rate limit exceeded, trying again... {0}/{1}".format(n_tries, max_retries)
                n_tries += 1
                # reddit is probably overloaded, wait and try again
                time.sleep(5)
            except Exception, e:
                raise e

        if n_tries == max_retries:
            raise Exception("Max submission attempts exceeded.")

        return submission

    def post(self, title=None, content=None, template=None, flair=None,
             distinguish=False, sticky=False, add_sort_by_new=False, stdout=False):

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

        submission = self._submit_post(submission_title, submission_content)

        if distinguish:
            submission.distinguish()
        if sticky:
            submission.sticky()
        if flair:
            submission.set_flair(flair[0], flair[1])
        if add_sort_by_new:
            self.add_sort_by_new(submission)

        print "{}: Posted to {} - '{}'".format(datetime.now(), self.subreddit, title)
        return submission


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

    bot_kwargs = {
        'author': author,
        'password': password,
        'subreddit': subreddit,
    }

    if args.bot_test:
        bot_kwargs['subreddit'] = "bottesting"

    bot = AutoPostingBot(**bot_kwargs)
    bot.post(stdout=args.test_run, **post_contents[args.post_type])
