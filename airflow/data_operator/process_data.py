import re
import csv

def process_data(input_raw, output_csv):
    current_matchday = 0
    matches = []

    with open(input_raw, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Iterate through each line in the file
    for line in lines:
        line = line.strip()
    
        # Skip lines with match date ("[Fri Aug/11]")
        if not line or line.startswith(("[","=", "#")):
            continue
        
        # Check for matchday header (e.g., "Round 1")
        if line.startswith("Matchday "):
            current_matchday = int(line.split("Matchday ")[1])
            continue
    
        # Handle both formats
        if line.startswith(tuple(f"{h:02d}.{m:02d}" for h in range(24) for m in [0, 15, 30, 45])):
            # Format 1: "20.00  Burnley FC 0-3 (0-2)  Manchester City FC"
            parts = line.split("  ", 1)  # Split on double space after time
            match_data = parts[1].strip()
        else:
            # Format 2: "Brighton & Hove Albion FC  4-1 (1-0)  Luton Town FC"
            match_data = line.strip()

        try:
            # Split match data into parts
            parts = re.split(r'\s{2,}', match_data)

            # read from parts
            home_team = parts[0]
            score_pre_process = parts[1]
            away_team = parts[2]
        
            # process score
            score = score_pre_process.split(' ')[0]
        
            # Add to results
            matches.append({
                "matchday": current_matchday,
                "home_team": home_team,
                "away_team": away_team,
                "score": score
            })
        except (ValueError, IndexError):
            print(f"Skipping malformed line: {line}")
            continue

    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["matchday", "home_team", "away_team", "score"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write data rows
        writer.writerows(matches)
    
        # print(f"Processed {len(matches)} matches and saved to {output_csv}")