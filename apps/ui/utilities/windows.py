from ..core import driver
from ..utilities.elements import explicit_wait


def switch_to_window_by_index(index):
    explicit_wait(3)
    if index < len(driver.instance.window_handles):
        new_window = driver.instance.window_handles[index]
        driver.instance.switch_to.window(new_window)
    else:
        print(f"No window exists at index {index}")


def close_window_by_index(index):
    explicit_wait(3)
    if index < len(driver.instance.window_handles):
        window_to_close = driver.instance.window_handles[index]
        driver.instance.switch_to.window(window_to_close)
        driver.instance.close()
    else:
        print(f"No window exists at index {index}")



