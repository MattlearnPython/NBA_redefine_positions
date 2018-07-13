#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 13:57:10 2018

@author: jinzhao
"""
import numpy as np
import pandas as pd
from selenium import webdriver
import time
import csv

# Old versions
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
def get_per_game(url):
    # Setup
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    # Get data from last 5 seasons (2013 - 2018)
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    seasons = driver.find_elements_by_xpath("//table[@id='per_game']/tbody/tr")
    if len(seasons) >= 3:
        seasons = seasons[-3: ]
    
    # Loop through these seasons and store data in a table 
    table = []
    for season in seasons:
        cells = season.find_elements_by_tag_name('td')
        row = []
        for cell in cells:
            row.append(cell.text)
        table.append(row)
   
    # Get header from last 5 season
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    headers = driver.find_elements_by_xpath("//table[@id='per_game']/thead/tr/th")
    headerList = []
    for header in headers:
        headerList.append(header.text)
    del headerList[0]
    
    driver.close()
     
    # Preprocess data
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    df = pd.DataFrame(table, columns=headerList)
    
    pos = label_position(df.Pos[0])
    
    df = df.drop(columns=['Age', 'Tm', 'Lg', 'Pos', 'GS'])
    
    # Check if some data is missed
    for index, row in df.iterrows():
        for col in df:
            if row[col] == '':
                df[col][index] = 0
                print(url)
                
    df = df.astype(float)
    
    dataSet = np.mean(df.values, axis=0)
    
    return dataSet, pos

def get_player_name(url):
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    players = driver.find_elements_by_xpath("//table[@class='sortable stats_table now_sortable'] \
                                            /tbody/tr/th/strong")     
    activePlayers = []
    for player in players:
        name = player.text
        activePlayers.append(name)
    driver.close()
    
    return activePlayers

def get_player_url(url, activePlayers):
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    players = driver.find_elements_by_xpath("//table[@class='sortable stats_table now_sortable'] \
                                        /tbody/tr/th//a")
    activePlayerUrls = []
    for player in players:
        if player.text in activePlayers:
            activePlayerUrls.append(player.get_attribute("href"))
            
    driver.close()
    
    return activePlayerUrls

# New versions
# ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
def get_active_player(url):
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    # 1. Get all player names
    playerNames = driver.find_elements_by_xpath("//table[@class='sortable stats_table now_sortable'] \
                                        /tbody/tr/th")
    player_names = []
    for name in playerNames:
        player_names.append(name.text)
    
    if len(player_names) == 0:
        return None
    
    # 2. Get all player years
    playerYears = driver.find_elements_by_xpath("//td[@data-stat = 'year_max']")
    player_years = []
    for year in playerYears:
        player_years.append(year.text)
    
    # 3. Select active players
    num_players = len(player_names)
    active_players = []
    for i in range(num_players):
        if player_years[i] == '2018':
            active_players.append(player_names[i])
    
    # 4. get active player url
    playerUrls = driver.find_elements_by_xpath("//table[@class='sortable stats_table now_sortable'] \
                                        /tbody/tr/th//a")
    active_player_urls = []
    for item in playerUrls:
        if item.text in active_players:
            active_player_urls.append(item.get_attribute("href"))
    
    driver.close()
    
    player_info = zip(active_players, active_player_urls)
    
    return player_info

def get_perGame_header(url):
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    headers = driver.find_elements_by_xpath("//table[@id='per_game']/thead/tr/th")
    headerList = []
    for header in headers:
        headerList.append(header.text)
    del headerList[0]
    driver.close()
    
    return headerList

def get_perGame_2018(url):
    # Setup
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    # Get data from the last season
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    row = driver.find_elements_by_xpath("//tr[@id = 'per_game.2018']/td")
    
    if len(row) == 0:
        print('Error ')
        print(url)
        driver.close()
        return None, None
        
    # Loop through these seasons and store data in a table 
    data = []
    n = 0
    for cell in row:
        if n == 4 and float(cell.text) <= 50:
            driver.close()
            return None, None
        else:    
            data.append(cell.text)
        
        # 28 category in headers
        if n == 28:
            break
        
        n += 1
    driver.close()
    
    # Get the position
    pos = label_position(data[3])
    if pos is None:
        print("No such position found!")
        print(url)
        return None, None
    # Delete element in reversed order
    del_list = [5, 3, 2, 1, 0]
    for index in del_list:
        del data[index]
    
    for i in range(len(data)):
        if data[i] == '':
            return None, None
        else:
            data[i] = float(data[i])
        
    data = np.array(data)
    
    return data, pos

def get_pos_tmp(url):
    # Setup
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- -----
    driver = webdriver.Chrome('/Users/jinzhao/Desktop/Machine_Learning/NBA/nba_redefine_position/chromedriver')
    driver.get(url)
    
    row = driver.find_elements_by_xpath("//tr[@id = 'per_game.2018']/td")
    
    if len(row) == 0:
        print('Error ')
        print(url)
        driver.close()
        return None
    
    n_game_played = driver.find_element_by_xpath("//tr[@id = 'per_game.2018']/td[5]").text
    if n_game_played <= '50':
        driver.close()
        return None
    else:
        pos = driver.find_element_by_xpath("//tr[@id = 'per_game.2018']/td[4]").text
        driver.close()
        return label_position(pos)      

def label_position(pos):
    if pos == 'C':
        return 5
    elif pos == 'PF':
        return 4
    elif pos == 'SF':
        return 3
    elif pos == 'SG':
        return 2
    elif pos == 'PG':
        return 1
    else:
        return None


if __name__ == '__main__':
    
    # Scraping data
    # ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== ===== 
    
    # 1. Scrape active players' NAME and URL ('Active' means 2017-2018)
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    all_info = []
    for idx in range(97, 123):
        url = 'https://www.basketball-reference.com/players/' + chr(idx) + '/'
        player_info = get_active_player(url)
        all_info.append(player_info)
        
    # Write data to CSV file
    with open('data_player_url.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(("Name", "Url"))
        for item in all_info:
            if item is not None:
                for pair in item:
                    writer.writerow(pair)
            writer.writerow('')
            
            
    # 2. Scrape active players' POSITION 
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    all_info = []
    with open('data_player_url.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[0] != '':
                all_info.append(line) # row[0] is player's name
    # Delete header
    del all_info[0]
    #all_info = all_info[0:2]
    
    positions = []
    player_ID = []
    for index in range(len(all_info)):
        url = all_info[index][1]
        pos = get_pos_tmp(url)
        if pos is not None:
            positions.append(pos)
            player_ID.append(all_info[index])
        print("Current progress: ", index / 540 * 100, '%')
    
    with open('data_player_pos.csv', 'w') as file:
        writer = csv.writer(file)
        header = ['Name', 'Url', 'Pos']
        writer.writerow(header)
        for idx in range(len(positions)):
            data_new = player_ID[idx] + [positions[idx]]
            writer.writerow(data_new)
    
    # 3. Scrape active players' PERFORMANCE 
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    # <1> Read Urls from file
    all_info = []
    with open('data_player_url.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            if line[0] != '':
                all_info.append(line) # row[0] is player's name
    # Delete header
    del all_info[0]
    
    # <2> Read data from Urls
    header = ['G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',  '2P', '2PA', '2P%', 
              'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
    length = len(header)
    
    dataset = np.zeros((1, length))   
    positions = []
    player_ID = []
    for index in range(len(all_info)):
        url = all_info[index][1]
        data, pos = get_perGame_2018(url)
        if data is not None and pos is not None:
            dataset = np.vstack((dataset, data))
            positions.append(pos)
            player_ID.append(all_info[index])
        print("Current progress: ", index / 540 * 100, '%')
    dataset = np.delete(dataset, 0, axis = 0)
    
    # <3> Save data for future use
    with open('data_player_perfomace.csv', 'w') as file:
        writer = csv.writer(file)
        header_new = ['Name', 'Url'] + header
        writer.writerow(header_new)
        for idx in range(dataset.shape[0]):
            data_new = player_ID[idx] + list(dataset[idx])
            writer.writerow(data_new)
    
    # 4. Combine active players' PERFORMANCE and POSITION
    # ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- ----- 
    player_performance = []
    with open('data_player_performance.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            player_performance.append(line)     
    del player_performance[0]

    player_position = []
    with open('data_player_pos.csv', 'r') as file:
        reader = csv.reader(file)
        for line in reader:
            player_position.append(line)     
    del player_position[0]   

    n_players = len(player_performance)
    for i in range(n_players):
        name = player_performance[i][0]
        for j in range(len(player_position)):
            print(1)
            name_match = player_position[j][0]
            if name == name_match:
                player_performance[i].append(player_position[j][2])
                
    with open('data_2018.csv', 'w') as file:
        writer = csv.writer(file)
        header = ['Name', 'Url', 'G', 'MP', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%',  '2P', '2PA', '2P%', 
              'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'Pos']
        writer.writerow(header)
        for idx in range(len(player_performance)):
            writer.writerow(player_performance[idx])
            
            


     
        


