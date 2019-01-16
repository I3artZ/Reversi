import run

a = "MinMax(self,1,depth_of_search=2)"
b = "MonteCarlo(self,2,iter_max=100)"
c = 4, 6

game = run.Game()
for i in c:
    game.game_start(a, b, i)

