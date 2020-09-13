import requests

if __name__ == "__main__":
  for v in range(1, 14):
    for b in range(1, 101):
      url = 'https://krazydad.com/suguru/sfiles/SUG_8x8_v{}_4pp_b{}.pdf'.format(v, b)
      r = requests.get(url, allow_redirects=True)
      open('krazydad/medium/{}/{}.pdf'.format(v, b), 'wb').write(r.content)
      print('saved volume ', v, ': book ', b)
