import web

# conifg
__urls = (
    '/', 'index'
    '/s', 'index'
)
__webapp = web.application(__urls, globals(), autoreload=True)


def run():
    __webapp.run()


class index:
    render = web.template.render('templates/')

    def GET(self):
        raise self.render.index()
