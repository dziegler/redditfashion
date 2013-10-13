"""
This is a script to scrape reddit WAYWT and compile a Top of WAYWT.

Requires praw 2.1.9 or above.

Usage:

$python top.py                  #top of waywt for current month in MFA
$python top.py --month==9       #top of waywt for september in FA
$python top.py --month==9 -f    #top of waywt for september in FFA
$python top.py -s 50            #top of waywt for current month in MFA with score cutoff of 50

==========================================
By David Ziegler based off code by wummo
license: MIT License
"""
import calendar
import datetime
import re
import mimetypes
import logging

import praw

logging.basicConfig(level=logging.INFO)

def get_url_type(url):
    """
    Tries to guess wether an URL points to an image.
    """
    link_type, link_encoding = mimetypes.guess_type(url)

    if link_type is None:
        return "link"

    return "image" if link_type.startswith("image/") else "link"

def get_comment_score(comment, score_type="upvotes"):
    if score_type == "upvotes":
        return comment.ups
    elif score_type == "score":
        return comment.score


class MFAScraper(object):

    author = "MFAModerator"
    subreddit = "malefashionadvice"
    version = "0.2"

    # Some people, when confronted with a problem, think "I know, I'll use regular expressions." Now they have two problems.

    # Regex which (hopefully) matches the WAYWT titles
    waywt_title_pattern = re.compile('^WAYWT\s*-\s*(?P<month_name>[a-zA-Z]+)\.*\s*(?P<date>\d+).*')

    # Regex to extract URLs out of comment bodies
    html_link_pattern = re.compile('a href=\"([^\"]+)\"')

    # Don't use calendar.month_abbr because Sept doesn't match
    month_abbr = [
        '',
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sept',
        'Oct',
        'Nov',
        'Dec'
    ]

    def __init__(self):
        self.user_agent = 'TopOfWAYWT Collector v{0}'.format(self.version)

    def get_urls_from_comment(self, comment):
        """
        Returns a list of all URLs in a comment.
        """
        return re.findall(self.html_link_pattern, comment.body_html)

    def scrape_waywt(self, score_type="upvotes", score_threshold=75, month=None, year=None):

        # default to current month and year
        year = year or datetime.date.today().year
        month = month or datetime.date.today().month
        month_name = calendar.month_name[month]
        month_abbr = self.month_abbr[month]

        reddit = praw.Reddit(user_agent=self.user_agent)

        # Query to search threads with WAYWT and the current month name in their title
        query = "title:WAYWT AND author:{0} AND (title:{1} OR title:{2})".format(self.author, month_name, month_abbr)
        posts = reddit.search(query, subreddit=self.subreddit, sort="new")

        comments = []
        for submission in posts:

            # Ignore if not submitted this month/year
            submission_date = datetime.date.fromtimestamp(int(submission.created_utc))
            if submission_date.month != month or submission_date.year != year:
                continue

            # Ignore if title doesn't match regex
            match = re.match(self.waywt_title_pattern, submission.title)
            if not match:
                continue

            logging.info("Checking {0}, posted {1}".format(submission.title, submission_date))

            # Check each comment of the submission
            for comment in submission.comments:
                if isinstance(comment, praw.objects.MoreComments):
                    continue

                # That's what we're looking for
                if get_comment_score(comment, score_type=score_type) >= score_threshold:
                    comments.append(comment)

        logging.info("Found {} comments.".format(len(comments)))
        comments.sort(key=lambda comment: get_comment_score(comment, score_type=score_type), reverse=True)
        self.get_photos(comments, score_type)

    def get_photos(self, comments, score_type):
        """
        I don't really understand this formatting, so I'm not going to touch it. Should probably use
        some kind of template library though.
        """

        all_image_urls = []

        for rank, comment in enumerate(comments, 1):

            urls = self.get_urls_from_comment(comment)

            if not urls:
                logging.warning("No URLs found in comment {}.".format(comment.permalink))
                continue

            # Print informations about the post: rank, permalink, author and score
            print u"{}. [Post]({}) by *{}* (+{})  ".format(rank, comment.permalink, comment.author, get_comment_score(comment, score_type=score_type))

            buckets = {
                "link": [],
                "image": [],
            }

            for url in urls:
                buckets[get_url_type(url)].append(url)

            # Print 4 spaces (actually only 3 because Python prints the 4th) to
            # let MarkDown indent the current line on the list item level.
            print "   ",

            # Print all links by their category
            for key, values in buckets.items():
                if not values:
                    continue

                if key == "image":
                    all_image_urls.extend(values)

                name = key.capitalize()
                for index, url in enumerate(values, 1):
                    print "[{} {}]({})".format(name, index, url)

        print "\n==========="
        print "Image links"
        print "==========="
        for img in all_image_urls:
            print img


class FFAScraper(MFAScraper):

    author = "FFA_Moderator"
    subreddit = "femalefashionadvice"
    version = "0.2"


if __name__ == "__main__":

    from optparse import OptionParser
    parser = OptionParser()

    parser.add_option(
        '-f',
        '--ffa',
        help='Run the scraper for FFA, defaults to MFA',
        dest='female',
        default=False,
        action='store_true'
    )
    parser.add_option(
        "-m",
        "--month",
        choices=map(str, range(1, 13)),
        dest="month",
        help="The month to scrape, defaults to current",
        default=0
    )
    parser.add_option(
        "-y",
        "--year",
        dest="year",
        help="The year to scrape, defaults to current",
        type='int',
        default=0
    )
    parser.add_option(
        "-s",
        "--score_threshold",
        dest="score_threshold",
        help="Manually set the score cutoff for inclusion in Top of WAYWT, defaults to 75",
        type='int',
        default=75
    )
    parser.add_option(
        "-t",
        "--score_type",
        dest="score_type",
        choices=["upvotes", "score"],
        help="Scoring method to use",
        default="upvotes"
    )
    (options, args) = parser.parse_args()

    if options.female:
        scraper = FFAScraper()
    else:
        scraper = MFAScraper()

    scraper.scrape_waywt(
        score_type=options.score_type,
        score_threshold=options.score_threshold,
        month=int(options.month),
        year=int(options.year)
    )
