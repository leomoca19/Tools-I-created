import urllib.request as req
from bs4 import BeautifulSoup


def extract_grid(html_content):
    table = BeautifulSoup(html_content, 'html.parser').find('table')
    x_coords, values, y_coords = [], [], []
    
    for row in table.find_all('tr')[1:]:  
        x, val, y = [cell.text for cell in row.find_all('span')]
        x_coords.append(int(x))
        values.append(val)
        y_coords.append(int(y))

    return [x_coords, values, y_coords]

def main(url):
    grid = extract_grid(req.urlopen(url).read())

    max_x = max(grid[0]) + 1
    max_y = max(grid[2]) + 1
    rows = [[' '] * max_x for _ in range(max_y)]

    for i in range(len(grid[0])):
        x = grid[0][i]
        y = grid[2][i]

        rows[y][x] = grid[1][i]

    for i in reversed(range(len(rows))): print(''.join(rows[i]))

main('https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub')
