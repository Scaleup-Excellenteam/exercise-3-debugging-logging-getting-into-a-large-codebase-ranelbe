from unittest import TestCase
from unittest.mock import Mock
from Piece import Knight, Pawn, Rook, Queen
from enums import Player
from enums import GameStatus
import chess_engine
import ai_engine


class TestChess(TestCase):

    # ========================= Helper functions ===========================

    def empty_board(self):
        """ set up an empty board """
        game_state = chess_engine.game_state()
        game_state.board = [[Player.EMPTY for _ in range(8)] for _ in range(8)]
        return game_state

    # ========================= Unit tests ================================

    def test_get_valid_piece_takes_knight_row_2_col_4_with_enemies(self):
        game_state = chess_engine.game_state()
        black_knight = Knight('n', 2, 4, Player.PLAYER_2)
        game_state.board[2][4] = black_knight
        moves = black_knight.get_valid_piece_takes(game_state)
        valid_piece_takes = [(0, 3), (0, 5), (1, 2), (1, 6)]
        self.assertListEqual(moves, valid_piece_takes)

    def test_get_valid_piece_takes_knight_row_5_col_4_with_allies(self):
        game_state = chess_engine.game_state()
        black_knight = Knight('n', 5, 4, Player.PLAYER_2)
        game_state.board[5][4] = black_knight
        moves = black_knight.get_valid_piece_takes(game_state)
        self.assertEqual(len(moves), 0)  # no valid take moves

    def test_get_valid_piece_takes_knight_row_0_col_0_with_ally_and_enemy(self):
        game_state = self.empty_board()
        white_knight = Knight('n', 0, 0, Player.PLAYER_1)
        game_state.board[0][0] = white_knight
        game_state.board[1][2] = Queen('q', 1, 2, Player.PLAYER_1)  # ally
        game_state.board[2][1] = Rook('r', 2, 1, Player.PLAYER_2)  # enemy
        moves = white_knight.get_valid_piece_takes(game_state)
        valid_piece_takes = [(2, 1)]
        self.assertListEqual(moves, valid_piece_takes)

    def test_get_valid_peaceful_moves_knight_row_3_col_4(self):
        game_state = self.empty_board()
        white_knight = Knight('n', 3, 4, Player.PLAYER_1)
        game_state.board[3][4] = white_knight
        moves = white_knight.get_valid_peaceful_moves(game_state)
        valid_peaceful_moves = [(1, 3), (1, 5), (2, 2), (2, 6),
                                (4, 2), (4, 6), (5, 5), (5, 3)]
        self.assertListEqual(moves, valid_peaceful_moves)

    def test_get_valid_peaceful_moves_knight_row_0_col_0(self):
        game_state = self.empty_board()
        black_knight = Knight('n', 0, 0, Player.PLAYER_2)
        game_state.board[0][0] = black_knight
        moves = black_knight.get_valid_peaceful_moves(game_state)
        valid_peaceful_moves = [(1, 2), (2, 1)]
        self.assertListEqual(moves, valid_peaceful_moves)

    def test_get_valid_peaceful_moves_knight_row_0_col_5_some_dest_not_empty(self):
        game_state = self.empty_board()
        white_knight = Knight('n', 0, 5, Player.PLAYER_1)
        game_state.board[0][5] = white_knight
        # add some pieces on some valid move destinations
        game_state.board[2][4] = Knight('n', 2, 4, Player.PLAYER_1)
        game_state.board[1][7] = Queen('q', 1, 7, Player.PLAYER_2)
        moves = white_knight.get_valid_peaceful_moves(game_state)
        valid_peaceful_moves = [(1, 3), (2, 6)]
        self.assertListEqual(moves, valid_peaceful_moves)

    # ========================= Integration tests ==========================

    def test_get_valid_piece_moves_row_3_col_4(self):
        """ test the get_valid_peaceful_moves and
        get_valid_piece_takes functions together"""
        game_state = chess_engine.game_state()
        white_knight = Knight('n', 5, 4, Player.PLAYER_1)
        game_state.board[5][4] = white_knight
        # add some allies
        game_state.board[3][3] = Rook('r', 3, 3, Player.PLAYER_1)
        game_state.board[6][2] = Pawn('p', 6, 2, Player.PLAYER_1)
        game_state.board[6][6] = Pawn('p', 6, 6, Player.PLAYER_1)
        moves = white_knight.get_valid_piece_moves(game_state)
        valid_piece_moves = [(3, 5), (4, 2), (4, 6), (7, 5), (7, 3)]
        self.assertListEqual(moves, valid_piece_moves)

    def test_evaluate_board(self):
        """ test the evaluate_board function that uses
        get_piece_value function to evaluate the board score """
        game_state = chess_engine.game_state()
        ai = ai_engine.chess_ai()
        game_state.board[0][0] = Player.EMPTY  # +50
        game_state.board[0][3] = Player.EMPTY  # +1000
        game_state.board[6][0] = Player.EMPTY  # -10
        game_state.board[7][2] = Player.EMPTY  # -30
        evaluate_board = ai.evaluate_board(game_state, Player.PLAYER_1)
        self.assertEqual(evaluate_board, 1010)

    # ========================= system tests ===============================

    def test_fools_mate_black_win(self):
        """ test the quickest way to win a game by executing "fools checkmate".
        this test is for complete game played by two players."""
        game_state = chess_engine.game_state()
        game_state.move_piece((1, 2), (2, 2), False)
        game_state.move_piece((6, 3), (5, 3), False)
        game_state.move_piece((1, 1), (3, 1), False)
        game_state.move_piece((7, 4), (3, 0), False)
        # black player wins
        self.assertEqual(game_state.checkmate_stalemate_checker(), GameStatus.BLACK_WIN)
