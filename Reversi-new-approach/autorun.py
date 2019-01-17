import run

a = "MinMax(self,1,depth_of_search=5)"
b = "MonteCarlo(self,2,iter_max=10)"
c = 4, 4

game = run.Game()
for i in c:
    game.game_start(a, b, i)

