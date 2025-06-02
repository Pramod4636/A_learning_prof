def plant_growth(team_number=26, days=33):
    height = float(team_number)  # Start with team number as height

    history = []  # Store heights before decay to reverse 33rd day's growth

    for day in range(1, days + 1):
        prev_height = height

        # --- GROWTH ---
        if day % 14 == 0:
            height *= 4
        elif day % 7 == 0:
            height *= 3
        else:
            height *= 2

        # Save the growth-only height to reverse on day 33
        history.append(height)

        # --- DECAY ---
        if day % 10 == 0:
            height *= 0.5
        if day % 21 == 0:
            height *= 0.7
        if day % 28 == 0:
            height *= 0.8

        # --- CURSE on Day 33 ---
        if day == 33:
            # Reverse previous day's growth but not decay
            height /= (history[day - 2] / history[day - 3])

    return round(height, 2)


print(plant_growth(26))  # Output is your final plant height after 33 days
