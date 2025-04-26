import os
import numpy as np
import pandas as pd
from typing import List
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import random
from agents.minimax_agent import MinimaxAgent
from utils.game_state import GameState
from utils.dataset_loader import DatasetLoader  # <-- Import properly

class MLAgent:
    def __init__(self, player_id: int, model_path: str = "models/ml_agent_model.pkl",
                 data_path: str = "connect4_dataset/connect-4.data.csv",
                 names_path: str = "connect4_dataset/connect-4.names.txt") -> None:
        self.player_id = player_id
        self.model_path = model_path
        self.data_path = data_path
        self.names_path = names_path
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        self.model = self._load_or_train_model()

    def _load_or_train_model(self):
        if os.path.exists(self.model_path):
            print("✅ Loading trained model from:", self.model_path)
            loaded_data = joblib.load(self.model_path)
            self.label_encoder = loaded_data["label_encoder"]
            self.feature_names = loaded_data["feature_names"]
            return loaded_data["model"]
        else:
            print("✅ Training new model...")
            return self._train_model()

    def _train_model(self) -> RandomForestClassifier:
        print("Training MLAgent model...")

        loader = DatasetLoader(os.path.dirname(self.data_path))

        csv_data = loader.load_csv('connect-4.data.csv')
        if not csv_data:
            print("[MLAgent] ERROR: Could not load CSV data.")
            return None

        attributes = loader.load_attribute_names('connect-4.names.txt')
        if not attributes:
            print("[MLAgent] ERROR: Could not load attributes.")
            return None

        self.feature_names = attributes

        df = pd.DataFrame(csv_data, columns=attributes)

        mapping = {'x': 1, 'o': 2, 'b': 0}

        for col in df.columns[:-1]:  
            df[col] = df[col].map(mapping).fillna(0).astype(int)


        df["Class"] = self.label_encoder.fit_transform(df["Class"])

        X = df.drop("Class", axis=1).astype(float) / 2.0
        y = df["Class"]

        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
        except ValueError:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=40,
            min_samples_split=3,
            min_samples_leaf=1,
            max_features='sqrt',
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        # ✅ Training accuracy
        train_accuracy = model.score(X_train, y_train)
        print(f"✅ Training Accuracy: {train_accuracy * 100:.2f}%")

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        joblib.dump({
            "model": model,
            "label_encoder": self.label_encoder,
            "feature_names": self.feature_names
        }, self.model_path)
        print("✅ Model trained and saved successfully.")
        return model

    def _outcome_score(self, outcome_label: str) -> float:
        mapping = {'win': 1.0, 'draw': 0.5, 'loss': 0.0}
        return mapping.get(outcome_label, 0.25)

    def _encode_board(self, board: np.ndarray) -> List[float]:
        flat = board.flatten()
        return (flat.astype(float) / 2.0).tolist()

    def get_move(self, board_or_game) -> int:
        if hasattr(board_or_game, 'get_board_copy'):
            board = board_or_game.get_board_copy()
        else:
            board = board_or_game

        valid_moves = [c for c in range(board.shape[1]) if board[0][c] == 0]

        if self.model is None:
            print("[MLAgent] No model loaded. Falling back to MinimaxAgent.")
            fallback = MinimaxAgent(player_id=self.player_id)
            return fallback.get_move(GameState(board.copy(), self.player_id))

        best_move = None
        best_score = -np.inf

        for col in valid_moves:
            temp_board = board.copy()
            for row in reversed(range(temp_board.shape[0])):
                if temp_board[row][col] == 0:
                    temp_board[row][col] = self.player_id
                    break

            encoded_board = self._encode_board(temp_board)
            input_df = pd.DataFrame([encoded_board], columns=self.feature_names[:-1])


            proba = self.model.predict_proba(input_df)[0]
            predicted_label = self.model.predict(input_df)[0]
            predicted_outcome = self.label_encoder.inverse_transform([predicted_label])[0]
            confidence = max(proba)
            score = self._outcome_score(predicted_outcome) * confidence

            if score > best_score:
                best_score = score
                best_move = col

        return best_move if best_move is not None else random.choice(valid_moves)

    def __str__(self):
        return f"MLAgent (Player {self.player_id})"
