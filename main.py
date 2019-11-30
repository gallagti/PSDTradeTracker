# Author: Tim Gallagher
# Date: 11/29/19
# Version: 1.1.3
# Project title: Python trade tracker
# Description: Project takes in OOTP CSV files and outputs a condensed CSV with all trades in the league
# Calculates several different types of WAR, switches player IDs, and creates a readable CSV


import csv
import time
import datetime


def tNumberToName(teamID, teams):
    for team in teams:
        if teamID == team[0]:
            return team[1]


def pNumberToName(playerID, players):
    realID = int(playerID) - 1
    return players[realID][1] + ' ' + players[realID][2]


def statsWarLookup(playerID, teamID, pWar, bWar, year):
    teamBattingWar = 0.0  # War gained while playing for team post-trade
    totalBattingWar = 0.0  # Player's overall generated war
    totalPostBattingWar = 0.0  # War gained post trade for all teams
    teamPitchingWar = 0.0  # War gained while playing for team post-trade
    totalPitchingWar = 0.0  # Player's overall generated war
    totalPostPitchingWar = 0.0  # War gained post trade for all teams
    temp = 0
    for line in bWar:
        statsID = int(line[0])
        yearStat = int(line[1])
        statsTID = int(line[2])
        stats = float(line[3])
        if (statsTID > 30 and statsTID < 61) or statsTID == 1221 or statsTID == 1222:  # ML team?
            if int(statsID == playerID):  # if the player ID from Statswar is the same as Player ID
                if int(statsTID == teamID):  # if the player played for that team
                    teamBattingWar += stats  # add his war from traded team
                else:
                    totalBattingWar += stats  # player was off the traded team but still contributed in PSD
                temp = 1
            if yearStat >= year: # Post trade overall war calc
                if int(statsID == playerID):
                    totalPostBattingWar += stats
                    temp = 1
        if playerID != int(line[0]) and temp == 1:
            break
    temp = 0
    for stat in pWar:
        statsID = int(stat[0])
        yearStat = int(stat[1])
        statsTID = int(stat[2])
        stats = float(stat[3])
        if (statsTID > 30 and statsTID < 61) or statsTID == 1221 or statsTID == 1222:  # ML team?
            if int(statsID == playerID):  # if the player ID from Statswar is the same as Player ID
                if int(statsTID == teamID):  # if the player played for that team
                    teamPitchingWar += stats  # add his war from traded team
                else:
                    totalPitchingWar += stats  # player was off the traded team but still contributed in PSD
                temp = 1
            if yearStat >= year:  # Post trade overall war calc
                if int(statsID == playerID):
                    temp = 1
                    totalPostPitchingWar += stats
        if playerID != int(stat[0]) and temp == 1:
            break
    totalBWar = teamBattingWar + totalBattingWar
    totalpWar = teamPitchingWar + totalPitchingWar
    if totalpWar > 5 and totalBWar > 5:  # 2 way players
        total = totalpWar + totalBWar
        totalPost = totalPostBattingWar + totalPostBattingWar
        totalTeam = teamPitchingWar + teamBattingWar
        return total, totalPost, totalTeam
    elif totalpWar > totalBWar:
        return totalpWar, totalPostPitchingWar, teamPitchingWar
    elif totalBWar > totalpWar:
        return totalBWar, totalPostBattingWar, teamBattingWar
    else:
        return 0, 0, 0


