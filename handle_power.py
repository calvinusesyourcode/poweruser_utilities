import yaml, argparse, os

def main(mode):


    if mode is None:
        raise ValueError("mode must be startup or shutdown or fauxshutdown")
        
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    from handle_github import auto_pull, auto_push
    auto_pull(config) if mode == "startup" else auto_push(config)
    os.system("shutdown -s -t 1") if mode == "shutdown" else None

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="handle power events")
    parser.add_argument("--mode", "-m", type=str, required=True, help="startup or shutdown or fauxshutdown")
    args = parser.parse_args()
    main(args.mode)