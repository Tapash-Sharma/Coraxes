import discord
from discord.ext import commands
from datetime import datetime
import aiohttp  # To handle HTTP requests for file downloads
import os  # To handle file system operations
import uuid  # To generate random file suffixes
import json  # To parse JSON responses
import subprocess

# Enable the message content intent
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Ensure download directory exists
download_dir = "downloads"
os.makedirs(download_dir, exist_ok=True)


def ensure_docker_running(container_name, port_mapping):
    try:
        # Check if the Docker container is running
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
        )
        running_containers = result.stdout.strip().split("\n")
        
        if container_name in running_containers:
            print(f"The container '{container_name}' is already running.")
        else:
            # Run the Docker container if not running
            print(f"Starting the container '{container_name}'...")
            subprocess.run(
                ["docker", "run", "-d", "-p", port_mapping, container_name],
                check=True,
            )
            print(f"Container '{container_name}' started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while managing Docker container: {e}")


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    ensure_docker_running("coraxes", "5000:5000")


@bot.event
async def on_message(message):
    # Check if the message is from a bot in the target channel
    channel_id = 1333338696950480926  # Replace with your target channel ID
    if message.channel.id == channel_id and message.author.bot:
        for attachment in message.attachments:
            try:
                # Generate a random suffix for the file name
                random_suffix = uuid.uuid4().hex[:8]
                filename, file_extension = os.path.splitext(attachment.filename)
                random_filename = f"{filename}_{random_suffix}{file_extension}"
                file_path = os.path.join(download_dir, random_filename)

                # Download the file
                async with aiohttp.ClientSession() as session:
                    async with session.get(attachment.url) as response:
                        if response.status == 200:
                            with open(file_path, 'wb') as f:
                                f.write(await response.read())
                            print(f"Downloaded: {random_filename}")

                            # Upload the file using Python HTTP request
                            upload_url = "http://127.0.0.1:5000/upload"
                            async with session.post(upload_url, data={"file": open(file_path, "rb")}) as upload_response:
                                if upload_response.status == 200:
                                    response_text = await upload_response.text()
                                    # print(f"Upload successful: {response_text}")

                                    # Parse the JSON response
                                    response_data = json.loads(response_text)
                                    final_result = response_data.get("final_result", "Unknown")
                                    predictions = response_data.get("predictions", [])

                                    if final_result == "Malicious":
                                        spam_models = [model.split(":")[0] for model in predictions if "['S']" in model]
                                        message_content = (
                                            "The email seems to be malicious. Handle with care.\n"
                                            "These prediction models identified it as malicious:\n" + "\n".join(spam_models)
                                        )
                                        await message.channel.send(message_content)
                                    elif final_result == "Healthy":
                                        await message.channel.send(
                                            "The email seems to be healthy, but be careful."
                                        )
                                else:
                                    print(f"Upload failed with status {upload_response.status}: {await upload_response.text()}")

                        else:
                            print(f"Failed to download: {attachment.filename}")
            except Exception as e:
                print(f"Error downloading {attachment.filename}: {e}")

    await bot.process_commands(message)

bot.run('your_discord_token')
