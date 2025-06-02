from collections import deque

def is_one_letter_diff(a, b):
    if len(a) != len(b): return False
    diff = sum(1 for x, y in zip(a, b) if x != y)
    return diff == 1

def bfs(words, start, end):
    word_set = set(words)
    if end not in word_set:
        return 0

    visited = set()
    queue = deque([(start, 1)])
    visited.add(start)

    while queue:
        current, dist = queue.popleft()
        if current == end:
            return dist

        for word in word_set:
            if word not in visited and is_one_letter_diff(current, word):
                visited.add(word)
                queue.append((word, dist + 1))

    return 0

def solve_file(file_path, team_number):
    with open(file_path) as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) < 2:
        return 0

    end = lines[-1]
    dictionary = lines[:-1]
    start_index = team_number % len(dictionary)
    start = dictionary[start_index]

    return bfs(dictionary, start, end)

def main():
    team_number = 26
    files = ["data0.csv", "data1.csv", "data2.csv", "data3.csv"]
    results = [solve_file(file, team_number) for file in files]
    print(f"[{', '.join(map(str, results))}]")

if __name__ == "__main__":
    main()
