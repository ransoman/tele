import asyncio
import re
import aiohttp
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from payloads import SQLI_PAYLOADS, XSS_PAYLOADS
from utils import fetch_url, detect_cms
from result_saver import save_result

async def test_sqli(url, session):
    results = []
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    
    if not qs:
        return results

    for param in qs:
        original = qs[param][0]
        for payload in SQLI_PAYLOADS:
            qs[param] = original + payload
            new_query = urlencode(qs, doseq=True)
            new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
            text = await fetch_url(new_url, session)
            if any(err in text for err in ["SQL syntax", "mysql_fetch", "ORA-"]):
                results.append(f"SQLi on parameter `{param}` with payload: {payload}")
            qs[param] = original
    return results

async def test_xss(url, session):
    results = []
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    
    if not qs:
        return results

    for param in qs:
        original = qs[param][0]
        for payload in XSS_PAYLOADS:
            qs[param] = original + payload
            new_query = urlencode(qs, doseq=True)
            new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))
            text = await fetch_url(new_url, session)
            if payload in text:
                results.append(f"XSS on parameter `{param}` with payload: {payload}")
            qs[param] = original
    return results

async def run_full_scan(url):
    results = []
    async with aiohttp.ClientSession() as session:
        sqli_results = await test_sqli(url, session)
        if sqli_results:
            results.append("🚨 SQL Injection Detected:")
            results.extend(sqli_results)
        else:
            results.append("✅ No SQL Injection vulnerabilities detected.")
        
        xss_results = await test_xss(url, session)
        if xss_results:
            results.append("🚨 XSS Vulnerabilities Detected:")
            results.extend(xss_results)
        else:
            results.append("✅ No XSS vulnerabilities detected.")
        
        cms = await detect_cms(url, session)
        results.append(f"🕵️ CMS Detected: {cms}")
    
    final_result = "\n".join(results)
    await save_result(url, final_result)
    return final_result