# dialogflow-alphanumeric-transcriber
A webhook to perform alphanumeric transcription for Dialogflow.

Authors: Vivek D'Lima, Pak Ming Wan with packaging and documentation.

## Introduction

The Alphanumeric Transcriber helps with the accurate transcription of alphanumeric entities by allowing a user an alternative for transcription. Only works for English but can be adapted for other languages.

Supports Dialogflow ES and CX. This pattern can also be extended to perform additional NLU processing out of Dialogflow if required (from within the Cloud Function).

Currently:
Virtual Agent: Please provide the postcode for the address.
User: 1SW 2EJ

With alphanumeric transcriber:
Virtual Agent: Please provide the postcode for the address using a word that starts with the letter than you wish to transcribe, for example say apple for a.
User: 1 Sierra Whisky 2 Echo Juliet

The alphanumeric transcriber is deployed into a Cloud Function where it is called post-transcription to convert the Speech to Text transcription into the entity (i.e. 1 Sierra Whisky 2 Echo Juliet into 1SW2EJ).

## Deployment

Using the `gcloud` command line tool, issue the following command to deploy the Cloud Function. Say no to allowing unauthenticated calls.

`gcloud functions deploy alphanumeric-transcriber --source source/ --entry-point main --runtime python37 --trigger-http`

## Security

Grant the role Cloud Function Invoker to the service identity account that is associated with Dialogflow. If you haven't already created one, do so with this command:

`gcloud beta services identity create --service=dialogflow.googleapis.com --project=project-name`

This should return with an identity that you can then refer to in IAM to grant the Cloud Function Invoker role.

## Testing

On the command line you can test the Cloud Function with the command samples in `test/testScript.sh`.

Example payloads that you can use to adjust for your own testing can be found in `test/testPayloadES.json` and `test/testPayloadCX.json` for ES and CX respectively.

## Usage

Within Dialogflow, provide the following tags to activate different parts of the Cloud Function:
* `dialogflow-es`: activates Dialogflow ES specific code
* `phonetics_processor`: activates Dialogflow CX specific code
* `partial_response`: activates Dialogflow CX partial response mode

### Dialogflow CX Design Time Specific Instructions

Create a new webhook and set the URL of the Cloud Function. Do not set any other authentication information as the Cloud Function will authenticate Dialogflow CX using the service identity.

The webhook will reference the following two parameters:
* `phrase` a required parameter for the input phrase to the webhook (i.e. what Speech to Text transcribes), and
* `processed_phrase` an optional parameter for the output of the webhook to integrate back in the agent.

See the [alphanumeric transcriber pre-built agent](assets/sample-agent/sample_cx_agent_alphanumeric-transcriber-demo.blob) for a more complete design example on how to implement this.

Example webhook configuration in Dialogflow CX:

![assets/img/webhook_configuration.png]

Example webhook call with appropriate tag in Dialogflow CX:

![assets/img/webhook_tag.png]

### Dialogflow ES Specific Instructions

All ES specific code is within the code section with `dialogflow-es` as the tag.

After calling the webhook, you may need to redirect the next call to a speicfic intent. A code example for this is provided in the intent matcher `trigger_intent_example`.


