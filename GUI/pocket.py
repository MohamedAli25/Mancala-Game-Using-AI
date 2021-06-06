class Pocket():
    def __init__(self, name, txt_area, boundry, font, init_value = 4):
        self.__value = init_value
        self.__text_area = txt_area
        self.__boundry = boundry
        self.__name = name
        self.__font = font
        self.__last_value = -1

    @property
    def last_value(self) -> int:
        return self.__last_value

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def boundry(self) -> list:
        return self.__boundry
    
    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, new_val) -> None:
        self.__last_value = self.__value
        self.__value = new_val
        
    def render(self, screen):
        val = str(self.value)
        if len(val) == 1: val = "0" + val
        area =  self.__font.render(val, False, (255, 255, 255))
        screen.blit(area, self.__text_area)

