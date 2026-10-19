"""Read-only, allowlisted HTTPS source collector for SCOUT.

Fetches public UTF-8 text into a fresh local directory, recording metadata.
It does not discover hypotheses, verify truth, or contact people.
"""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from urllib.error import HTTPError, URLError

ALLOW_HOSTS = {"help.etsy.com", "www.etsy.com", "www.gutenberg.org"}
MAX_BYTES = 200_000

def allowed(url):
    parts = urlsplit(url)
    return (parts.scheme == "https" and parts.hostname in ALLOW_HOSTS
            and not parts.username and not parts.password and parts.port in (None, 443))

class RestrictedRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not allowed(newurl):
            raise ValueError("Redirect blocked: destination not on HTTPS allowlist")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def collect(url, output, opener=None):
    if not allowed(url):
        raise ValueError("URL must be HTTPS on the explicit public-source allowlist")
    folder = Path(output)
    if folder.exists():
        raise ValueError("Output directory already exists")
    folder.mkdir(parents=True)
    record = {"url": url, "retrieved_at": datetime.now(timezone.utc).isoformat(), "status": "error", "error": None}
    try:
        request = Request(url, headers={"User-Agent": "KI-01-SCOUT-Research/0.1 (read-only)"})
        with (opener or build_opener(RestrictedRedirect()).open)(request, timeout=12) as response:
            final = urlsplit(response.geturl())
            if not allowed(response.geturl()):
                raise ValueError("Redirect left HTTPS source allowlist")
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError("Source exceeds maximum snapshot size")
            content_type = response.headers.get_content_type()
            if content_type not in ("text/plain", "text/html"):
                raise ValueError("Unexpected content type: " + content_type)
            text = data.decode("utf-8")
            (folder / "source.txt").write_text(text, encoding="utf-8")
            record.update(status="ok", final_url=response.geturl(), content_type=content_type,
                          bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    except (HTTPError, URLError, OSError, ValueError, UnicodeError) as exc:
        record["error"] = str(exc)[:500]
    (folder / "provenance.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    return record

def main():
    p = argparse.ArgumentParser(description="Collect one allowlisted public HTTPS page as an auditable snapshot")
    p.add_argument("--url", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    try:
        result = collect(args.url, args.output)
        print(json.dumps(result))
        return 0 if result["status"] == "ok" else 2
    except ValueError as exc:
        print(str(exc))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
