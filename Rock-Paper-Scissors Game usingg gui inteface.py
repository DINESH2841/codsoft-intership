import tkinter as tk
import random

CHOICES = ['Rock', 'Paper', 'Scissors',]
HAND_EMOJI = {'Rock': '✊', 'Paper': '✋', 'Scissors': '✌️'}

def determine_winner(user, computer):
    if user == computer:
        return "It's a Tie!"
    elif (user == 'Rock' and computer == 'Scissors') or \
         (user == 'Paper' and computer == 'Rock') or \
         (user == 'Scissors' and computer == 'Paper'):
        return "You Win!"
    else:
        return "You Lose!"

class RPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Game")
        self.user_score = 0
        self.computer_score = 0
        self.round = 1

        self.label = tk.Label(root, text="Choose Rock, Paper, or Scissors:", font=("Arial", 14))
        self.label.pack(pady=10)

        # Hand signal frames
        self.hands_frame = tk.Frame(root)
        self.hands_frame.pack(pady=5)
        self.user_hand_label = tk.Label(self.hands_frame, text="❔", font=("Arial", 40))
        self.user_hand_label.pack(side=tk.LEFT, padx=40)
        self.vs_label = tk.Label(self.hands_frame, text="VS", font=("Arial", 18))
        self.vs_label.pack(side=tk.LEFT)
        self.computer_hand_label = tk.Label(self.hands_frame, text="❔", font=("Arial", 40))
        self.computer_hand_label.pack(side=tk.LEFT, padx=40)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()
        self.buttons = []
        for choice in CHOICES:
            btn = tk.Button(self.button_frame, text=choice, width=10, font=("Arial", 12),
                            command=lambda c=choice: self.play_round(c))
            btn.pack(side=tk.LEFT, padx=5)
            self.buttons.append(btn)

        self.result_label = tk.Label(root, text="", font=("Arial", 12))
        self.result_label.pack(pady=10)

        self.score_label = tk.Label(root, text=self.get_score_text(), font=("Arial", 12))
        self.score_label.pack(pady=5)

        self.exit_btn = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit)
        self.exit_btn.pack(pady=5)

        self.animation_running = False
        self.animation_count = 0
        self.animation_max = 15
        self.user_choice = None
        self.computer_choice = None

    def get_score_text(self):
        return f"Round: {self.round}   Your Score: {self.user_score}   Computer Score: {self.computer_score}"

    def play_round(self, user_choice):
        self.user_choice = user_choice
        self.disable_buttons()
        self.result_label.config(text="Computer is choosing...")
        self.user_hand_label.config(text=HAND_EMOJI.get(user_choice, "❔"))
        self.computer_hand_label.config(text="❔")
        self.animation_running = True
        self.animation_count = 0
        self.animate_computer_choice()

    def animate_computer_choice(self):
        if self.animation_count < self.animation_max:
            # Animate both hands
            user_anim = HAND_EMOJI[self.user_choice]
            computer_anim = HAND_EMOJI[random.choice(CHOICES)]
            self.user_hand_label.config(text=user_anim)
            self.computer_hand_label.config(text=computer_anim)
            self.result_label.config(text=f"Computer is choosing...\n{computer_anim}")
            self.animation_count += 1
            self.root.after(70, self.animate_computer_choice)
        else:
            self.animation_running = False
            self.computer_choice = random.choice(CHOICES)
            result = determine_winner(self.user_choice, self.computer_choice)
            if result == "You Win!":
                self.user_score += 1
            elif result == "You Lose!":
                self.computer_score += 1

            self.computer_hand_label.config(text=HAND_EMOJI[self.computer_choice])
            self.result_label.config(
                text=f"You chose: {self.user_choice} {HAND_EMOJI[self.user_choice]}\n"
                     f"Computer chose: {self.computer_choice} {HAND_EMOJI[self.computer_choice]}\n{result}"
            )
            self.score_label.config(text=self.get_score_text())
            # Start next round automatically after 5 seconds
            self.root.after(5000, self.reset_round)

    def reset_round(self):
        self.round += 1
        self.result_label.config(text="")
        self.score_label.config(text=self.get_score_text())
        self.user_hand_label.config(text="❔")
        self.computer_hand_label.config(text="❔")
        self.enable_buttons()

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

    def enable_buttons(self):
        for btn in self.buttons:
            btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGame(root)
    root.mainloop()