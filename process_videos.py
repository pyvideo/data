#!/usr/bin/env python3
import json
import os
import re
from pathlib import Path

def extract_speakers_from_text(text):
    """Extract speaker names from text like 'Name, Name & Name, Org'"""
    speakers = []
    # Remove common organization keywords
    text = text.replace(" - Meta", "").replace(" - Amazon", "").replace(", Meta", "").replace(", Amazon", "")
    text = text.replace(", Hugging Face", "").replace(", Amazon Web Services (AWS)", "").replace(", AWS", "")
    text = text.replace(", Intel", "").replace(", Google", "").replace(", OpenAI", "").replace(", Microsoft", "")
    text = text.replace(", Facebook", "").replace(", Lightning AI", "").replace(", NVIDIA", "")
    text = text.replace(", Meta Platforms, Inc.", "").replace("(AWS)", "").replace(" (AWS)", "")
    
    # Handle "Name & Name" and "Name, Name" patterns
    # Split by & first
    parts = re.split(r'\s*&\s*', text)
    for part in parts:
        # Then split each part by commas
        subparts = re.split(r',\s*', part.strip())
        for subpart in subparts:
            name = subpart.strip()
            # Skip common non-name words
            skip_words = ['Ltd.', 'Inc.', 'Inc', 'LLC', 'Labs', 'AI', 'USA', 'US', 'UK', 'and', 'the']
            if name and len(name) > 2 and not any(skip in name for skip in skip_words):
                if name not in speakers:
                    speakers.append(name)
    
    return speakers

def clean_file(filepath):
    """Process a single JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extract speakers from title
        title = data.get('title', '')
        if ' - ' in title:
            # Pattern: "Title - Speaker(s), Org"
            parts = title.rsplit(' - ', 1)
            if len(parts) == 2:
                title_part = parts[0].strip()
                speaker_part = parts[1].strip()
                speakers = extract_speakers_from_text(speaker_part)
                
                if speakers and data['speakers'] == ['TODO']:
                    data['speakers'] = speakers
                
                data['title'] = title_part
        
        # Clean description - remove leading "Title - Speakers, Org\n\n"
        description = data.get('description', '')
        if description and '\n\n' in description:
            parts = description.split('\n\n', 1)
            if len(parts) == 2:
                first_part = parts[0].strip()
                # Check if first part looks like "Title - Speakers, Org"
                if ' - ' in first_part and len(first_part) < 200:
                    data['description'] = parts[1].strip()
        
        # Write back
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write('\n')
        
        return True
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    branches = ['pytorchconf-2023', 'pytorchconf-2024']
    
    for branch in branches:
        branch_path = Path(branch) / 'videos'
        if not branch_path.exists():
            print(f"Skipping {branch_path} - not found")
            continue
        
        json_files = list(branch_path.glob('*.json'))
        print(f"\nProcessing {len(json_files)} files in {branch}...")
        
        for i, filepath in enumerate(json_files):
            if clean_file(str(filepath)):
                print(f"  [{i+1}/{len(json_files)}] Processed {filepath.name}")
            else:
                print(f"  [{i+1}/{len(json_files)}] FAILED {filepath.name}")

if __name__ == '__main__':
    main()

