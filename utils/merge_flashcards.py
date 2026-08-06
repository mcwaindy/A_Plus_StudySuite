#!/usr/bin/env python3
"""
Merge Core 1 and Core 2 flashcards and add exam field
"""
import json

# Load Core 1
with open('data/flashcards.json', 'r', encoding='utf-8') as f:
    core1_data = json.load(f)

# Load Core 2
with open('data/flashcards_core2.json', 'r', encoding='utf-8') as f:
    core2_data = json.load(f)

# Add exam field to Core 1 cards
for card in core1_data:
    card['exam'] = 'Core 1'

# Merge both lists
merged = core1_data + core2_data

# Save merged file
with open('data/flashcards.json', 'w', encoding='utf-8') as f:
    json.dump(merged, f, indent=2, ensure_ascii=False)

print(f"Merged flashcards!")
print(f"Core 1: {len(core1_data)} cards")
print(f"Core 2: {len(core2_data)} cards")
print(f"Total: {len(merged)} cards")
