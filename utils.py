def game_over(self):
    self.game_over = True
    self.points = []
    self.distances = []  # distance between each point
    self.currlength = 0  # total lenght of snake
    self.allowedlength = 150
    self.prepoint = 0, 0  # previous point
    if self.score > self.maxscore:
        self.maxscore = self.score


def length_reduction(self):
    if self.currlength > self.allowedlength:
        for i, dis in enumerate(self.distances):
            self.currlength -= self.distances[i]
            self.distances.pop(i)
            self.points.pop(i)
            if self.currlength <= self.allowedlength:
                break
