import io

import aiohttp
from dotenv import load_dotenv
from gcloud.aio.storage import Storage
from google.cloud import texttospeech

load_dotenv()

names = [f"ja-JP-Neural2-{letter}" for letter in "BCD"]

# Instantiates a client
t2s_client = texttospeech.TextToSpeechClient()

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)


async def gcloud_text_to_speech(
    text: str, output: str, name: str = "ja-JP-Neural2-B"
) -> None:
    """Use Google Cloud Text-to-Speech to

    Args:
        text (str): _description_
        output (str): _description_
    """
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-JP") and the name
    # of the voice
    voice = texttospeech.VoiceSelectionParams(language_code="ja-JP", name=name)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = t2s_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    async with aiohttp.ClientSession() as session:
        client = Storage(session=session)  # type: ignore

        status = await client.upload(
            bucket="maiasahi-audio",
            object_name=output,
            file_data=io.BytesIO(response.audio_content),
            content_type="audio/mpeg",
        )

        print(f"Audio content uploaded to maiasahi-audio/{output}")

    # The response's audio_content is binary.
    # with open(output, "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)
    #     print(f'Audio content written to file "{output}.mp3"')
