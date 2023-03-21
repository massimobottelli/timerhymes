# TimeRhymes
import json
import openai
import datetime
import time
import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
width = 800
height = 480

# Create screen surface
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)


# set the window title
pygame.display.set_caption("TimeRhymes")

# hide the mouse pointer
pygame.mouse.set_visible(False)


# Function to create ChatGPT response
def get_response(messages: list):
    global response

    # Load OpenAI API key
    with open("secrets.json") as f:
        secrets = json.load(f)
        api_key = secrets["api_key"]
    openai.api_key = api_key

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=1.0
    )
    return response.choices[0].message


def show_message(message):
    # Generate random color
    background_color = (
        random.randint(128, 255),
        random.randint(128, 255),
        random.randint(128, 255),
    )

    # Fill screen with random color
    screen.fill(background_color)

    # Set font and font size
    font = pygame.font.Font(None, 52)

    # Get complementary color for text
    text_color = (
        255 - background_color[0],
        255 - background_color[1],
        255 - background_color[2],
    )

    # Render and blit the first line
    line1 = font.render(message[0], True, text_color)
    text_x = (width - line1.get_width()) // 2
    text_y = (height - line1.get_height()) // 2 - 20
    screen.blit(line1, (text_x, text_y))

    # Render and blit the second line
    line2 = font.render(message[1], True, text_color)
    text_x = (width - line2.get_width()) // 2
    text_y = (height - line2.get_height()) // 2 + 20
    screen.blit(line2, (text_x, text_y))

    # Render and blit the time in the top right corner
    time_text = font.render(hour, True, text_color)
    screen.blit(time_text, (width - time_text.get_width() - 20, 20))

    # Update display
    pygame.display.flip()


while True:

    # Initialize chatGPT
    messages = []

    # Get current time
    now = datetime.datetime.now()
    hour = now.strftime("%H:%M")

    # compose prompt for chatGPT
    prompt = ("write a 2 lines poem in alternate rhyme on " + hour +
              "but you must use hour and minute in capital letters and not numbers")

    # receive chatGPT response
    messages.append({"role": "user", "content": prompt})
    response = get_response(messages=messages)
    poem = response["content"]

    print(prompt)
    print(poem)

    text = poem.lstrip("\n")
    text = text.split("\n")

    show_message(text)

    for i in range(int(60 - time.time() % 60)):

        # Detect key press ESC to exit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

        # Wait for one second
        time.sleep(1)
