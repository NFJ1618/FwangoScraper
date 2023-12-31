from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
import time
from datatypes import TeamObject, TournamentData, GameData, SeriesData, TeamResultObject
import re
import os

#setTimeout(() => { debugger; }, 5000)


xpaths = [
    "//*[@id='root']/span/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div/nav/ul[2]/li[3]/div/a/span/i",
    "//*[@id='root']/span/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div/nav/ul[2]/li[4]/div/a/span/i",
    "//*[@id='root']/span/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div/nav/ul[2]/li[2]/div/a/span/i",
    "//*[@id='root']/span/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div/div/nav/ul[2]/li[1]/div/a/span/i"
]

class FwangoScraper:
    def __init__(self, tourney_path) -> None:      
        # if swap_bracket_and_pool:
        #     self.POOL_PLAY_XPATH = BRACKET_XPATH
        #     self.BRACKET_XPATH = POOL_PLAY_XPATH
        # else:
        #     self.POOL_PLAY_XPATH = POOL_PLAY_XPATH
        #     self.BRACKET_XPATH = BRACKET_XPATH
        self.this_tournaments_react_number = 2
        self.quiet = False
        self.tournament_specific_team_player_mappings = {}
        self.width = 1450
        self.height = 1400
        self.tourney_path = tourney_path
        self.BRACKET_PLAY_XPATH, self.POOL_PLAY_XPATH, self.HOME_XPATH, self.RESULTS_XPATH = "", "", "", ""

    def run(self, tournaments):
        # Set up ChromeDriver automatically
        driver = webdriver.Chrome()

        tournament_names = tournaments



        program_start_time = time.time()

        for i, tourney_name in enumerate(tournament_names):
            team_objects = []
            division_team_results = []
            games = []
            series = []
            tournament_objects = []

            start_time = time.time()
            self.tournament_specific_team_player_mappings[tourney_name] = {}

            print(f"Currently working on: {tourney_name} ({i + 1} out of {len(tournament_names)})")

            url = f"https://fwango.io/{tourney_name}"
            driver.set_window_size(self.width, self.height)  # Set window size

            print("Working on home page")
            self.process_home_page(driver, url, tourney_name, team_objects, tournament_objects)

            print("Working on results page")
            self.process_results_page(driver, url, division_team_results, tourney_name)

            print("Working on pool play page")
            self.process_pool_play(driver, url, tourney_name, games)

            print("Working on bracket play page")
            self.process_bracket_play(driver, url, tourney_name, games, series)



            # print_data(team_objects, division_team_results, games, series)

            # I'm assuming you have write_data_to_csv function defined elsewhere
            os.makedirs(f"{self.tourney_path}/{tourney_name}", exist_ok=True)
            self.write_data_to_csv("teamObjects", f"{self.tourney_path}/{tourney_name}/teamObjects.csv", team_objects)
            self.write_data_to_csv("divisionTeamResults", f"{self.tourney_path}/{tourney_name}/divisionTeamResults.csv", division_team_results)
            self.write_data_to_csv("games", f"{self.tourney_path}/{tourney_name}/games.csv", games)
            self.write_data_to_csv("series", f"{self.tourney_path}/{tourney_name}/series.csv", series)
            self.write_data_to_csv("tournaments", f"{self.tourney_path}/tournaments.csv", tournament_objects)
            
            end_time = time.time()  # Capture end timeRF
            elapsed_time = end_time - start_time  # Calculate elapsed time

            print(f"{len(team_objects)} teams")
            print(f"{len(division_team_results)} records")
            print(f"{len(games)} games")
            print(f"{len(series)} series")
            print(f"Iteration took {elapsed_time * 1000} milliseconds")
            
        program_end_time = time.time()  # Capture end time
        program_elapsed_time = program_end_time - program_start_time  # Calculate elapsed time

        print(f"{len(tournament_names)} tournaments took {program_elapsed_time * 1000} milliseconds")
        driver.quit()
        
    def set_xpaths(self, driver):
        for path in xpaths:
            a = driver.find_elements(By.XPATH, path)
            if a:
                if a[0].get_attribute("class") == "far fa-list-alt fa-fw":
                    if not self.POOL_PLAY_XPATH:
                        self.POOL_PLAY_XPATH = path
                elif a[0].get_attribute("class") == "fas fa-project-diagram fa-fw":
                    if not self.BRACKET_PLAY_XPATH:
                        self.BRACKET_PLAY_XPATH = path
                elif a[0].get_attribute("class") == "fas fa-home fa-fw":
                    if not self.HOME_XPATH:
                        self.HOME_XPATH = path
                elif a[0].get_attribute("class") == "fas fa-trophy fa-fw":
                    if not self.RESULTS_XPATH:
                        self.RESULTS_XPATH = path
        


    def print_data(self, team_objects, division_team_results, games, series):
        for team in team_objects:
            team.print()
        for result in division_team_results:
            result.print()
        for game in games:
            game.print()
        for this_series in series:
            this_series.print()

    def write_data_to_csv(self, dataset_name, csv_file_path, dataset):
        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write header row based on dataset type
            headers = []
            if dataset_name == "teamObjects":
                headers = ["Player 1", "Player 2", "Team Name", "Division", "Tournament"]
            elif dataset_name == "divisionTeamResults":
                headers = ["Team Name", "Wins", "Losses", "Result", "Division", "Tournament"]
            elif dataset_name == "games":
                headers = ["Team 1", "Team 2", "Players 1", "Players 2", "Score 1", "Score 2", "Tournament Stage", "Tournament Name", "Division"]
            elif dataset_name == "series":
                headers = ["Team 1", "Team 2", "Round", "Tournament", "Team 1 Scores", "Team 2 Scores", "Division"]
            elif dataset_name == "tournaments":
                headers = ["Tournament Name", "URL", "Date"]

            if dataset_name != "tournaments":
                writer.writerow(headers)

            # Write data rows
            for data in dataset:
                row = []

                if isinstance(data, TeamObject):
                    row = [data.player1, data.player2, data.team_name, data.division, data.tournament]
                elif isinstance(data, TeamResultObject):
                    row = [data.team_name, str(data.wins), str(data.losses), data.result, data.division, data.tournament]
                elif isinstance(data, GameData):
                    if not (data.team1 and data.team2):
                        continue
                    if f"{data.division}_{data.team1}" not in self.tournament_specific_team_player_mappings[data.tournament_name]:
                        continue
                    if f"{data.division}_{data.team2}" not in self.tournament_specific_team_player_mappings[data.tournament_name]:
                        continue
                    t1p1, t1p2 = self.tournament_specific_team_player_mappings[data.tournament_name][f"{data.division}_{data.team1}"]
                    t2p1, t2p2 = self.tournament_specific_team_player_mappings[data.tournament_name][f"{data.division}_{data.team2}"]
                    row = [data.team1, data.team2, f"{t1p1}, {t1p2}", f"{t2p1}, {t2p2}", str(data.t1_points), str(data.t2_points), data.tournament_stage, data.tournament_name, data.division]
                elif isinstance(data, SeriesData):
                    row = [data.team1, data.team2, data.round, data.tournament, str(data.t1_scores), str(data.t2_scores), data.division]
                elif isinstance(data, TournamentData):
                    row = [data.name, data.url, data.date]

                writer.writerow(row)


    def process_home_page(self, driver, url, tourney_name, team_objects, tournament_objects):
        try:
            driver.get(url)
            time.sleep(2)

            # Wait for the page to fully load
            WebDriverWait(driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(1)
            self.set_xpaths(driver)

            # Get tournament date
            tourney_date_element = driver.find_element(By.CLASS_NAME, "date")
            this_tournament = TournamentData()
            this_tournament.date = tourney_date_element.text
            this_tournament.name = tourney_name
            this_tournament.url = url
            tournament_objects.append(this_tournament)

            # Here, I assume you have a function named get_team_names, but it wasn't provided in the original Java
            new_team_names = []
            player_names = []
            self.get_team_names(driver, new_team_names, "", player_names)
            
            divisions = driver.find_elements(By.CSS_SELECTOR, "h5.TournamentTeamList__DivisionTitle-sc-13mkiy8-2.cGNVUd")
            divisions = [i.text for i in divisions]
            container = driver.find_element(By.CSS_SELECTOR, "div.TournamentTeamList__Container-sc-13mkiy8-0.irfjog")

            last_loaded_team_name = ""
            last_last_loaded_team_name = ""

            short_loading_delay = 0.3
            actions = ActionChains(driver)
            # actions.move_to_element(container).click().perform()
            while last_loaded_team_name != new_team_names[-1] and last_last_loaded_team_name != new_team_names[-1]:
                last_last_loaded_team_name = last_loaded_team_name
                last_loaded_team_name = new_team_names[-1]
                actions.send_keys_to_element(container, Keys.PAGE_DOWN).perform()

                # Pause for a short duration to allow new content to load
                time.sleep(short_loading_delay)  # Adjust this duration if needed

                # Fetch the team names
                division = self.get_team_names(driver, new_team_names, last_loaded_team_name, player_names)
                if len(division) > 0:
                    divisions.extend(division)
                

            
            divisions = self.clean_up_divisions(divisions)
            unique_player_names_and_team_names = self.remove_non_unique_combinations(player_names, new_team_names)
            divisions, split_players = self.split_into_divisions(divisions, unique_player_names_and_team_names)
            
            for division, unique_player_names_and_team_names in zip(divisions, split_players):
                if division != 'Free Agent':
                    for unique_name in unique_player_names_and_team_names:
                        parts1 = unique_name.split("UNIQUESPLITTERDONOTREPEAT")
                        parts2 = sorted(parts1[0].split(" and "))
                        this_team = TeamObject()
                        this_team.team_name = parts1[1]

                        if len(parts2) == 2:
                            first_player = parts2[0].lower()
                            second_player = parts2[1].lower()
                            this_team.player1 = first_player
                            this_team.player2 = second_player
                            this_team.tournament = tourney_name
                            this_team.division = division
                            team_objects.append(this_team)
                            self.tournament_specific_team_player_mappings[tourney_name][f"{division}_{this_team.team_name}"] = (this_team.player1, this_team.player2)

        except Exception as e:
            if not self.quiet:
                print(e)


    def split_into_divisions(self, divisions, player_team_names):
        divs = []
        number_in_div = []
        split = []
        player_team_names = player_team_names[::-1]
        for i in divisions:
            name, num = i.split('\n')
            num = int(num.strip('()'))
            divs.append(name)
            number_in_div.append(num)
            players = []
            for i in range(num):
                if player_team_names:
                    players.append(player_team_names.pop())
            split.append(players)
        # free_agent = divs.index('Free Agent')
        # divs.pop(free_agent)
        # split.pop(free_agent)
        return divs, split


    def clean_up_divisions(self, divisions):
        s = set()
        d = []
        for i in divisions:
            if i not in s:
                s.add(i)
                d.append(i)
        return d

    def get_team_names(self, driver, team_names, last_team_name, player_names):
        team_name_elements = driver.find_elements(By.CSS_SELECTOR, "div.team-info-gist")
        # players_elements = driver.find_elements(By.CLASS_NAME, "players")
        try:
            division = driver.find_elements(By.CSS_SELECTOR, "h5.TournamentTeamList__DivisionTitle-sc-13mkiy8-2.cGNVUd")
            division = [i.text for i in division]
        except NoSuchElementException:
            division = []

        for i in team_name_elements:
            if not i.text.startswith('Traceback'):
                try:
                    team_name, names = i.text.split('\n')
                    team_names.append(team_name)
                    player_names.append(names)
                except:
                    # non responsive
                    pass

        return division

    def process_results_page(self, driver, url, division_team_results, tournament):
        try:
            driver.get(f"{url}/results")

            # Wait for the page to fully load
            WebDriverWait(driver, 30).until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            time.sleep(2)

            # Locate the dropdown button element
            dropdown_button = driver.find_element(By.CLASS_NAME, "select-input-container")

            self.results_processing_helper(driver, dropdown_button, division_team_results, tournament)
        except Exception as e:
            if not self.quiet:
                print(e)

    def results_processing_helper(self, driver, dropdown_button, division_team_results, tournament):
        try:
            found_react_number = False
            for j in range(10): # the j number changes depending on the tournament
                element_found = True
                if found_react_number:
                    break
                i = 0
                while element_found:
                    element_id = f"react-select-{j}-option-{i}"
                    try:
                        # Click on the dropdown button
                        dropdown_button.click()
                        time.sleep(0.3)
                        option_element = driver.find_element(By.ID, element_id)
                        division = option_element.text
                        # if division.lower() == "free agent":
                        #     continue
                        option_element.click()
                        self.this_tournaments_react_number = j
                        found_react_number = True
                        time.sleep(1)
                        results = []
                        self.get_results_data(driver, results, division, tournament)
                        division_team_results.extend(results)

                        i += 1
                    except NoSuchElementException:
                        element_found = False
        except Exception as e:
            if not self.quiet:
                print(e)

    def get_results_data(self, driver, team_results, division, tournament):
        # These will all match in terms of order of items
        if division.lower() == 'free agent':
            return
        team_name_elements = driver.find_elements(By.CLASS_NAME, "team-name")
        record_elements = driver.find_elements(By.CLASS_NAME, "record-column")
        rank_elements = driver.find_elements(By.CSS_SELECTOR, "td.rank-column")
        if record_elements:
            record_elements.pop(0)  # Remove the first element
        for i in range(len(record_elements)):
            this_result = TeamResultObject()
            if i < 3 and rank_elements:
                this_result.result = i+1
            elif rank_elements:
                try:
                    this_result.result = int(rank_elements[i].text)
                except:
                    pass
            team_name = team_name_elements[i].text
            record = record_elements[i].text
            this_result.team_name = team_name
            try:
                parts = record.split(" - ")
                if len(parts) == 2:
                    wins = self.extract_number(parts[0])
                    losses = self.extract_number(parts[1])
                    this_result.wins = wins
                    this_result.losses = losses
            except Exception as e:
                if not self.quiet:
                    print(e)
            this_result.division = division
            this_result.tournament = tournament
            team_results.append(this_result)

    def process_pool_play(self, driver, url, tournament_name, games):
        try:
            driver.get(url)
            time.sleep(2)

            # Locate the pool play button element
            pool_play_button = driver.find_element(By.XPATH, self.POOL_PLAY_XPATH)
            pool_play_button.click()
            time.sleep(1)

            dropdown_button = driver.find_element(By.CLASS_NAME, "select-input-container")
            self.pool_play_helper(driver, dropdown_button, games, tournament_name)
        except Exception as e:
            if not self.quiet:
                print(e)

    def pool_play_helper(self, driver, dropdown_button, division_game_results, tournament_name):
        try:
            slot = 0
            element_found = True
            while element_found:
                element_id = f"react-select-{self.this_tournaments_react_number}-option-{slot}"
                try:
                    action = ActionChains(driver)
                    body = driver.find_element(By.TAG_NAME, 'body')
                    action.move_to_element_with_offset(body, 0,0).move_by_offset(0, 1).click().perform()
                    time.sleep(0.1)
                    dropdown_button.click()
                    time.sleep(0.1)
                    option_element = driver.find_element(By.ID, element_id)
                    division = option_element.text
                    # if division.lower() == "free agent":
                    #     option_element.click()
                    #     slot += 1
                    #     continue
                    option_element.click()
                    time.sleep(1)
                    games = []

                    # Scroll and load more content
                    try:
                        container = driver.find_element(By.CSS_SELECTOR, "#body-scroll > div > div > div.infinite-scroll-component__outerdiv")
                    except:
                        slot += 1
                        continue

                    # while time.time() - start_time < duration_secs:
                    
                    reached_page_end = False
                    last_height = container.size['height']
                    last_offset = container.location['y']
                    while not reached_page_end:
                        action.send_keys_to_element(container, Keys.PAGE_DOWN).perform()
                        time.sleep(0.1)
                        new_height = container.size['height']
                        new_offset = container.location['y']
                        if last_height == new_height and last_offset == new_offset:
                            reached_page_end = True
                        else:
                            last_height = new_height
                            last_offset = new_offset

                    self.get_pool_play_data(driver, games, tournament_name, division)
                    division_game_results.extend(games)
                    action.send_keys_to_element(container, Keys.HOME).perform()
                    slot += 1
                except NoSuchElementException:
                    element_found = False
        except Exception as e:
            if not self.quiet:
                print(e)

    def remove_non_unique_combinations(self, player_names, team_names):
        unique_combinations = set()
        non_unique_combinations = []

        for i in range(len(player_names)):
            combination = player_names[i] + "UNIQUESPLITTERDONOTREPEAT" + team_names[i]
            if combination not in unique_combinations:
                unique_combinations.add(combination)
                non_unique_combinations.append(combination)

        return non_unique_combinations

    def extract_number(self, input_str):
        matches = re.findall(r'\d+', input_str)
        if matches:
            return int(matches[0])
        return 0

    def get_pool_play_data(self, driver, games, tournament_name, division):
        team_elements = driver.find_elements(By.CLASS_NAME, "teams-container")
        point_elements = driver.find_elements(By.CLASS_NAME, "games-container")

        for i in range(len(team_elements)):
            name_elements = team_elements[i].find_elements(By.CLASS_NAME, "team-name")
            score_element = point_elements[i].find_elements(By.CSS_SELECTOR, "[type='number']")
            these_games = [GameData() for i in range(len(score_element)//2)]
            for i, this_game in enumerate(these_games):
                try:
                    this_game.team1 = name_elements[0].text
                except:
                    pass
                try:
                    this_game.team2 = name_elements[1].text
                except:
                    pass
                try:
                    this_game.t1_points = int(score_element[2*i].get_attribute("value"))
                    this_game.t2_points = int(score_element[2*i+1].get_attribute("value"))
                except:
                    pass
                this_game.division = division
                this_game.tournament_stage = "Pool Play"
                this_game.tournament_name = tournament_name
                this_game.division = division
            games.extend(these_games)


    def process_bracket_play(self, driver, url, tournament_name, all_games, all_series):
        try:
            # Going to add a game_data object for each game in the bracket and a series object for each series
            driver.get(url)
            time.sleep(2)
            
            # Locate the bracket play button element
            bracket_play_button = driver.find_element(By.XPATH, self.BRACKET_PLAY_XPATH)
            bracket_play_button.click()
            time.sleep(1)
            self.zoom_out(driver)
            time.sleep(0.1)
            buttons = driver.find_elements(By.CLASS_NAME, "select-input-container")
            # dropdown_button.click()
            # draw_button.send_keys(Keys.RETURN)
            self.bracket_play_helper(driver, buttons, all_games, all_series, tournament_name)
            # self.zoom_in(driver)
        except Exception as e:
            # self.zoom_out(driver)
            if not self.quiet:
                print(e)

    def zoom_out(self, driver):
        try:
            menu = driver.find_element(By.CLASS_NAME, "IconButtonBase-sc-g1y1-0.IconButtonSolid-sc-q6gfks-0.gJLpLb.jGWydz")
            menu.click()
            symmetric = driver.find_element(By.CLASS_NAME, "DropdownMenu__MenuItem-sc-1rahj45-3.bkppMm")
            symmetric.click()
        except:
            pass
        # driver.set_window_size(1800, 1200)
        time.sleep(0.5)

    def zoom_in(self, driver):
        driver.set_window_size(self.width, self.height)
        time.sleep(0.5)

        
            

    def bracket_play_helper(self, driver, buttons, all_games, all_series, tournament_name):
        
        
        try:
            div_index = 0
            element_found = True


            while element_found:

                element_id = f"react-select-{self.this_tournaments_react_number}-option-{div_index}"
                
                #
                # try:
                #     dropdown_button, draw_button = driver.find_elements(By.CLASS_NAME, "select-input-container")
                # except:
                #     if div_index == 10:
                #         break
                #     div_index += 1
                #     continue
                #
            
                ### USE SELECT OBJECT -. 
                
                try:
                    # Click on the dropdown button
                    dropdown_button = buttons[0]
                    dropdown_button.click()
                    time.sleep(0.1)

                    option_element = driver.find_element(By.ID, element_id)
                    time.sleep(0.1)
                    
                    #
                    
                    #
                    try:
                        division = option_element.text
                    except:
                        continue
                    
                    games = []
                    series = []
                    #
                    #
                    
                    if division.lower() == "free agent":
                        option_element.click()
                        div_index += 1
                        continue
                    
                    try:
                        option_element.click()
                    except:
                        continue
                    time.sleep(1)

                    self.zoom_out(driver)
                    for bracket_index in range(0, 2):
                        second_element_found = True
                        draw_index = 0
                        while second_element_found:
                            second_element_id = f"react-select-{self.this_tournaments_react_number+1}-option-{bracket_index}-{draw_index}" 
                            try:
                                buttons = driver.find_elements(By.CLASS_NAME, "select-input-container")
                                if len(buttons) < 2:
                                    break
                                draw_button = buttons[1]
                                draw_button.click()
                                time.sleep(0.1)
                                second_option_element = driver.find_element(By.ID, second_element_id)
                                draw = second_option_element.text
                                second_option_element.click()
                                time.sleep(0.1)

                                games, series = self.process_draw(driver, tournament_name, division)
                                all_games.extend(games)
                                all_series.extend(series)
                                draw_index += 1
                            except NoSuchElementException:
                                second_element_found = False
                                draw_button.click()
                            except:
                                break

                    # Need to scroll out a bit to see all series
                    # start_time = time.time()
                    duration_secs = 1  # 1 second
                    
                    # container = driver.find_element(By.CSS_SELECTOR, "#body-scroll > div > div > div > div.react-transform-component.TransformComponent-module_container__3NwNd > div > div > div > div")
                    
                    # actions = ActionChains(driver
                    # actions.move_to_element(container).send_keys(Keys.PAGE_DOWN).perform()
                    all_series.extend(series)
                    all_games.extend(games)

                    div_index += 1
                except:
                    element_found = False
        except Exception as e:
            if not self.quiet:
                print(e)


    def process_draw(self, driver, tournament_name, division):
        
        games, series = [], []
        
        try:
            container = driver.find_element(By.CLASS_NAME, "Bracketsstyle__BracketDrawContainer-sc-vcines-2.iSmTud")
            rounds = driver.find_elements(By.CLASS_NAME, "Bracketsstyle__BracketDrawColumn-sc-vcines-6.eHosNn")
            titles = container.find_elements(By.CLASS_NAME, "title")


            for round_elem, title in zip(rounds, titles):
                current_round = title.text
                series_elements = round_elem.find_elements(By.CLASS_NAME, "Matchstyle__BracketMatchContainer-sc-18us5a1-2")

                is_final = True
                for series_element in series_elements:
                    if current_round == "Final" and not is_final:
                        current_round = "Third Place"
                    else:
                        is_final = False

                    try:
                        team_name_elements = series_element.find_elements(By.CLASS_NAME, "team-name")
                    except Exception:
                        continue

                    try:
                        score_elements = series_element.find_element(By.CLASS_NAME, "games-container").find_elements(By.CSS_SELECTOR, "[type='number']")
                    except Exception:
                        continue

                    team1 = team_name_elements[0].text
                    team2 = team_name_elements[1].text

                    t1_scores = []
                    t2_scores = []

                    for k, score_element in enumerate(score_elements):
                        try:
                            score = int(score_element.get_attribute("value"))
                            if k % 2 == 0:
                                t1_scores.append(score)
                            else:
                                t2_scores.append(score)
                        except Exception:
                            score = -1
                            if k % 2 == 0:
                                t1_scores.append(score)
                            else:
                                t2_scores.append(score)

                    this_series = SeriesData()  # Assuming you've defined a SeriesData class in Python
                    this_series.team1 = team1
                    this_series.team2 = team2
                    this_series.round = current_round
                    this_series.tournament = tournament_name
                    this_series.t1_scores = t1_scores
                    this_series.t2_scores = t2_scores
                    this_series.division = division
                    series.append(this_series)

                    # Now adding each individual game from the series
                    for k, (t1_score, t2_score) in enumerate(zip(t1_scores, t2_scores)):
                        this_game = GameData()  # Assuming you've defined a GameData class in Python
                        this_game.team1 = team1
                        this_game.team2 = team2
                        this_game.t1_points = t1_score
                        this_game.t2_points = t2_score
                        this_game.tournament_name = tournament_name
                        this_game.tournament_stage = f"Bracket play round of {current_round} game {k+1}"
                        this_game.division = division
                        games.append(this_game)
        except:
            pass
        return games, series


if __name__ == "__main__":
    scraper = FwangoScraper("../data/sts")
    scraper.run([
            # "saltlakecity2023",
            "richmond2023",
            # ...
            # "etsprague2023",
            # "tograndslam2023"
        ])
