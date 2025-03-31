import turtle
import numpy as np
import matplotlib.pyplot as plt


class Gomoku:
    def __init__(self):
        self.board_size=15
        self.board=np.zeros((self.board_size,self.board_size),dtype=int)
        self.current_player=1

    def draw_board(self):
        turtle.setup(600,600)
        turtle.speed(0)
        turtle.hideturtle()
        turtle.tracer(0)
        for i in range(self.board_size):
            turtle.penup()
            turtle.goto(-280,280-i*40)
            turtle.pendown()
            turtle.goto(280,280-i*40)
            turtle.penup()
            turtle.goto(-280+i*40,280)
            turtle.pendown()
            turtle.goto(-280+i*40,-280)
        turtle.update()

    def draw_piece(self,x,y,player):
        turtle.penup()
        turtle.goto(-280+x*40,280-y*40)
        if player==1:
            turtle.dot(30,"black")  # 黑子
        else:
            turtle.dot(32,"black")  # 黑色边框
            turtle.dot(30,"white")  # 白子

    def check_winner(self,x,y):
        directions=[(1,0),(0,1),(1,1),(1,-1)]
        for dx,dy in directions:
            count=1
            for step in range(1,5):
                nx,ny=x+step*dx,y+step*dy
                if 0<=nx<self.board_size and 0<=ny<self.board_size and self.board[ny][nx]==self.current_player:
                    count+=1
                else:
                    break
            for step in range(1,5):
                nx,ny=x-step*dx,y-step*dy
                if 0<=nx<self.board_size and 0<=ny<self.board_size and self.board[ny][nx]==self.current_player:
                    count+=1
                else:
                    break
            if count>=5:
                return True
        return False

    def click_handler(self,x,y):
        col=round((x+280)/40)
        row=round((280-y)/40)
        if 0<=col<self.board_size and 0<=row<self.board_size and self.board[row][col]==0:
            self.board[row][col]=self.current_player
            self.draw_piece(col,row,self.current_player)
            if self.check_winner(col,row):
                print(f"Player {self.current_player} wins!")
                turtle.done()
            self.current_player=3-self.current_player

    def play(self):
        self.draw_board()
        turtle.onscreenclick(self.click_handler)
        turtle.done()


if __name__=="__main__":
    game=Gomoku()
    game.play()