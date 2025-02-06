from vision_boards import east_ray_empty, west_ray_empty, north_ray_empty, south_ray_empty, north_east_ray_empty, north_west_ray_empty, south_east_ray_empty, south_west_ray_empty

def rook_vision_board_empty(self, square_notation):
    vision_board = np.uint64(west_ray_empty(self, square_notation)[0] |
                            east_ray_empty(self, square_notation)[0] |
                            north_ray_empty_ray_empty(self, square_notation)[0] | 
                            south_ray_empty(self, square_notation)[0] | )
    return vision_board

def bishop_vision_board_empty(self,square_notation):
    vision_board = np.uint64(north_west_ray_empty(self, square_notation)[0] |
                            north_east_ray_empty(self, square_notation)[0] |
                            south_west_ray_empty_ray_empty(self, square_notation)[0] | 
                            south_east_ray_empty(self, square_notation)[0] | )
    return vision_board

def queen_vision_board_empty(self, square_notation):
    pass