from utils.finance import get_new_finance
import configs
import init
import os
os.chdir(os.path.join(os.getcwd(), '..'))


if __name__ == '__main__':
    get_new_finance()
