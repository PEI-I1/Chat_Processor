#!/usr/bin/python3
"""Chat Processor Thread Manager

    Early days Documentation ^^

    Will mantain control over threads, used to responde to users
    questions.
    Responsible for a early triage of the message, deciding what
    problem category the message belongs.
    Will call other modules, responsible for providing the correct
    response for the users question.
"""

import logging
import threading
import random
import time


def choose_module():
    """Choose Module

        This selects the module which can best responde to the
        user question.
        TODO: usar o que o raul anda a fazer
    """
    return random.choice(range(2))


def call_module(info):
    """Call module

        Probably unnecessary, but simulates calling another
        module for now.
    """
    return info + " com SAL"


def get_response(msgData):
    """Gets best response for user question"""
    bestModule = choose_module()
    response = call_module(bestModule)
    return response


def thread_function(threadID, msgData):
    """Each thread runs this function when started"""
    logging.info("Chat %s: Starting", threadID)
    talking = True
    while(talking):
        msgData = get_question()
        response = get_response(msgData)

    logging.info("Chat %s: Finishing", threadID)




if __name__ == "__main__":
    logging.basicConfig()
    log = logging.getLogger("Logger")
    log.setLevel(logging.DEBUG)
    get_response("Problema de router...")
    time.sleep(1)
    get_response("O que há no cinema?")


    # log.debug("STARTING get_response")
    # newThread = threading.Thread(target=thread_function, args=(1,))
    # log.info("> before running thread")
    # newThread.start()
    # log.info("> thread running")
    # # newThread.join()
    # log.info("> all done")
