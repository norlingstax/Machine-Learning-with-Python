cookies = {}

def player(prev_play, opponent_history=[]):
  global cookies

  n = 3

  if prev_play in ['R', 'P', 'S']:
    opponent_history.append(prev_play)

  guess = 'R'

  if len(opponent_history) > n:
    last_three = ''.join(opponent_history[-n:])

    if ''.join(opponent_history[-(n+1):]) in cookies.keys():
      cookies[''.join(opponent_history[-(n+1):])]+=1
    else:
      cookies[''.join(opponent_history[-(n+1):])]=1

    possible =[last_three +'R', last_three +'P', last_three +'S']

    for i in possible:
      if not i in cookies.keys():
        cookies[i] = 0

    predict = max(possible, key=lambda key: cookies[key])

    if predict[-1] == 'P':
      guess = 'S'
    if predict[-1] == 'R':
      guess = 'P'
    if predict[-1] == 'S':
      guess = 'R'

  return guess
