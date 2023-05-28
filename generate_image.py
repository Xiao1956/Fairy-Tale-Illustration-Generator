import openai
import generate_fairy_tale_scene
import configparser
import os

# Get the sentence describing the fairytale scene
prompt = generate_fairy_tale_scene.main()

def generate_image(prompt):
    """
    Generate an image based on the given sentence using OpenAI's Image API.

    Args:
        prompt (str): The sentence for generating the image.

    Returns:
        str: The URL of the generated image.
    """
    response = openai.Image.create(
      prompt = prompt,
      n=1,
      # Adjust the resolution of the generated image
      size="1024x1024"
    )
    image_url = response['data'][0]['url']
    return image_url


def main():
    """
    Main function to generate an image based on the fairytale scene sentence.

    Returns:
        str: The URL of the generated image.
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(directory, "config.ini")
    config = configparser.ConfigParser()
    config.read(config_file_path)

    # Read user token from the config file"
    openai.organization = config.get("Twitter", "openai_organization")
    openai.api_key = config.get("Twitter", "openai_api_key")
    return generate_image(prompt)

if __name__ == "__main__":
    main()
