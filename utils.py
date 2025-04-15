import aiohttp

async def fetch_url(url, session):
    headers = {"User-Agent": "X-VULN-SCANNER-BOT"}
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            return await response.text()
    except Exception as e:
        return str(e)

async def detect_cms(url, session):
    text = await fetch_url(url, session)
    if "wp-content" in text or "WordPress" in text:
        return "WordPress"
    elif "Joomla" in text:
        return "Joomla"
    elif "Drupal" in text:
        return "Drupal"
    else:
        return "Unknown"