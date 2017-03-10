#! /usr/bin/env python

import os.path
import sys

import apiai

import json

CLIENT_ACCESS_TOKEN = '03461f3a16334973acf1efb8949722c2'

ADDRESS_BOOK = {"Rein Appeldoorn": "rein@ruvu.nl",
                "Jesse Scholtes": "scholtes.jesse@gmail.com",
                "Rokus Ottervanger": "rokus@ruvu.nl"}

class Message():
    def __init__(self):
        self.addressee = None
        self.message = None

    def ready(self):
        return self.addressee and self.message

    def send(self):
        print "Sending message to:"
        print "\t" + self.addressee
        print "Message:"
        print "\t" + self.message

    def clear(self):
        self.__init__()


class ApiAIPepperClient(object):
    def __init__(self):
        self._ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
        self._session_id = None
        self._user_input = None

    def assemble_message(self):
        message = Message()

        while not message.ready():
            response = self._ask_for_user_input(user_input)
            message.extract_info(response)
            print self._get_speech(response)

        message.send()

    def _get_action(self, response):
        return response['result']['action']

    def _get_speech(self, response):
        result = response['result']
        fulfillment = result['fulfillment']
        speech = fulfillment['speech']
        return speech

    def _ask_for_user_input(self):
        request = self._ai.text_request()

        if self._session_id:
            request.session_id = self._session_id

        self._user_input = raw_input()
        request.query = self._user_input
        response_str = request.getresponse()
        response_json = json.loads(response_str.read())
        return response_json

    def run(self):
        print "Type 'Hey Pepper'... "
        self._user_input = raw_input()

        response = self._ask_for_user_input()
        action = self._get_action(response)

        if action == "send-email":
            self.assemble_message()

if __name__ == '__main__':
    client = ApiAIPepperClient()
    client.run()