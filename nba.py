import pygame
import random
import game_data  # Import shared money variable

NBA_TEAMS = {
    "Atlanta Hawks": 75, "Boston Celtics": 90, "Brooklyn Nets": 80, "Charlotte Hornets": 70, "Chicago Bulls": 78,
    "Cleveland Cavaliers": 82, "Dallas Mavericks": 85, "Denver Nuggets": 92, "Detroit Pistons": 65, "Golden State Warriors": 88,
    "Houston Rockets": 72, "Indiana Pacers": 78, "LA Clippers": 86, "Los Angeles Lakers": 89, "Memphis Grizzlies": 83,
    "Miami Heat": 87, "Milwaukee Bucks": 91, "Minnesota Timberwolves": 80, "New Orleans Pelicans": 79, "New York Knicks": 81,
    "Oklahoma City Thunder": 77, "Orlando Magic": 74, "Philadelphia 76ers": 88, "Phoenix Suns": 90, "Portland Trail Blazers": 76,
    "Sacramento Kings": 79, "San Antonio Spurs": 70, "Toronto Raptors": 77, "Utah Jazz": 75, "Washington Wizards": 68
}

def generate_matchups():
    teams = random.sample(list(NBA_TEAMS.keys()), 8)
    return [(teams[i], teams[i+1]) for i in range(0, 8, 2)]

def calculate_payout(bet_amount, team_odds, opponent_odds):
    rating_diff = abs(team_odds - opponent_odds)

    if team_odds >= opponent_odds:  # Favorite team
        payout_multiplier = 1.3 + (0.15 / (1 + rating_diff / 4))  # Ensures at least ~30% return
    else:  # Underdog
        if rating_diff <= 2:
            payout_multiplier = 1.5  # Small difference: 50% return
        elif rating_diff <= 4:
            payout_multiplier = 1.8  # Medium difference
        elif rating_diff <= 7:
            payout_multiplier = 2.6  # Bigger underdog
        else:
            payout_multiplier = 3.4 + (rating_diff - 7) * 0.35  # Extreme underdogs

    payout = int(bet_amount * round(payout_multiplier, 2))
    return max(payout, int(bet_amount * 1.25))
