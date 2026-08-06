#!/usr/bin/env python3
"""Quick test to check review history loading."""
import json
from pathlib import Path

# Load review history
review_path = Path("data/review_history.json")
print(f"Review file exists: {review_path.exists()}")

if review_path.exists():
    with open(review_path, "r", encoding="utf-8") as f:
        reviews = json.load(f)
        print(f"\nTotal reviews: {len(reviews)}")

        review_objectives = set()
        for review in reviews:
            cards_reviewed = review.get("cards_reviewed", [])
            print(f"Cards reviewed in this session: {len(cards_reviewed)}")

            for card in cards_reviewed:
                obj = card.get("objective", "")
                term = card.get("term", "")
                print(f"  - Objective: '{obj}'")
                print(f"    Term: '{term}'")
                if obj:
                    review_objectives.add(obj)

        print(f"\nUnique objectives flagged for review:")
        for obj in sorted(review_objectives):
            print(f"  - '{obj}'")
