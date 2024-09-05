from app import get_piece_asset_path, get_board_asset_path


def test_get_piece_asset_path():
    path = get_piece_asset_path('Black', 'Pawn')
    assert path == "C:\\Users\\Jared\\Documents\\Projects\\python\\chess\\app\\gui\\assets\\16x32 pieces\\B_Pawn.png"


def test_get_board_asset_path():
    path = get_board_asset_path()
    assert path == "C:\\Users\\Jared\\Documents\\Projects\\python\\chess\\app\\gui\\assets\\boards\\board_plain_01.png"