def main():
    start_time = time.time()
    with open('human_Managers.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        managers = []
        for row in csv_reader:
            managers.append(row)
    with open('trade_history2035.csv') as csv_file1:
        csv_reader1 = csv.reader(csv_file1, delimiter=',')
        trades = []
        for row1 in csv_reader1:
            trades.append(row1)
    with open('teams.csv')as csv_file2:
        csv_reader2 = csv.reader(csv_file2, delimiter=',')
        teams = []
        for row2 in csv_reader2:
            teams.append(row2)
    with open('players_career_batting_stats.csv') as csv_file3:
        csv_reader3 = csv.reader(csv_file3, delimiter=',')
        battingWar = []
        for row3 in csv_reader3:
            battingWar.append(row3)
    with open('players_career_pitching_stats.csv') as csv_file4:
        csv_reader4 = csv.reader(csv_file4, delimiter=',')
        pitchingWar = []
        for row4 in csv_reader4:
            pitchingWar.append(row4)
    with open('players.csv', encoding="utf8") as csv_file5:
        csv_reader5 = csv.reader(csv_file5, delimiter=',')
        players = []
        for row6 in csv_reader5:
            players.append(row6)
    tradesWNames = [[] for i in range(len(trades) + 1)]
    tradesWNames[0].append("Date")
    tradesWNames[0].append("Team 1")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P1")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P2")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P3")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P4")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P5")
    tradesWNames[0].append("Team 2")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P1")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P2")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P3")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P4")
    tradesWNames[0].append("War Sent")
    tradesWNames[0].append("P5")
    tradesWNames[0].append("T1 Lost War(Overall)")
    tradesWNames[0].append("T1 Lost War(Post-trade)")
    tradesWNames[0].append("T1 Lost war(Post-trade team only)")
    tradesWNames[0].append("T2 Lost War(Overall)")
    tradesWNames[0].append("T2 Lost War(Post-trade)")
    tradesWNames[0].append("T2 Lost war(Post-trade team only)")
    tradesWNames[0].append("War Diff(post trade) (+ = T2 wins, - = T1 wins)")
    tradesWNames[0].append("War Diff (overall)")

    counter1 = 1
    year = 0
    for trade in trades:
        aTotalPostTradeWar = 0.0
        atotalTWar = 0.0
        aTotalOvrWar = 0.0
        bTotalPostTradeWar = 0.0
        btotalTWar = 0.0
        bTotalOvrWar = 0.0
        string = trade[0]
        if int(trade[1]) == 37 or int(trade[8]) == 37:
            date = datetime.datetime.strptime(string, "%m/%d/%Y")
            tradesWNames[counter1].append(trade[0])
            # tradesWNames[counter1].append(trade[1])
            name = tNumberToName(trade[1], teams)
            tradesWNames[counter1].append(name)
            for count in range(5):
                temp = count + 2
                aplayerTotalWar = 0.0
                aplayerPostTradeWar = 0.0
                aplayerTeamWar = 0.0
                if int(trade[temp]) == 0:
                    tradesWNames[counter1].append("0")
                    tradesWNames[counter1].append("0")
                else:
                    aplayerTotalWar, aplayerPostTradeWar, aplayerTeamWar = statsWarLookup(int(trade[temp]), int(trade[8]), pitchingWar, battingWar, date.year)
                    # print("Searching values1: ", trade[temp], ' ', trade[1], ', he had ', pTotalWar)
                    tradesWNames[counter1].append(aplayerPostTradeWar)
                    tradesWNames[counter1].append(pNumberToName(trade[temp], players))
                aTotalPostTradeWar += aplayerPostTradeWar
                atotalTWar += aplayerTeamWar
                aTotalOvrWar += aplayerTotalWar
                count += 1
            # tradesWNames[counter1].append(trade[8])
            tradesWNames[counter1].append(tNumberToName(trade[8], teams))
            for counter in range(5):
                bplayerTotalWar = 0.0
                bplayerPostTradeWar = 0.0
                bplayerTeamWar = 0.0
                temp1 = counter + 9
                if int(trade[temp1]) == 0:
                    tradesWNames[counter1].append("0")
                    tradesWNames[counter1].append("0")
                else:
                    bplayerTotalWar, bplayerPostTradeWar, bplayerTeamWar = statsWarLookup(int(trade[temp1]), int(trade[8]), pitchingWar, battingWar, date.year)
                    # print("Searching values1: ", trade[temp1], ' ', trade[8], ', he had ', pTotalWar)
                    tradesWNames[counter1].append(bplayerPostTradeWar)
                    tradesWNames[counter1].append(pNumberToName(trade[temp1], players))
                bTotalPostTradeWar += bplayerPostTradeWar
                btotalTWar += bplayerTeamWar
                bTotalOvrWar += bplayerTotalWar
                counter += 1
            tradesWNames[counter1].append(aTotalOvrWar)
            tradesWNames[counter1].append(aTotalPostTradeWar)
            tradesWNames[counter1].append(atotalTWar)
            tradesWNames[counter1].append(bTotalOvrWar)
            tradesWNames[counter1].append(bTotalPostTradeWar)
            tradesWNames[counter1].append(btotalTWar)
            tradesWNames[counter1].append(aTotalPostTradeWar - bTotalPostTradeWar)
            tradesWNames[counter1].append(aTotalOvrWar - bTotalOvrWar)
            # if btotalTWar != 0 or btotalOffWar != 0:
            #    tradesWNames[counter1].append(btotalTWar / (btotalTWar + btotalOffWar))
            # else:
            #    tradesWNames[counter1].append(0)
            # if atotalTWar != 0 or atotalOffWar !=0:
            #    tradesWNames[counter1].append(atotalTWar / (atotalTWar + atotalOffWar))
            # else:
            #    tradesWNames[counter1].append(0)
            counter1 += 1
            with open("Cincinatti1.1.3", "w+") as my_csv:
                csvWriter = csv.writer(my_csv, delimiter=',')
                csvWriter.writerows(tradesWNames)
        a = 0
    print("--- %s seconds ---" % (time.time() - start_time))


main()
