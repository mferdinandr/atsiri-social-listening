from __future__ import annotations

import subprocess


COMMANDS = [
    [
        "python3",
        "scripts/normalize/google_maps.py",
        "--raw-path",
        "data/raw/google_maps/batch_001/gmaps_output.json",
        "--reviews-output",
        "data/processed/batch_001/google_maps/gmaps_reviews.csv",
        "--reviewers-output",
        "data/processed/batch_001/google_maps/gmaps_reviewers.csv",
        "--batch-number",
        "batch_001",
    ],
    [
        "python3",
        "scripts/normalize/instagram_posts.py",
        "--raw-path",
        "data/raw/instagram_posts/all_posts/ig_posts_output.json",
        "--output-path",
        "data/processed/batch_001/instagram_posts/instagram_posts.csv",
        "--batch-number",
        "batch_001",
    ],
    [
        "python3",
        "scripts/normalize/instagram_comments.py",
        "--raw-path",
        "data/raw/instagram_comments/batch_001/ig_comments_output.json",
        "--posts-index-path",
        "data/raw/instagram_posts/all_posts/ig_post_index.json",
        "--output-path",
        "data/processed/batch_001/instagram_comments/instagram_comments.csv",
        "--batch-number",
        "batch_001",
    ],
]


def main() -> None:
    for command in COMMANDS:
        print("[normalize] running", " ".join(command))
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