def nba_game(SCREEN):
    pygame.display.flip()

    screen_width, screen_height = SCREEN.get_size()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 200, 0)
    BLUE = (30, 144, 255)
    BOX_COLOR = (0, 0, 0, 180)

    font = pygame.font.Font(None, 36)
    result_font = pygame.font.Font(None, 40)
    score_font = pygame.font.Font(None, 60)

    court_bg = pygame.image.load("court.png")
    court_bg = pygame.transform.scale(court_bg, (screen_width, screen_height))

    matchups = generate_matchups()
    bet_amount = 5
    selected_game = 0
    selected_team = 0
    result_text = ""
    game_running = False
    showing_results = False
    exit_button = pygame.Rect(20, screen_height - 50, 100, 30)

    # Add variables to track the last played teams
    last_played_team1 = ""
    last_played_team2 = ""
    last_played_team1_rating = 0
    last_played_team2_rating = 0

    # Set more realistic starting scores
    score1, score2 = 0, 0
    game_timer = 0
    game_duration = 10
    last_update_time = pygame.time.get_ticks()
    result_display_time = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_data.save_money(game_data.money)
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    game_data.save_money(game_data.money)
                    return
            elif event.type == pygame.KEYDOWN and not game_running and not showing_results:
                if event.key == pygame.K_ESCAPE:
                    game_data.save_money(game_data.money)
                    return
                elif event.key == pygame.K_SPACE and bet_amount < game_data.money:
                    if bet_amount > game_data.money and game_data.money > 0:
                        result_text = "Not enough money!"
                        bet_amount = 5
                    elif bet_amount < 5:
                        result_text = "Minimum bet is $5!"
                    else:
                        game_data.money -= bet_amount
                        game_running = True
                        last_update_time = pygame.time.get_ticks()
                        # Start with random scores between 0-10 to simulate game already in progress
                        score1, score2 = random.randint(0, 10), random.randint(0, 10)
                        game_timer = 0
                # Add key controls for selecting games (up/down arrows)
                elif event.key == pygame.K_UP:
                    selected_game = (selected_game - 1) % len(matchups)
                elif event.key == pygame.K_DOWN:
                    selected_game = (selected_game + 1) % len(matchups)
                # Add key controls for toggling between teams (left/right arrows)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    selected_team = 1 if selected_team == 0 else 0
                # Add key controls for adjusting bet amount
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    if bet_amount + 5 <= game_data.money:
                     bet_amount += 5
                elif event.key == pygame.K_MINUS:
                    bet_amount = max(5, bet_amount - 5)
            # Add key handling for showing_results state to dismiss results
            elif event.type == pygame.KEYDOWN and showing_results:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    showing_results = False
                    # Generate new matchups only after results are dismissed
                    matchups = generate_matchups()

        SCREEN.blit(court_bg, (0, 0))

        overlay = pygame.Surface((screen_width, 250), pygame.SRCALPHA)
        overlay.fill(BOX_COLOR)
        SCREEN.blit(overlay, (0, 0))

        team1, team2 = matchups[selected_game]
        team1_odds, team2_odds = NBA_TEAMS[team1], NBA_TEAMS[team2]
        team1_rating = team1_odds  # Define ratings here for use throughout
        team2_rating = team2_odds

        selected_team_name = team1 if selected_team == 0 else team2
        selected_team_odds = team1_odds if selected_team == 0 else team2_odds
        opponent_odds = team2_odds if selected_team == 0 else team1_odds
        potential_winnings = calculate_payout(bet_amount, selected_team_odds, opponent_odds)

        SCREEN.blit(font.render(f"Money: ${game_data.money}", True, WHITE), (20, 20))
        SCREEN.blit(font.render(f"Bet: ${bet_amount}", True, WHITE), (20, 60))
        game_data.save_money(game_data.money)

        # Display matchups
        for i, (t1, t2) in enumerate(matchups):
            color = RED if i == selected_game else WHITE
            SCREEN.blit(font.render(f"{t1} ({NBA_TEAMS[t1]}) vs {t2} ({NBA_TEAMS[t2]})", True, color), (20, 100 + i * 30))

        SCREEN.blit(font.render(f"Selected: {selected_team_name} ({selected_team_odds})", True, GREEN), (screen_width - 400, 50))
        SCREEN.blit(font.render(f"Potential Winnings: ${potential_winnings}", True, GREEN), (screen_width - 400, 90))

        # Display controls
        if not game_running and not showing_results:
            control_y = screen_height - 210
            SCREEN.blit(font.render("Controls:", True, WHITE), (screen_width - 550, control_y))
            SCREEN.blit(font.render("Up/Down: Select game", True, WHITE), (screen_width - 550, control_y + 35))
            SCREEN.blit(font.render("Left/Right: Switch team", True, WHITE), (screen_width - 550, control_y + 70))
            SCREEN.blit(font.render("+/-: Adjust bet", True, WHITE), (screen_width - 550, control_y + 105))
            SCREEN.blit(font.render("SPACE: Place bet", True, WHITE), (screen_width - 550, control_y + 140))

        if game_running:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_time >= 1000:
                last_update_time = current_time
                game_timer += 1

                # Factor in team levels for scoring
                team1_rating = NBA_TEAMS[team1]
                team2_rating = NBA_TEAMS[team2]

                # Calculate base scoring ranges based on team ratings
                # Higher rated teams will score more points on average
                team1_min = 4 + (team1_rating - 65) // 10  # Min score increases with team rating
                team1_max = 12 + (team1_rating - 65) // 6   # Max score increases with team rating

                team2_min = 4 + (team2_rating - 65) // 10
                team2_max = 12 + (team2_rating - 65) // 6

                # Add some randomness but maintain the advantage for better teams
                team1_score_increase = random.randint(team1_min, team1_max)
                team2_score_increase = random.randint(team2_min, team2_max)

                # Add a chance for "hot streaks" - occasionally teams go on a run
                if random.random() < 0.2:  # 20% chance of a hot streak
                    if random.random() < team1_rating / (team1_rating + team2_rating):
                        # Team 1 goes on a run
                        team1_score_increase += random.randint(3, 8)
                    else:
                        # Team 2 goes on a run
                        team2_score_increase += random.randint(3, 8)

                score1 += team1_score_increase
                score2 += team2_score_increase

            # Draw an improved scoreboard
            scoreboard_width = 500
            scoreboard_height = 140
            scoreboard_x = screen_width // 2 - scoreboard_width // 2
            scoreboard_y = screen_height // 2 - scoreboard_height // 2

            # Draw scoreboard background
            pygame.draw.rect(SCREEN, (30, 30, 30),
                            (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 0, 10)
            pygame.draw.rect(SCREEN, WHITE,
                            (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 3, 10)

            # Draw team names and scores
            team1_color = GREEN if selected_team == 0 else WHITE
            team2_color = GREEN if selected_team == 1 else WHITE

            # Draw team divider
            pygame.draw.line(SCREEN, WHITE,
                            (screen_width // 2, scoreboard_y + 10),
                            (screen_width // 2, scoreboard_y + scoreboard_height - 10), 3)

            # Team 1 info
            team1_name = team1 if len(team1) < 15 else team1[:12] + "..."
            SCREEN.blit(font.render(team1_name, True, team1_color),
                        (scoreboard_x + 20, scoreboard_y + 20))
            SCREEN.blit(score_font.render(str(score1), True, team1_color),
                        (scoreboard_x + scoreboard_width // 4 - 20, scoreboard_y + 50))

            # Draw team 1 rating below the score
            SCREEN.blit(font.render(f"Rating: {team1_rating}", True, team1_color),
                        (scoreboard_x + 20, scoreboard_y + scoreboard_height - 40))

            # Team 2 info
            team2_name = team2 if len(team2) < 15 else team2[:12] + "..."
            SCREEN.blit(font.render(team2_name, True, team2_color),
                        (scoreboard_x + scoreboard_width // 2 + 20, scoreboard_y + 20))
            SCREEN.blit(score_font.render(str(score2), True, team2_color),
                        (scoreboard_x + scoreboard_width * 3 // 4 - 20, scoreboard_y + 50))

            # Draw team 2 rating below the score
            SCREEN.blit(font.render(f"Rating: {team2_rating}", True, team2_color),
                        (scoreboard_x + scoreboard_width // 2 + 20, scoreboard_y + scoreboard_height - 40))

            if game_timer >= game_duration:
                # Save the teams before generating new matchups
                last_played_team1 = team1
                last_played_team2 = team2
                last_played_team1_rating = team1_rating
                last_played_team2_rating = team2_rating

                # Make sure the final scores are in the NBA range (80-130)
                # But still factor in team ratings for the final adjustment
                team1_boost = (team1_rating - 65) // 3
                team2_boost = (team2_rating - 65) // 3

                base_score1 = 80 + team1_boost
                base_score2 = 80 + team2_boost

                # Calculate how many more points needed to reach the base score
                score1_needed = max(0, base_score1 - score1)
                score2_needed = max(0, base_score2 - score2)

                # Add the needed points plus a random amount up to 20
                final_score1 = score1 + score1_needed + random.randint(0, 20)
                final_score2 = score2 + score2_needed + random.randint(0, 20)

                # Cap at 130
                final_score1 = min(130, final_score1)
                final_score2 = min(130, final_score2)

                # Make sure scores are different to avoid ties
                if final_score1 == final_score2:
                    # The team with the higher rating is more likely to win in a tie
                    if random.random() < team1_rating / (team1_rating + team2_rating):
                        final_score1 += random.randint(1, 3)
                    else:
                        final_score2 += random.randint(1, 3)

                score1, score2 = final_score1, final_score2
                game_running = False
                showing_results = True
                result_display_time = pygame.time.get_ticks()
                winner = last_played_team1 if score1 > score2 else last_played_team2
                if winner == selected_team_name:
                    game_data.money += potential_winnings
                    game_data.save_money(game_data.money)
                    result_text = f"{winner} won! You won ${potential_winnings}!"
                else:
                    result_text = f"{winner} won! You lost."

        if showing_results:
            # Use the saved team names instead of current matchup
            display_team1 = last_played_team1
            display_team2 = last_played_team2

            # Draw final scoreboard
            scoreboard_width = 500
            scoreboard_height = 140
            scoreboard_x = screen_width // 2 - scoreboard_width // 2
            scoreboard_y = screen_height // 2 - 100

            # Draw scoreboard background
            pygame.draw.rect(SCREEN, (30, 30, 30),
                           (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 0, 10)
            pygame.draw.rect(SCREEN, WHITE,
                           (scoreboard_x, scoreboard_y, scoreboard_width, scoreboard_height), 3, 10)

            # Draw FINAL text
            SCREEN.blit(font.render("FINAL", True, RED),
                       (scoreboard_x + scoreboard_width // 2 - 40, scoreboard_y + 5))

            # Draw team names and scores
            team1_color = GREEN if score1 > score2 else WHITE
            team2_color = GREEN if score2 > score1 else WHITE

            # Draw team divider
            pygame.draw.line(SCREEN, WHITE,
                            (screen_width // 2, scoreboard_y + 30),
                            (screen_width // 2, scoreboard_y + scoreboard_height - 10), 3)

            # Team 1 info
            team1_name = display_team1 if len(display_team1) < 15 else display_team1[:12] + "..."
            SCREEN.blit(font.render(team1_name, True, team1_color),
                        (scoreboard_x + 20, scoreboard_y + 40))
            SCREEN.blit(score_font.render(str(score1), True, team1_color),
                        (scoreboard_x + scoreboard_width // 4 - 20, scoreboard_y + 65))



            # Team 2 info
            team2_name = display_team2 if len(display_team2) < 15 else display_team2[:12] + "..."
            SCREEN.blit(font.render(team2_name, True, team2_color),
                        (scoreboard_x + scoreboard_width // 2 + 20, scoreboard_y + 40))
            SCREEN.blit(score_font.render(str(score2), True, team2_color),
                        (scoreboard_x + scoreboard_width * 3 // 4 - 20, scoreboard_y + 65))


            # Draw result message
            results_bg = pygame.Surface((500, 80), pygame.SRCALPHA)
            results_bg.fill((0, 0, 0, 220))
            SCREEN.blit(results_bg, (screen_width // 2 - 250, screen_height // 2 + 80))

            result_color = GREEN if "won!" in result_text else RED
            SCREEN.blit(result_font.render(result_text, True, result_color),
                       (screen_width // 2 - 240, screen_height // 2 + 90))
            SCREEN.blit(font.render("Press SPACE or ENTER to continue", True, WHITE),
                       (screen_width // 2 - 230, screen_height // 2 + 135))

        pygame.draw.rect(SCREEN, RED, exit_button)
        SCREEN.blit(font.render("Exit", True, WHITE), (30, screen_height - 45))

        pygame.display.flip()
