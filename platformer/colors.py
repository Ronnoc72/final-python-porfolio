# colors for pygame in rgb

class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = GREY = (200, 200, 200)
    LIGHT_GRAY = LIGHT_GREY = (100, 100, 100)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)
    ORANGE = (255, 165, 0)
    BROWN = (210, 105, 30)
    CORNFLOWER_BLUE = (100, 149, 237)
    DARK_GREEN = (71, 122, 75)
    DARK_PURPLE = (34, 39, 122)
    PINK = (255, 192, 203)
    SANDY_BROWN = (244, 164, 96)
    LIGHT_BLUE = (173, 216, 230)
    color_arr = [WHITE, BLACK, GRAY, RED, GREEN, BLUE, YELLOW, PURPLE, CYAN, ORANGE,
                 BROWN, CORNFLOWER_BLUE, DARK_PURPLE, DARK_GREEN, PINK, SANDY_BROWN, LIGHT_BLUE]

    @staticmethod
    def random_color(old_color):
        import random
        temp = Colors.color_arr.copy()
        if old_color in temp:
            temp.remove(old_color)
        else:
            print("--Not a valid color in the color array--")
        choice = random.choice(temp)
        return choice


if __name__ == "__main__":
    print(__file__+" is meant to be imported.")