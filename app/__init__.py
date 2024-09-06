import os


def get_board_asset_path():
    """
    Gets asset for board
    :return:
    """
    # Get the absolute path to the directory containing main.py
    base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "gui", "assets", "boards", "board_plain_01.png")


def get_piece_asset_path(colour: str, piece: str):
    """
    Grabs png asset for given piece.
    :param colour: (str) Colour of piece (WHITE or BLACK)
    :param piece: (str) Name of piece
    :return: path to piece png
    """
    # Get the absolute path to the directory containing main.py
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Create filename of piece
    colour_initial = colour.value[0]
    filename = colour_initial + '_' + piece + '.png'

    # Construct the full path to the asset file in the gui/assets directory
    return os.path.join(base_path, 'gui', 'assets', '16x32 pieces', filename)


if __name__ == '__main__':
    path = get_piece_asset_path('BLACK', 'Pawn')
    print(path)
