#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import json

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        json_data = self.request.body
        data = json.loads(json_data)

        #print the readed json PRETTY
        print json.dumps(data, indent=2, sort_keys=True)
        #self.write("OK")


def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([(r"/sendData", MainHandler)])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
