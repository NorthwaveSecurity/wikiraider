from Parser import Parser

if __name__ == '__main__':
    files = ['a', 'b', 'c']
    parser = Parser(files)

    parser.start()
    print('parser.start()')
    parser.join()
    print('parser.join()')
    print('finished...')