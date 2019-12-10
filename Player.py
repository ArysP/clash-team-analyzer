import time

class Player():

    def setSummonerInfo(self, sinfo):
        self.summonerInfo = sinfo

    def setMasteryInfo(self, minfo):
        self.masteryInfo = minfo
    
    def setMatchlist(self, mlist):
        self.matchlist = mlist
        self.unanalyzedMatches = []
        self.analyzedMatches = []
        for i in range(0, 20):
            self.unanalyzedMatches.append(mlist["matches"][i]["gameId"])
    
    def setMatchInfo(self, matchId, mInfo):
        self.unanalyzedMatches.remove(matchId)
        self.analyzedMatches.append(mInfo)
    
    def setLeagueInfo(self, linfo):
        self.leagueInfo = linfo
    
    def setTeamMates(self, p1, p2, p3, p4):
        self.teammates = [p1, p2, p3, p4]

    def getEncryptedSummonerId(self):
        return self.summonerInfo["id"]
    
    def getSummonerName(self):
        return self.summonerInfo["name"]
    
    def getSummonerLevel(self):
        return self.summonerInfo["summonerLevel"]

    def getTop5Mastery(self):
        return [self.masteryInfo[0], self.masteryInfo[1], self.masteryInfo[2], self.masteryInfo[3], self.masteryInfo[4]]
    
    def getMastery(self):
        return self.masteryInfo
    
    def getEncryptedAccountId(self):
        return self.summonerInfo["accountId"]
    
    def getToplanePercent(self):
        topmatches = 0
        for match in self.matchlist["matches"]:
            if match["lane"] == "TOP":
                topmatches += 1
        return (topmatches / self.matchlist["matches"].__len__()) * 100
    
    def getMidlanePercent(self):
        topmatches = 0
        for match in self.matchlist["matches"]:
            if match["lane"] == "MID":
                topmatches += 1
        return (topmatches / self.matchlist["matches"].__len__()) * 100
        
    def getAdcPercent(self):
        topmatches = 0
        for match in self.matchlist["matches"]:
            if match["lane"] == "BOTTOM" and match["role"] == "DUO_CARRY":
                topmatches += 1
        return (topmatches / self.matchlist["matches"].__len__()) * 100
    
    def getSupportPercent(self):
        topmatches = 0
        for match in self.matchlist["matches"]:
            if match["lane"] == "BOTTOM" and match["role"] == "DUO_SUPPORT":
                topmatches += 1
        return (topmatches / self.matchlist["matches"].__len__()) * 100
    
    def getJunglePercent(self):
        topmatches = 0
        for match in self.matchlist["matches"]:
            if match["lane"] == "JUNGLE":
                topmatches += 1
        return (topmatches / self.matchlist["matches"].__len__()) * 100
    
    def getAnalyzedMatches(self):
        return self.analyzedMatches.__len__()

    def getMaxMatches(self):
        return self.analyzedMatches.__len__() + self.unanalyzedMatches.__len__()

    def getMostPlayedChampions(self):
        champs = {}
        for match in self.matchlist["matches"]:
            if match["champion"] in champs:
                champs[match["champion"]] += 1
            else:
                champs[match["champion"]] = 1
        return champs
    
    def getMatchToAnalyze(self):
        if self.unanalyzedMatches.__len__() > 0:
            return self.unanalyzedMatches[0]
        else:
            return -1
    
    def getAvgKDA(self):
        pID = 0
        kills = 0
        deaths = 0
        assists = 0

        if self.analyzedMatches.__len__() == 0:
            return 0, 0, 0

        for match in self.analyzedMatches:
            for participantIdentitiy in match["participantIdentities"]:
                if participantIdentitiy["player"]["summonerName"] == self.summonerInfo["name"]:
                    pID = participantIdentitiy["participantId"]
            for stats in match["participants"]:
                if stats["participantId"] == pID:
                    kills += stats["stats"]["kills"]
                    deaths += stats["stats"]["deaths"]
                    assists += stats["stats"]["assists"]
        
        kills = kills/self.getAnalyzedMatches()
        deaths = deaths/self.getAnalyzedMatches()
        assists = assists/self.getAnalyzedMatches()

        return kills, deaths, assists
    
    def getWinRate(self):
        pID = 0
        wins = 0

        if self.getAnalyzedMatches() == 0:
            return 0

        for match in self.analyzedMatches:
            for participantIdentitiy in match["participantIdentities"]:
                if participantIdentitiy["player"]["summonerName"] == self.summonerInfo["name"]:
                    pID = participantIdentitiy["participantId"]
            for stats in match["participants"]:
                if stats["participantId"] == pID:
                    if stats["stats"]["win"]:
                        wins += 1
        
        wins = wins/self.getAnalyzedMatches()

        return wins*100
    
    def getSoloDuoRank(self):
        for queue in self.leagueInfo:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                return queue["tier"] + " " + queue["rank"], queue["leaguePoints"]
        return "UNRANKED", 0
    
    def getFlexRank(self):
        for queue in self.leagueInfo:
            if queue["queueType"] == "RANKED_FLEX_SR":
                return queue["tier"] + " " + queue["rank"], queue["leaguePoints"]
        return "UNRANKED", 0
    
    def getSoloDuoWR(self):
        for queue in self.leagueInfo:
            if queue["queueType"] == "RANKED_SOLO_5x5":
                wr = queue["wins"]/(queue["wins"]+queue["losses"])
                return round(wr*100, 1)
        return 0
    
    def getFlexWR(self):
        for queue in self.leagueInfo:
            if queue["queueType"] == "RANKED_FLEX_SR":
                wr = queue["wins"]/(queue["wins"]+queue["losses"])
                return round(wr*100, 1)
        return 0