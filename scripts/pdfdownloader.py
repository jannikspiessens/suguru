import requests, subprocess, time

auth = "vpn/auth"
fmt = "vpn/us/us-free-{}.protonvpn.net.udp.ovpn"
configs = [fmt.format(str(i).zfill(2)) for i in range(1, 28)]

class VPN_Switcher:

    def __init__(self, configs, auth):
        self.i = -1
        self.configs = configs
        self.auth = auth
        self.process = None
        self.process = self.next()

    def next(self):
        self.i += 1
        if not self.process is None:
            print('terminating previous vpn')
            self.process.terminate()
            time.sleep(5)
        print('opening vpn', self.i)
        cmd = "openvpn --config " + self.configs[self.i] + " --auth-user-pass " + self.auth
        return subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

if __name__ == "__main__":
    vpn = VPN_Switcher(configs, auth)
    for v in range(1, 14):
        for b in range(26, 101):
            url = 'https://krazydad.com/suguru/sfiles/SUG_8x8_v{}_4pp_b{}.pdf'.format(v, b)
            try:
                print('requesting', url)
                r = requests.get(url)
            except:
                print('switching VPN')
                vpn.next()
                print('retrying request')
                r = requests.get(url)
            open('../data/pdf/medium_{}_{}.pdf'.format(v, b), 'wb').write(r.content)
            print('saved volume ', v, ': book ', b)
