from utils.system import check_root, detect_distro, dep_installation
import argparse
import sys
def main ():
    parser = argparse.ArgumentParser(description="Evil_nix Auto Installer")
    parser.add_argument("--domain", required=True,  help="Domain is required")
    parser.add_argument("--ip", required=True, help="Ip is required")
    args = parser.parse_args()
    print(f"Domain: {args.domain}")
    print(f"IP: {args.ip}")
    try:
       if not check_root() :
           sys.exit(1)
    except AttributeError:
        print("\n❌ Usage: install-evil --domain your.domain.com --ip your.ip.addr\n")
        sys.exit(1)
if  __name__ == "__main__":
    main()
