import re


async def format_content(content):
    button_matches = re.findall(r"\[(.+?)\s*=\s*(https?://\S+)\]", content)

    buttons = [{"text": text.strip(), "link": link.strip()} for text, link in button_matches]

    message_text = re.sub(r"\[.+?\s*=\s*https?://\S+\]", "", content).strip()

    return {
        "message_text": message_text,
        "buttons": buttons
    }
