import tkinter as tk
from tkinter import messagebox, simpledialog
import pygame
from game import Connect4Game
from agents.random_agent import RandomAgent
from agents.smart_agent import SmartAgent
from agents.minimax_agent import MinimaxAgent
from agents.ml_agent import MLAgent
from constants import BLUE, BLACK, YELLOW, RED, WHITE, SQUARE_SIZE, ROW_COUNT, COLUMN_COUNT,WIDTH, HEIGHT




class Connect4:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4 Game")
        self.game = None
        self.current_player = 1
        self.agents = {
            "Random": RandomAgent(player_id=2),
            "Smart": SmartAgent(player_id=2),
            "Minimax": MinimaxAgent(player_id=2),
            "ML": MLAgent(player_id=2)
        }
        self.board_buttons = []
        self.selected_game_mode = None
        self.user_name = None

        # Initialize Pygame mixer for music
        pygame.mixer.init()
        self.music_files = ["track1.mp3", "track2.mp3", "track3.mp3"]  # Example track list
        self.current_track_index = 0
        self.is_playing = False

    def start(self):
        """
        Entry point to start the GUI application.
        """
        self.setup_ui()
        self.root.bind('<p>', self.toggle_music)  # Bind 'P' to play/pause music
        self.root.bind('<s>', self.stop_music)   # Bind 'S' to stop music
        self.root.bind('<Up>', self.prev_track)  # Bind arrow up to move to previous track
        self.root.bind('<Right>', self.next_track)  # Bind right arrow to move to next track
        self.root.mainloop()

    def setup_ui(self):
        """
        Sets up the initial game mode selection UI.
        """
        label = tk.Label(self.root, text="Choose Game Mode:")
        label.pack()

        modes = [
            ("Human vs Random Agent", "Random"),
            ("Human vs Smart Agent", "Smart"),
            ("Human vs Minimax Agent", "Minimax"),
            ("Human vs ML Agent", "ML"),
            ("AI vs AI (Random vs Smart)", "AI-Random-Smart"),
            ("AI vs AI (Minimax vs ML)", "AI-Minimax-ML")
        ]

        for text, mode in modes:
            tk.Button(self.root, text=text, width=30, command=lambda m=mode: self.select_game_mode(m)).pack(pady=2)

    def select_game_mode(self, mode):
        self.selected_game_mode = mode
        self.game = Connect4Game()
        self.clear_window()

        if "AI" not in mode:
            self.user_name = simpledialog.askstring("User Registration", "Enter your name:")
            if not self.user_name:
                self.root.destroy()
                return
            self.display_board()
        else:
            self.display_board()
            self.run_ai_vs_ai()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def display_board(self):
        self.board_buttons = []
        for row in range(6):
            row_buttons = []
            for col in range(7):
                btn = tk.Button(self.root, text=" ", width=6, height=3, bg="white",
                                command=lambda c=col: self.make_move(c))
                btn.grid(row=row, column=col)
                row_buttons.append(btn)
            self.board_buttons.append(row_buttons)
        if "AI" not in self.selected_game_mode:
            self.status_label = tk.Label(self.root, text=f"{self.user_name}'s Turn (X)")
            self.status_label.grid(row=6, columnspan=7)

    def make_move(self, col):
        if not self.game.is_valid_move(col):
            return

        self.game.make_move(col)
        self.update_board()

        if self.game.is_game_over():
            self.show_winner()
        else:
            self.current_player = 3 - self.current_player
            self.status_label.config(text="AI's Turn (O)")
            self.root.after(500, self.ai_turn)

    def ai_turn(self):
        if self.selected_game_mode not in self.agents:
            return

        agent = self.agents[self.selected_game_mode]
        move = agent.get_move(self.game)
        self.game.make_move(move)
        self.update_board()

        if self.game.is_game_over():
            self.show_winner()
        else:
            self.current_player = 3 - self.current_player
            self.status_label.config(text=f"{self.user_name}'s Turn (X)")

    def update_board(self):
        for r in range(6):
            for c in range(7):
                cell = self.game.board[r][c]
                btn = self.board_buttons[r][c]
                if cell == 1:
                    btn.config(text="X", bg="red")
                elif cell == 2:
                    btn.config(text="O", bg="yellow")
                else:
                    btn.config(text=" ", bg="white")

    def run_ai_vs_ai(self):
        if self.selected_game_mode == "AI-Random-Smart":
            agent1 = self.agents["Random"]
            agent2 = self.agents["Smart"]
        else:
            agent1 = self.agents["Minimax"]
            agent2 = self.agents["ML"]

        def next_turn():
            if self.game.is_game_over():
                self.show_winner()
                return

            agent = agent1 if self.current_player == 1 else agent2
            move = agent.get_move(self.game)
            self.game.make_move(move)
            self.update_board()
            self.current_player = 3 - self.current_player
            self.root.after(500, next_turn)

        next_turn()

    def show_winner(self):
        winner = self.game.get_winner()
        if winner == 1:
            message = f"{self.user_name} wins!" if "AI" not in self.selected_game_mode else "Player 1 (X) wins!"
        elif winner == 2:
            message = "AI wins!" if "AI" not in self.selected_game_mode else "Player 2 (O) wins!"
        else:
            message = "It's a draw!"
        messagebox.showinfo("Game Over", message)
        self.root.quit()

    # Music Control Methods
    def toggle_music(self, event):
        """Toggle music play/pause."""
        if self.is_playing:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.load(self.music_files[self.current_track_index])
            pygame.mixer.music.play(loops=0, start=0.0)
        self.is_playing = not self.is_playing

    def stop_music(self, event):
        """Stop the music."""
        pygame.mixer.music.stop()
        self.is_playing = False

    def prev_track(self, event):
        """Move to the previous track."""
        self.current_track_index = (self.current_track_index - 1) % len(self.music_files)
        if self.is_playing:
            pygame.mixer.music.load(self.music_files[self.current_track_index])
            pygame.mixer.music.play(loops=0, start=0.0)

    def next_track(self, event):
        """Move to the next track."""
        self.current_track_index = (self.current_track_index + 1) % len(self.music_files)
        if self.is_playing:
            pygame.mixer.music.load(self.music_files[self.current_track_index])
            pygame.mixer.music.play(loops=0, start=0.0)
