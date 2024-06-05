#!/usr/bin/env python
import json
import os
import sc2reader
from sc2reader.factories.plugins.replay import toJSON, APMTracker

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Combines replay data in a directory to a single json file.")
    parser.add_argument(
        "--dir",
        metavar="directory",
        type=str,
        default=r"C:\Users\Des\Documents\StarCraft II\Accounts\329330652\1-S2-2-1270556\Replays\Multiplayer",
        help="Path to the directory containing replays to serialize.",
    )
    args = parser.parse_args()

    directory = args.dir

    # Verify that the provided path is a directory
    if not os.path.isdir(directory):
        print(f"Error: Directory not found. The provided path '{directory}' is not a directory.")
        return

    # Ideally a plugin can be enabled in the same factory?
    replayFactory = sc2reader.factories.SC2Factory()
    replayFactory.register_plugin("Replay", toJSON())

    apmFactory = sc2reader.factories.SC2Factory()
    apmFactory.register_plugin("Replay", APMTracker())

    replays_json = []

    # Iterate over all files in the directory
    for idx, filename in enumerate(os.listdir(directory)):
        filepath = os.path.join(directory, filename)

        # Ensure the file is a replay file 
        if os.path.isfile(filepath) and filepath.endswith('.SC2Replay'):
            
            # Load replay
            replay = sc2reader.load_replay(filepath, load_level=4)
            apm = apmFactory.load_replay(filepath)
            
            # Create a json object of replay data (toJSON plugin)
            replay_json_str = replayFactory.load_replay(filepath)

            # Get the avg_apm (APMTracker plugin)
            player_1_apm = apm.players[0].avg_apm
            player_2_apm = apm.players[1].avg_apm
            
            chat_messages = []
            if replay.messages:
                for message in replay.messages:
                    if isinstance(message, sc2reader.events.message.ChatEvent):
                        chat_messages.append({
                            "player": message.player.name,
                            "time": message.second,
                            "message": message.text
                        })
            
            # Convert the JSON string to a dictionary
            replay_json = json.loads(replay_json_str)
            
            # Add chat messages to the replay_json dictionary
            replay_json["chat_messages"] = chat_messages
            
            # Update avg_apm 
            replay_json["players"][0]["avg_apm"] = player_1_apm
            replay_json["players"][1]["avg_apm"] = player_2_apm

            # Add the replay
            replays_json.append(replay_json)

            print(f"Saved {idx} file: {filename}")

        with open(args.output, 'w') as outfile:
            json.dump(replays_json, outfile, indent=4)

    print(f"Saved {len(replays_json)} replay(s) to {os.path.abspath(args.output)}")

if __name__ == "__main__":
    main()
