piece_representation = {"B":"\u2659", "BR":"\u2656", "BN":"\u2658", "BB":"\u2657",
                        "BQ":"\u2655", "BK":"\u2654", "W":"\u265F", "WR":"\u265C",
                        "WN":"\u265E", "WB":"\u265D", "WQ":"\u265B", "WK":"\u265A"}

#♕ #wq-\u265B
#W \u265F

def get_square_location_from_coordinates(notation:str):
    letter = notation[0]
    number = int(notation[1])
    letter_dict = {"a":0, "b":1,"c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    square_location = letter_dict[letter] + (number-1) * 8
    return square_location

