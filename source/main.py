import time

NUMBER_MAP = {
    'one': '1',
    'two': '2',
    'to': '2',
    'three': '3',
    'four': '4',
    'for': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'neuf': '9',
    'zero': '0',
}


def processPhrase(phrase):
    if type(phrase).__name__ == 'float':
        phrase = int(phrase)
    phrase = str(phrase)
    query_list = phrase.split(' ')
    sequence = []
    print(query_list)
    for w in query_list:
        # Speech adds '.' to the utterance strings
        w = w.replace('.', '')
        print(w)
        if w.isnumeric():
            sequence.append(w)
        else:
            if NUMBER_MAP.get(w.lower()):
                sequence.append(NUMBER_MAP.get(w.lower()))
            else:
                sequence.append(w[0])
    sequence_str = ''.join(sequence)
    return sequence_str


def main(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        #flask.Flask.make_response>`.
        `make_response <http://flask.pocoo.org/docs/1.0/api/

    """
    request_json = request.get_json()
    print(request_json)

    if request_json.get('fulfillmentInfo', None):
        tag = request_json['fulfillmentInfo']['tag']
        print('Dialogflow CX webhook request with Tag: {}'.format(tag))
    elif request_json.get('queryResult', None):
        tag = 'dialogflow-es'
        print('Dialogflow ES webhook request')
    else:
        return ('Unrecognized request', 404)

    if tag == 'dialogflow-es':
        intent_name = request_json['queryResult']['intent']['displayName']

        # example to trigger intent followup in ES
        if intent_name == 'trigger_intent_example':
            # Set a response
            response = {}
            # response['fulfillmentText'] = ('This is fulfillment_text from the webhook')

            # Trigger the intent '3-zip-code-regex'
            response['followupEventInput'] = {
                'name': 'zip-code-regex'
            }

            return response

        elif intent_name in 'phonetic_recognizer':
            if request_json['queryResult']['parameters'].get('any'):
                parameter_any = request_json['queryResult']['parameters'].get(
                    'any')
                sequence_str = processPhrase(parameter_any)
                print(sequence_str)
            response = {}
            response['fulfillmentMessages'] = [
                {'text': {
                    'text': [f'Sequence received is: {sequence_str}']
                }
                }
            ]
            response['outputContexts'] = [
                {'name': request_json['session'] + ('/contexts/phonetic_recognizer'),
                 'lifespanCount': 5,
                 'parameters': {
                     'sequence': f'{sequence_str}'
                }
                }
            ]
            return response

        elif intent_name in 'Phonetic_recognizer_multi_format':
            if request_json['queryResult'].get('queryText'):
                query_text = request_json['queryResult'].get(
                    'queryText')
                sequence_str = processPhrase(query_text)
                print(sequence_str)
            response = {}
            response['fulfillmentMessages'] = [
                {'text': {
                    'text': [f'Sequence received is: {sequence_str}']
                }
                }
            ]
            response['outputContexts'] = [
                {'name': request_json['session'] + ('/contexts/phonetic_recognizer_multi_format'),
                 'lifespanCount': 5,
                 'parameters': {
                     'sequence': f'{sequence_str}'
                }
                }
            ]
            return response

        elif intent_name in ['phonetic_recognizer_1',
                             'phonetic_recognizer_2']:
            if request_json['queryResult']['parameters'].get('any'):
                parameter_any = request_json['queryResult']['parameters'].get(
                    'any')
                sequence_str = processPhrase(parameter_any)
                print(sequence_str)

            sequence = []
            if request_json['queryResult']['parameters'].get('one'):
                one = request_json['queryResult']['parameters'].get('one')
                one_str = processPhrase(one)
                sequence.append(one_str)
            if request_json['queryResult']['parameters'].get('two'):
                two = request_json['queryResult']['parameters'].get('two')
                two_str = processPhrase(two)
                sequence.append(two_str)
            if request_json['queryResult']['parameters'].get('three'):
                three = request_json['queryResult']['parameters'].get('three')
                three_str = processPhrase(three)
                sequence.append(three_str)
            if request_json['queryResult']['parameters'].get('four'):
                four = request_json['queryResult']['parameters'].get('four')
                four_str = processPhrase(four)
                sequence.append(four_str)
            if request_json['queryResult']['parameters'].get('five'):
                five = request_json['queryResult']['parameters'].get('five')
                five_str = processPhrase(five)
                sequence.append(five_str)
            if request_json['queryResult']['parameters'].get('six'):
                six = request_json['queryResult']['parameters'].get('six')
                six_str = processPhrase(six)
                sequence.append(six_str)
            if request_json['queryResult']['parameters'].get('seven'):
                seven = request_json['queryResult']['parameters'].get('seven')
                seven_str = processPhrase(seven)
                sequence.append(seven_str)
            if request_json['queryResult']['parameters'].get('eight'):
                eight = request_json['queryResult']['parameters'].get('eight')
                eight_str = processPhrase(eight)
                sequence.append(eight_str)
            sequence_str = ''.join(sequence)
            print(sequence_str)

            response = {}
            response['fulfillmentMessages'] = [
                {'text': {
                    'text': [f'Sequence received is: {sequence_str}']
                }
                }
            ]
            response['outputContexts'] = [
                {'name': request_json['session'] + ('/contexts/phonetic_recognizer'),
                 'lifespanCount': 5,
                 'parameters': {
                     'sequence': f'{sequence_str}'
                }
                }
            ]
            return response

    # code for Dialoglflow CX : standard response
    elif tag == 'phonetics_processor':
        parameter_info = request_json['pageInfo']['formInfo']['parameterInfo']
        for param in parameter_info:
            if param['displayName'] == 'phrase':
                parameter_any = param['value']
                sequence_str = processPhrase(parameter_any)
                print(sequence_str)
        response = {}
        response['page_info'] = {
            'form_info': {
                'parameter_info': [
                    {
                        'display_name': 'processed_phrase',
                        'value': sequence_str
                    }
                ]
            }
        }
        return response

    # code for Dialogflow CX : partial response
    elif tag == 'partial_response':
        time.sleep(10)
        response = {}
        response['fulfillment_response'] = {
            'messages': [
                {
                    'text': {
                        'text': ['Response from webhook']
                    }
                }
            ]
        }
        return response

    else:
        return ('Not matched', 404)
