"""Chemisty Flash Cards.

This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import math
import random


# When editing your questions pay attention to your punctuation.
# Make sure you use question marks or periods.
# Make sure the first answer is the correct one.
# Set at least 4 answers, any extras will be shuffled in.
questions = [
    {
        "What is A C?": [
            "actinium"
        ]
    },
    {
        "What is A L?": [
            "aluminum"

        ]
    },
    {
        "What is A M?": [
            "americium"
        ]
    },
    {
        "What is S B?": [
            "antimony"
        ]
    },
    {
        "What is A R?": [
            "argon"
        ]
    },
    {
        "What is A S?": [
            "arsenic"
        ]
    },
    {
        "What is A T?": [
            "astatine"
        ]
    },
    {
        "What is B A?": [
            "barium"
        ]
    },
    {
        "What is B K?": [
            "berkelium"
        ]
    },
    {
        "What is B E?": [
            "beryllium"
        ]
    },
    {
        "What is B I?": [
            "bismuth"
        ]
    },
    {
        "What is B H?": [
            "bohrium"
        ]
    },
    {
        "What is B?": [
            "boron"
        ]
    },
    {
        "What is B R ?": [
            "bromine"
        ]
    },
    {
        "What is C D ?": [
            "cadmium"
        ]
    },
    {
        "What is C A ?": [
            "calcium"
        ]
    },
    {
        "What is C F ?": [
            "californium"
        ]
    },
    {
        "What is C ?": [
            "carbon"
        ]
    },
    {
        "What is C E ?": [
            "cerium"
        ]
    },
    {
        "What is C S ?": [
            "cesium"
        ]
    },
    {
        "What is C L ?": [
            "chlorine"
        ]
    },
    {
        "What is C R ?": [
            "chromium"
        ]
    },
    {
        "What is C O ?": [
            "cobalt"
        ]
    },
    {
        "What is C U ?": [
            "copper"
        ]
    },
    {
        "What is C M?": [
            "curium"
        ]
    },
]


def lambda_handler(event, context):
    """
    Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID
    to prevent someone else from configuring a skill that sends requests
    to this function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """Called when the session starts"""

    print("on_session_started requestId=" +
          session_started_request['requestId'] + ", sessionId=" +
          session['sessionId'])


def on_launch(launch_request, session):
    """
    Called when the user launches the skill without specifying what they
    want.
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """Called when the user specifies an intent for this skill"""

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # handle yes/no intent after the user has been prompted
    if 'attributes' in session.keys() and 'user_prompted_to_continue' in session['attributes'].keys():
        del session['attributes']['user_prompted_to_continue']
        if intent_name == 'AMAZON.NoIntent':
            return handle_finish_session_request(intent, session)
        elif intent_name == "AMAZON.YesIntent":
            return handle_repeat_request(intent, session)

    # Dispatch to your skill's intent handlers
    if intent_name == "AnswerIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AnswerOnlyIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return handle_answer_request(intent, session)
    elif intent_name == "AMAZON.StartOverIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.RepeatIntent":
        return handle_repeat_request(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_get_help_request(intent, session)
    elif intent_name == "AMAZON.StopIntent":
        return handle_finish_session_request(intent, session)
    elif intent_name == "AMAZON.CancelIntent":
        return handle_finish_session_request(intent, session)
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """
    Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# ------- Skill specific business logic -------

ANSWER_COUNT = 1
GAME_LENGTH = 5
CARD_TITLE = "Chemistry Flash Cards"  # Be sure to change this for your skill.

# --------------- Functions that control the skill's behavior -------------


def get_welcome_response():
    """
    If we wanted to initialize the session to have some attributes we could
    add those here
    """

    speech_output = ("Let's test your skills with FlashCards. I will ask you " +
                     str(GAME_LENGTH) + " questions, try to get as many right" +
                     "as you can. Just say the answer. Let's begin. ")
    should_end_session = False

    game_questions = populate_game_questions()

    current_questions_index = 0

    # Generate a random index for the correct answer, from 0 to 3
    correct_answer_index = math.floor(random.random() * (ANSWER_COUNT))
    round_answers = populate_round_answers(game_questions[current_questions_index], 0, correct_answer_index)

    spoken_question = questions[game_questions[current_questions_index]].keys()[0]
    reprompt_text = spoken_question

    # Update code to deal with multiple choice answers
    for i in range(0, ANSWER_COUNT):
        reprompt_text = reprompt_text + ""

    speech_output = speech_output + reprompt_text
    attributes = {"speech_output": reprompt_text,
                  "reprompt_text": reprompt_text,
                  "current_questions_index": current_questions_index,
                  "correct_answer_index": correct_answer_index + 1,
                  "questions": game_questions,
                  "score": 0,
                  "correct_answer_text": questions[game_questions[current_questions_index]].values()[0][0]
                  }

    return build_response(attributes, build_speechlet_response(
        CARD_TITLE, speech_output, reprompt_text, should_end_session))


def populate_game_questions():
    game_questions = []
    index_list = []
    index = len(questions)

    if GAME_LENGTH > index:
        raise ValueError("Invalid Game Length")

    for i in range(0, index):
        index_list.append(i)

    # Pick GAME_LENGTH random questions from the list to ask the user,
    # make sure there are no repeats
    for j in range(0, GAME_LENGTH):
        rand = int(math.floor(random.random() * index))
        index -= 1

        temp = index_list[index]
        index_list[index] = index_list[rand]
        index_list[rand] = temp
        game_questions.append(index_list[index])

    return game_questions


