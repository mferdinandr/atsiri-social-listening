from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.apify.com/v2"
TERMINAL_STATUSES = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run an Apify actor and save dataset items to JSON.")
    parser.add_argument("--actor-id", required=True, help="Actor ID, e.g. Xb8osYTtOjlsgI6k9")
    parser.add_argument("--input", required=True, help="Path to actor input JSON")
    parser.add_argument("--output", required=True, help="Path to output JSON dataset items")
    parser.add_argument("--meta-output", help="Optional path to save run metadata JSON")
    parser.add_argument("--poll-seconds", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--token", help="Optional Apify API token. Falls back to APIFY_API_TOKEN.")
    return parser.parse_args()


def load_env_file(path: str = ".env") -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def ensure_parent(path: str | Path) -> Path:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return file_path


def request_json(url: str, *, method: str = "GET", payload: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}\n{body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc}") from exc


def start_run(actor_id: str, token: str, actor_input: dict[str, Any]) -> dict[str, Any]:
    actor_path = quote(actor_id, safe="")
    query = urlencode({"token": token})
    url = f"{API_BASE}/acts/{actor_path}/runs?{query}"
    payload = request_json(url, method="POST", payload=actor_input)
    return payload["data"]


def get_run(run_id: str, token: str) -> dict[str, Any]:
    query = urlencode({"token": token})
    url = f"{API_BASE}/actor-runs/{run_id}?{query}"
    payload = request_json(url)
    return payload["data"]


def fetch_dataset_items(dataset_id: str, token: str) -> list[dict[str, Any]]:
    query = urlencode({"token": token, "format": "json", "clean": "true"})
    url = f"{API_BASE}/datasets/{dataset_id}/items?{query}"
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}\n{body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error for {url}: {exc}") from exc


def wait_for_run(run_id: str, token: str, timeout_seconds: int, poll_seconds: int) -> dict[str, Any]:
    started_at = time.monotonic()
    while True:
        run = get_run(run_id, token)
        status = run.get("status", "UNKNOWN")
        print(f"[apify] status={status} run_id={run_id}")
        if status in TERMINAL_STATUSES:
            return run
        if time.monotonic() - started_at > timeout_seconds:
            raise TimeoutError(f"Timed out waiting for run {run_id} after {timeout_seconds} seconds.")
        time.sleep(poll_seconds)


def main() -> None:
    args = parse_args()
    load_env_file()
    token = args.token or os.getenv("APIFY_API_TOKEN")
    if not token:
        raise SystemExit("APIFY_API_TOKEN is missing. Set it in .env or pass --token.")

    actor_input = json.loads(Path(args.input).read_text(encoding="utf-8"))
    run = start_run(args.actor_id, token, actor_input)
    final_run = wait_for_run(run["id"], token, args.timeout_seconds, args.poll_seconds)

    meta_output = args.meta_output or str(Path(args.output).with_name(Path(args.output).stem + "_run.json"))
    ensure_parent(meta_output).write_text(json.dumps(final_run, indent=2), encoding="utf-8")

    if final_run.get("status") != "SUCCEEDED":
        print(json.dumps(final_run, indent=2))
        raise SystemExit(f"Actor run ended with status: {final_run.get('status')}")

    dataset_id = final_run.get("defaultDatasetId")
    if not dataset_id:
        raise SystemExit("Actor run succeeded but defaultDatasetId is missing.")

    items = fetch_dataset_items(dataset_id, token)
    ensure_parent(args.output).write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"[apify] saved {len(items)} items to {args.output}")
    print(f"[apify] saved run metadata to {meta_output}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
