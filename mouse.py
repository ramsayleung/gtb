

def sayHello():
    print(mouse.get_position(),'sayHello')
if __name__ == '__main__':

    mouse.on_double_click(sayHello)  # lambda: print(11111111111) callback, args=()

    mouse.wait(button='left', target_types=('double',))
