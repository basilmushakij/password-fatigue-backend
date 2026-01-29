import numpy as np

KEY_MAP = {
    '`':(0,0), '~':(0,0), '1':(1,0), '!':(1,0), '2':(2,0), '@':(2,0), '3':(3,0), '#':(3,0), '4':(4,0), '$':(4,0), '5':(5,0), '%':(5,0),
    '6':(6,0), '^':(6,0), '7':(7,0), '&':(7,0), '8':(8,0), '*':(8,0), '9':(9,0), '(':(9,0), '0':(10,0), ')':(10,0), '-':(11,0), '_':(11,0), '=':(12,0), '+':(12,0),
    'q':(1.5,1), 'w':(2.5,1), 'e':(3.5,1), 'r':(4.5,1), 't':(5.5,1), 'y':(6.5,1), 'u':(7.5,1), 'i':(8.5,1), 'o':(9.5,1), 'p':(10.5,1),
    '[':(11.5,1), '{':(11.5,1), ']':(12.5,1), '}':(12.5,1), '\\':(13.5,1), '|':(13.5,1),
    'a':(1.8,2), 's':(2.8,2), 'd':(3.8,2), 'f':(4.8,2), 'g':(5.8,2), 'h':(6.8,2), 'j':(7.8,2), 'k':(8.8,2), 'l':(9.8,2),
    ';':(10.8,2), ':':(10.8,2), "'":(11.8,2), '"':(11.8,2),
    'z':(2.3,3), 'x':(3.3,3), 'c':(4.3,3), 'v':(5.3,3), 'b':(6.3,3), 'n':(7.3,3), 'm':(8.3,3),
    ',':(9.3,3), '<':(9.3,3), '.':(10.3,3), '>':(10.3,3), '/':(11.3,3), '?':(11.3,3)
}

def extract_features(password):
    password = password.lower()
    if not password: return [0, 0, 0, 0]

    distances = []
    sequential_moves = 0
    
    for i in range(len(password) - 1):
        char1, char2 = password[i], password[i+1]
        
        if char1 in KEY_MAP and char2 in KEY_MAP:
            p1, p2 = KEY_MAP[char1], KEY_MAP[char2]
            
            dist = np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            distances.append(dist)
            
            if 0.9 <= dist <= 1.3:
                sequential_moves += 1
                
    avg_dist = np.mean(distances) if distances else 0
    length = len(password)
    unique_ratio = len(set(password)) / length if length > 0 else 0
    seq_ratio = sequential_moves / (length - 1) if length > 1 else 0

    return [avg_dist, length, unique_ratio, seq_ratio]