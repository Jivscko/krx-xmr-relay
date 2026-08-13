import paramiko
import time

VPS_FILE = 'vps.txt'
SSH_KEY_PATH = 'vps_key.pem'
SSH_USER = 'root'
BASH_URL = 'https://pub-bb6723fa45b54588811315105aa22358.r2.dev/bash.sh'

def run_cmd(ssh, cmd, timeout=60):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=timeout)
    exit_code = stdout.channel.recv_exit_status()
    return exit_code, stdout.read().decode(), stderr.read().decode()

def main():
    with open(VPS_FILE) as f:
        ips = [l.strip() for l in f if l.strip()]

    key = paramiko.Ed25519Key.from_private_key_file(SSH_KEY_PATH)
    print(f"Total VPS: {len(ips)}")

    for idx, ip in enumerate(ips, 1):
        print(f"\n[{idx}/{len(ips)}] {ip}")

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ip, username=SSH_USER, pkey=key, timeout=15)

            # Step 1: Install dependencies
            print("  [1/3] Install libhwloc15 curl...")
            code, out, err = run_cmd(ssh, "apt-get update -qq && apt-get install -y -qq libhwloc15 curl", timeout=120)
            if code != 0:
                print(f"  -> Install gagal: {err[:100]}")
                ssh.close()
                continue
            print("  -> OK")

            # Step 2: Setup hugepages
            print("  [2/3] Setup hugepages...")
            run_cmd(ssh, "echo 3072 > /proc/sys/vm/nr_hugepages 2>/dev/null || sysctl -w vm.nr_hugepages=3072 2>/dev/null || true")
            print("  -> OK")

            # Step 3: Download & run in screen
            print("  [3/3] Download & start miner...")
            run_cmd(ssh, f"curl -sL {BASH_URL} -o /tmp/bash.sh && chmod +x /tmp/bash.sh")
            ssh.exec_command("screen -dmS xmr bash /tmp/bash.sh")
            time.sleep(5)

            # Check status
            code, out, err = run_cmd(ssh, "screen -ls 2>/dev/null | grep -q 'xmr' && echo RUNNING || echo DEAD")
            status = out.strip()
            print(f"  -> Screen: {status}")

            ssh.close()

        except Exception as e:
            print(f"  -> Error: {e}")

        time.sleep(2)

    print(f"\nDone. Cek miner di VPS: screen -r xmr")

if __name__ == "__main__":
    main()