def populate_round_answers(game_question_indexes, correct_answer_index, correct_answer_target_location):
    """
    Get the answers for a given question, and place the correct answer
    at the spot marked by the correct_answer_target_location variable.
    Note that you can have as many answers as you want but
    only ANSWER_COUNT will be selected.
    """

    answers = []
    answers_copy = questions[game_question_indexes].values()[0]

    index = len(answers_copy)

    if index < ANSWER_COUNT:
        raise ValueError("Not enough answers for question.")

    # Shuffle the answers, excluding the first element.
    # If only 1 element no need to shuffle
    if index > 1:
        temp = answers_copy[1:]
        random.shuffle(temp)
        answers.append(answers_copy[0])
        answers.append(temp[0:ANSWER_COUNT-1])

        # Swap the correct answer into the target location
        answers[0], answers[correct_answer_target_location] = answers[correct_answer_target_location], answers[0]
    else:
        answers = answers_copy

    return answers


def handle_answer_request(intent, session):
    attributes = {}
    should_end_session = False
    answer_slot_valid = is_answer_slot_valid(intent)
    user_gave_up = intent['name']

    if 'attributes' in session.keys() and 'questions' not in session['attributes'].keys():
        # If the user responded with an answer but there is no game
        # in progress ask the user if they want to start a new game.
        # Set a flag to track that we've prompted the user.
        attributes['user_prompted_to_continue'] = True
        speech_output = "There is no game in progress. " \
                        "Do you want to start a new game?"
        reprompt_text = speech_output
        return build_response(attributes, build_speechlet_response(CARD_TITLE,
                              speech_output, reprompt_text, should_end_session))
    elif not answer_slot_valid and user_gave_up == "DontKnowIntent":
        # If the user provided answer isn't a number > 0 and < ANSWER_COUNT,
        # return an error message to the user. Remember to guide the user
        # into providing correct values.
        reprompt = session['attributes']['speech_output']
        speech_output = "Your answer must be a known element " + reprompt
        return build_response(session['attributes'], build_speechlet_response(CARD_TITLE, speech_output, reprompt_text, should_end_session))
    else:
        game_questions = session['attributes']['questions']
        correct_answer_index = session['attributes']['correct_answer_index']
        current_score = session['attributes']['score']
        current_questions_index = session['attributes']['current_questions_index']
        correct_answer_text = session['attributes']['correct_answer_text']

        speech_output_analysis = None
        if answer_slot_valid and intent['slots']['Answer']['value'].lower() == correct_answer_text:
            current_score += 1
            speech_output_analysis = "correct. "
        else:
            if user_gave_up != "DontKnowIntent":
                speech_output_analysis = "wrong. "
            speech_output_analysis = (speech_output_analysis +
                                      "The correct answer is " +
                                      correct_answer_text + ".")

        # if current_questions_index is 4, we've reached 5 questions
        # (zero-indexed) and can exit the game session
        if current_questions_index == GAME_LENGTH - 1:
            speech_output = "" if intent['name'] == "DontKnowIntent" else "That answer is "
            speech_output = (speech_output + speech_output_analysis + "Yog got "
                             + str(current_score) + " out of " + str(GAME_LENGTH)
                             + " questions correct. Thank you for learning Flash"
                             " Cards with Alexa!")
            reprompt_text = None
            should_end_session = True
            return build_response(session['attributes'],
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text, should_end_session))
        else:
            current_questions_index += 1
            spoken_question = questions[game_questions[current_questions_index]].keys()[0]
            # Generate a random index for the correct answer, from 0 to 3
            correct_answer_index = math.floor(random.random() * (ANSWER_COUNT))
            round_answers = populate_round_answers(game_questions[current_questions_index], current_questions_index, correct_answer_index)
            reprompt_text = spoken_question
            for i in range(0, ANSWER_COUNT):
                reprompt_text = reprompt_text + ""

            speech_output = "" if user_gave_up == "DontKnowIntent" else "That answer is "
            speech_output = (speech_output + speech_output_analysis +
                             "Your score is " +
                             str(current_score) + '. ' + reprompt_text)
            attributes = {"speech_output": reprompt_text,
                          "reprompt_text": reprompt_text,
                          "current_questions_index": current_questions_index,
                          "correct_answer_index": correct_answer_index + 1,
                          "questions": game_questions,
                          "score": current_score,
                          "correct_answer_text": questions[game_questions[current_questions_index]].values()[0][0]
                          }

            return build_response(attributes,
                                  build_speechlet_response(CARD_TITLE, speech_output, reprompt_text,
                                                           should_end_session))


def handle_repeat_request(intent, session):
    """
    Repeat the previous speech_output and reprompt_text from the
    session['attributes'] if available else start a new game session
    """
    if 'attributes' not in session or 'speech_output' not in session['attributes']:
        return get_welcome_response()
    else:
        attributes = session['attributes']
        speech_output = attributes['speech_output']
        reprompt_text = attributes['reprompt_text']
        should_end_session = False
        return build_response(attributes,
                              build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session))


def handle_get_help_request(intent, session):
    attributes = {}
    card_title = "Flash Cards"
    speech_output = ("You can begin a game by saying start a new game, or, "
                     "you can say exit... What can I help you with?")
    reprompt_text = "What can I help you with?"
    should_end_session = False
    return build_response(attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_finish_session_request(intent, session):
    """
    End the session with a message
    if the user wants to quit the game
    """
    attributes = session['attributes']
    reprompt_text = None
    speech_output = "Thanks for playing Flash Cards!"
    should_end_session = True
    return build_response(attributes,
                          build_speechlet_response_without_card(speech_output, reprompt_text, should_end_session))


def is_answer_slot_valid(intent):
    if 'Answer' in intent['slots'].keys() and 'value' in intent['slots']['Answer'].keys():
        return True
    else:
        return False


# --------------- Helpers that build all of the responses -----------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_speechlet_response_without_card(output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speechlet_response
    }
