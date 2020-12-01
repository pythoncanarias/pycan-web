from urllib.parse import quote_plus
from django import template

register = template.Library()


def make_tweet(msg, url=''):
    msg = quote_plus(str(msg))
    buff = [
        'https://twitter.com/intent/tweet?',
        'text={}'.format(msg)
    ]
    if url:
        buff.append('&url={}'.format(url))
    return ''.join(buff)


@register.tag(name="tweet")
def tweet(parser, token):
    params = token.split_contents()
    tag_name = params.pop(0)
    assert tag_name == 'tweet'
    url = template.Variable(params.pop(0)) if params else ''
    assert len(params) == 0
    nodelist = parser.parse(('endtweet',))
    parser.delete_first_token()
    return TweetNode(nodelist, url)


class TweetNode(template.Node):

    def __init__(self, nodelist, url=''):
        self.nodelist = nodelist
        self.url = url

    def render(self, context):
        msg = self.nodelist.render(context)
        url = self.url.resolve(context)
        return '''<a href="{url}">{msg}</a>'''.format(
            url=make_tweet(msg, url),
            msg=msg,
            )
