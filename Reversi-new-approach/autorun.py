import run

a = "MinMax(self,1,depth_of_search=5)"
b = "MonteCarlo(self,2,iter_max=10)"

players_1 = []
players_2 = []
iter_max = [i*100 for i in range(11)]
depth_of_search = [i for i in range(11)]
print(iter_max, depth_of_search)

for a in iter_max:
    players_1.append("MonteCarlo(self,1,iter_max="+str(a)+")")
    players_2.append("MonteCarlo(self,2,iter_max="+str(a)+")")

for i in depth_of_search:
    players_1.append("MinMax(self,1,depth_of_search="+str(i)+")")
    players_2.append("MinMax(self,2,depth_of_search="+str(i)+")")

board_size = 4, 6, 8
number_of_plays = 10
play_number = 0

plays = []
#game = run.Game()
while play_number < number_of_plays:
    play_number += 1
    for size in board_size:
        for player_1 in players_1:
            for player_2 in players_2:
                plays.append((player_1, player_2, size))
                #game.game_start(player_1, player_2, size)

print(len(plays))