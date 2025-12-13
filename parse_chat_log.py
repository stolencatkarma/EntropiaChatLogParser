import re
import sys
import json
import os

def parse_chat_log(file_path):
    """
    Parses an Entropia Universe chat log file.
    
    Args:
        file_path (str): Path to the chat.log file.
        
    Returns:
        list: A list of dictionaries containing parsed chat messages.
    """
    
    # Regex pattern to match the log format:
    # YYYY-MM-DD HH:MM:SS [Channel] [Sender] Message
    # Note: Sender can be empty []
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([^\]]+)\] \[([^\]]*)\] (.*)$')
    
    parsed_messages = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                match = pattern.match(line)
                if match:
                    timestamp, channel, sender, message = match.groups()
                    parsed_messages.append({
                        'timestamp': timestamp,
                        'channel': channel,
                        'sender': sender,
                        'message': message
                    })
                else:
                    # Handle cases where a line might not match (e.g. continuation of previous message?)
                    # For now, we'll just log it to stderr
                    # print(f"Skipping non-matching line: {line}", file=sys.stderr)
                    pass
                    
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return []
        
    return parsed_messages

def main():
    if len(sys.argv) < 2:
        print("Usage: python parse_chat_log.py <path_to_chat_log>")
        sys.exit(1)
        
    log_file_path = sys.argv[1]
    
    if not os.path.exists(log_file_path):
         print(f"Error: File not found at {log_file_path}")
         sys.exit(1)

    messages = parse_chat_log(log_file_path)
    
    # Output as JSON
    print(json.dumps(messages, indent=4))
    
    print(f"\nParsed {len(messages)} messages.")

if __name__ == "__main__":
    main()
