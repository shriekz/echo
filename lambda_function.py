# This attempts to be (more or less) the simplest possible hello world Alexa skill...

from __future__ import print_function
import weather
import xl
import yokibu

# We'll start with a couple of globals...
CardTitlePrefix = "Greeting"

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Build a speechlet JSON representation of the title, output text, 
    reprompt text & end of session
    """
    output = "<speak>" + output + "</speak>"
    reprompt_text = "<speak>" + reprompt_text + "</speak>"
    print(output)
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Standard',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Hello"
    speech_output = "Congratulations on using our kid raising companion. "
    speech_output += "You can say the following. Greet the kids. Get time table schedule. Get messages from school."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry - I didn't understand. Please try again"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Genius wishes you a very nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def say_hello():
    #
    #Return a suitable greeting, along with weather.
    print("say hello message is triggered...")
    card_title = "Greeting Message"
    greeting_string = "Hello Abhinav and Vidhyuth. How are you doing?" + weather.getWeather()
    return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to greet the kids", True))

def say_yokibu(intent):

    # scrape the response from yokibu and return.
    card_title = "Message from Yokibu"
    print("Yokibu message is triggered...")
    yokibuMsg = yokibu.extractFromYokibu()
    print(yokibuMsg)
    return build_response({}, build_speechlet_response(card_title, yokibuMsg, "Ask genius to get messages from yokibu", True))


def say_timetable(intent):

    card_title = "Time table Message"

    print("say timetable message is triggered...")
    print(intent)
    status = intent['slots']['childname']['resolutions']['resolutionsPerAuthority'][0]['status']['code']
    if (status == "ER_SUCCESS_MATCH"):
        kid_name = intent['slots']['childname']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']
        time_table_string = xl.read_time_table(kid_name)
        print(time_table_string)
        should_end_session = True
    else:
        kid_name = intent['slots']['childname']['value']
        time_table_string = "sorry...heard kid name as " + kid_name + ", Please try again"
        should_end_session = False

    return build_response({}, build_speechlet_response(card_title, time_table_string, "Ask genius to get exam schedule for Abhi or Vidhyuth", should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print(intent_request)
    print("INTENT:" + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "GreetingIntent":
        return say_hello()
    elif intent_name == "TimetableIntent":
        return say_timetable(intent)
    elif intent_name == "YokibuIntent":
        return say_yokibu(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")
        #return say_hello()


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    
    
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
