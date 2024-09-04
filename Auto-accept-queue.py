from lcu_driver import Connector
connector = Connector()
import os
import time

@connector.ready
async def connect(connection):
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    print('Welcome ' + (await summoner.json())['displayName'])
    checkF = 0
    checkQ = 0
    while True:
        gamephase = await connection.request('get', '/lol-gameflow/v1/gameflow-phase')
        currentphase = await gamephase.json()
        if currentphase == 'Lobby':
            checkF = 0
            checkQ = 0
        if currentphase == 'ReadyCheck':
            checkQ=0
            await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
            if checkF==0:
                print('Partita trovata!')
                checkF=1
        if currentphase == 'ChampSelect':
            print('\n')
            for i in range(5):
                try:
                    playernumber = i + 1
                    infosummoners = await connection.request('get', '/lol-champ-select/v1/summoners/' + str(i))
                    summonersid = (await infosummoners.json())['summonerId']
                    sums = await connection.request('get', '/lol-summoner/v1/summoners/' + str(summonersid))
                    displayname = (await sums.json())['displayName']
                    puuid = (await sums.json())['puuid']
                    rankstats = await connection.request('get', '/lol-ranked/v1/ranked-stats/' + puuid)
                    queues = (await rankstats.json())['queues'][0]
                    tier = queues['tier']
                    division = queues['division']

                    if division == 'NA':
                        print(displayname," ","UNRANKED")
                    else:
                        print(displayname,tier,division)

                except:
                    print('Player ' + str(playernumber)+" No Data")

            print("\n")
            os.system('pause')
            break

        if currentphase == 'Matchmaking':
            checkF=0
            if checkQ==0:
                print("in queue...")
                checkQ=1

        time.sleep(2)

@connector.close
async def disconnect(connection):
    print('Finished task')


connector.start()
