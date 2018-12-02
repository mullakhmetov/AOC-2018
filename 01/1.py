def main():
    with open('input.txt', 'r') as f:
        print(eval(' '.join([l.strip() for l in f.readlines()])))


if __name__ == '__main__':
    main()
