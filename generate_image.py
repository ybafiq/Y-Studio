#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
generate_image.py
-----------------
Pure vanilla Python text-to-image generator.
Zero external dependencies — standard library only.

Uses the Pollinations.ai free public API (no signup, no API key).

Usage:
  python generate_image.py --prompt "a photorealistic oil palm seedling"
  python generate_image.py --prompt "..." --output "C:/images/plant.jpg" --width 1280 --height 720

Stdout on success (machine-readable):
  {"status": "success", "saved_path": "C:/images/plant.jpg"}

Stdout on failure:
  {"status": "error", "message": "..."}
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

API_BASE    = "https://image.pollinations.ai/prompt"
TIMEOUT_SEC = 120       # Pollinations can be slow on complex prompts
CHUNK_SIZE  = 8192      # Bytes per read chunk when streaming to disk
USER_AGENT  = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="generate_image",
        description="Vanilla Python text-to-image via Pollinations.ai — no ML deps required.",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text description of the image to generate. (Required)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output.jpg",
        help="Filename or full path for the saved image.\n(Default: output.jpg)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Image width in pixels. (Default: 1024)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Image height in pixels. (Default: 1024)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Fixed seed for reproducible results. (Default: random)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="flux",
        choices=["flux", "turbo"],
        help="Pollinations model to use.\n"
             "  flux  → FLUX.1 (higher quality, slower)\n"
             "  turbo → SDXL-Turbo (faster, lighter)\n"
             "(Default: flux)",
    )

    return parser


# ---------------------------------------------------------------------------
# URL builder
# ---------------------------------------------------------------------------

def build_url(prompt: str, width: int, height: int, seed: int | None, model: str) -> str:
    """
    Construct the full Pollinations.ai request URL.

    Structure:
      https://image.pollinations.ai/prompt/{encoded_prompt}?width=...&height=...
    """
    # Encode the prompt — replaces spaces with %20, escapes special chars
    encoded_prompt = urllib.parse.quote(prompt.strip(), safe="")

    # Query parameters
    params: dict = {
        "width":   width,
        "height":  height,
        "model":   model,
        "nologo":  "true",    # strips the Pollinations watermark logo
        "private": "true",    # prevents the image appearing on their public feed
        "enhance": "false",   # we supply our own prompt; skip their auto-enhancer
    }

    if seed is not None:
        params["seed"] = seed

    query_string = urllib.parse.urlencode(params)

    return f"{API_BASE}/{encoded_prompt}?{query_string}"


# ---------------------------------------------------------------------------
# Output path resolver
# ---------------------------------------------------------------------------

def resolve_output_path(raw_output: str) -> str:
    """
    Return the absolute path for the output file.
    Creates any missing parent directories automatically.
    """
    path = os.path.abspath(raw_output)
    parent = os.path.dirname(path)

    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)

    return path


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def validate_args(args: argparse.Namespace) -> None:
    """Raise SystemExit with a JSON error if any argument is invalid."""
    if not args.prompt.strip():
        _fatal("--prompt cannot be empty.")

    if args.width < 64 or args.width > 2048:
        _fatal("--width must be between 64 and 2048.")

    if args.height < 64 or args.height > 2048:
        _fatal("--height must be between 64 and 2048.")


# ---------------------------------------------------------------------------
# Network download
# ---------------------------------------------------------------------------

def download_image(url: str, output_path: str) -> None:
    """
    Stream the image binary from the API and write it to disk in chunks.

    Using chunked reads (instead of response.read() in one shot) keeps
    memory usage flat regardless of image size.

    Raises:
        urllib.error.URLError   — network/DNS failure
        urllib.error.HTTPError  — non-200 HTTP status from the API
        OSError                 — disk write failure
    """
    request = urllib.request.Request(
        url,
        headers={
            # Some CDNs block requests without a recognisable User-Agent
            "User-Agent": USER_AGENT,
            "Accept":     "image/jpeg,image/png,image/*,*/*",
        },
    )

    print(f"[generate_image] Requesting: {url}", file=sys.stderr)
    print(f"[generate_image] Saving to : {output_path}", file=sys.stderr)

    with urllib.request.urlopen(request, timeout=TIMEOUT_SEC) as response:
        # Validate content type — API should return an image
        content_type = response.headers.get("Content-Type", "")
        if "image" not in content_type.lower():
            raise ValueError(
                f"Unexpected Content-Type from API: '{content_type}'. "
                "The API may have returned an error page instead of an image. "
                f"Check the prompt or try again later."
            )

        http_status = response.status
        print(f"[generate_image] HTTP status: {http_status}", file=sys.stderr)

        # Stream binary to disk in chunks
        bytes_written = 0
        with open(output_path, "wb") as f:
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                f.write(chunk)
                bytes_written += len(chunk)

    if bytes_written == 0:
        # Remove the empty file to avoid leaving a corrupt artefact
        if os.path.exists(output_path):
            os.remove(output_path)
        raise ValueError("API returned a zero-byte response. The image was not generated.")

    kb = bytes_written / 1024
    print(f"[generate_image] Downloaded : {kb:.1f} KB", file=sys.stderr)


# ---------------------------------------------------------------------------
# Fatal error helper
# ---------------------------------------------------------------------------

def _fatal(message: str) -> None:
    """Print a JSON error payload to stdout and exit with code 1."""
    print(json.dumps({"status": "error", "message": message}, ensure_ascii=False))
    sys.exit(1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    # 1. Validate inputs
    validate_args(args)

    # 2. Resolve output path (creates directories if needed)
    try:
        output_path = resolve_output_path(args.output)
    except OSError as exc:
        _fatal(f"Cannot create output directory: {str(exc)}")

    # 3. Build request URL
    url = build_url(
        prompt=args.prompt,
        width=args.width,
        height=args.height,
        seed=args.seed,
        model=args.model,
    )

    # 4. Download image
    try:
        download_image(url, output_path)

    except urllib.error.HTTPError as exc:
        _fatal(
            f"API returned HTTP {exc.code} ({exc.reason}).\n"
            "Possible causes:\n"
            "  • The prompt was rejected by the content filter.\n"
            "  • The Pollinations.ai service is temporarily down.\n"
            "  • Rate limit exceeded — wait a moment and retry."
        )

    except urllib.error.URLError as exc:
        _fatal(
            f"Network error — could not reach the API.\n"
            f"Detail: {str(exc.reason)}\n\n"
            "Troubleshooting:\n"
            "  • Check your internet connection.\n"
            "  • Verify https://image.pollinations.ai is reachable in a browser.\n"
            "  • If behind a proxy, set the HTTPS_PROXY environment variable."
        )

    except TimeoutError:
        _fatal(
            f"Request timed out after {TIMEOUT_SEC} seconds.\n"
            "The Pollinations.ai API may be under heavy load. Try again shortly."
        )

    except ValueError as exc:
        _fatal(str(exc))

    except OSError as exc:
        _fatal(f"Failed to write image to disk: {str(exc)}")

    except Exception as exc:
        _fatal(f"Unexpected error: {type(exc).__name__}: {str(exc)}")

    # 5. Confirm file actually exists on disk before declaring success
    if not os.path.isfile(output_path):
        _fatal(f"Image file was not found after download: '{output_path}'")

    # 6. Emit machine-readable success JSON to stdout
    result = {
        "status":     "success",
        "saved_path": output_path,
        "width":      args.width,
        "height":     args.height,
        "model":      args.model,
        "prompt":     args.prompt,
    }

    print(json.dumps(result, ensure_ascii=False))


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()