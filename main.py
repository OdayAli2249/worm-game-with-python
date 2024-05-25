import tkinter as tk
import random

class WormGame:
    def __init__(self, master):
        self.master = master
        master.title("Worm Game")

        self.canvas = tk.Canvas(master, width=400, height=400, bg="black")
        self.canvas.pack()

        self.score = 0
        self.delay = 150
        self.segments = [(200, 200)]
        self.food = self.create_food()
        self.direction = "Right"
        self.game_over = False

        self.canvas.bind("<KeyPress>", self.change_direction)
        self.canvas.focus_set()

        self.draw_worm()
        self.draw_food()

        self.update()

    def draw_worm(self):
        for segment in self.segments:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + 10, y + 10, fill="green")

    def draw_food(self):
        x, y = self.food
        self.canvas.create_oval(x, y, x + 10, y + 10, fill="red")

    def create_food(self):
        while True:
            x = random.randrange(0, 400, 10)
            y = random.randrange(0, 400, 10)
            if (x, y) not in self.segments:
                return x, y

    def move(self):
        head_x, head_y = self.segments[0]
        if self.direction == "Right":
            new_head = (head_x + 10, head_y)
        elif self.direction == "Left":
            new_head = (head_x - 10, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - 10)
        elif self.direction == "Down":
            new_head = (head_x, head_y + 10)

        self.segments = [new_head] + self.segments[:-1]

    def check_collision(self):
        head = self.segments[0]
        if head in self.segments[1:] or head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 400:
            self.game_over = True

    def check_food(self):
        if self.segments[0] == self.food:
            self.score += 1
            self.segments.append(self.segments[-1])
            self.food = self.create_food()

    def change_direction(self, event):
        key = event.keysym
        if (key == "Up" and self.direction != "Down") or \
           (key == "Down" and self.direction != "Up") or \
           (key == "Left" and self.direction != "Right") or \
           (key == "Right" and self.direction != "Left"):
            self.direction = key

    def update(self):
        if not self.game_over:
            self.move()
            self.check_collision()
            self.check_food()
            self.canvas.delete("all")
            self.draw_worm()
            self.draw_food()
            self.canvas.create_text(20, 10, anchor="nw", text="Score: {}".format(self.score), fill="white")
            self.master.after(self.delay, self.update)
        else:
            self.canvas.create_text(200, 200, text="Game Over!", fill="white", font=("Helvetica", 24, "bold"))

def main():
    root = tk.Tk()
    app = WormGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()