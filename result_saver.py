import aiofiles
import datetime

async def save_result(url, content):
    filename = "scan_results.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] Scan for {url}\n{content}\n{'-'*40}\n"
    async with aiofiles.open(filename, mode="a") as f:
        await f.write(log_entry)