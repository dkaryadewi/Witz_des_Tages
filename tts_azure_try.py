import azure.cognitiveservices.speech as speechsdk

speech_key = ""
service_region = ""

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "de-DE-ConradNeural"

def text_to_speech(text, filename):
    # Speech synthesizer
    audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    # TTS conversion
    result = synthesizer.speak_text_async(text).get()

    # Result status
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized successfully.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.error_details:
            print(f"Error details: {cancellation_details.error_details}")


def list_available_voices():
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    voices_result = synthesizer.get_voices_async().get()

    for voice in voices_result.voices:
        print(f"Name: {voice.name}, Locale: {voice.locale}, Gender: {voice.gender}")
