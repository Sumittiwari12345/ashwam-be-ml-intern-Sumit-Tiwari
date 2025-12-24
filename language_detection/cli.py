import argparse
import json
import sys

from .detector import analyze_text


def parse_jsonl_line(line, line_no):
    try:
        return json.loads(line)
    except json.JSONDecodeError as exc:
        print(f"Skipping invalid JSON on line {line_no}: {exc}", file=sys.stderr)
        return None


def run_cli(in_path, out_path):
    with open(in_path, "r", encoding="utf-8") as f_in, open(out_path, "w", encoding="utf-8") as f_out:
        for line_no, line in enumerate(f_in, start=1):
            line = line.strip()
            if not line:
                continue
            payload = parse_jsonl_line(line, line_no)
            if payload is None:
                continue
            text = payload.get("text", "")
            result = analyze_text(text)
            result["id"] = payload.get("id", "")
            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Rule-based language and script detector.")
    parser.add_argument("--in", dest="in_path", required=True, help="Path to input texts.jsonl")
    parser.add_argument("--out", dest="out_path", required=True, help="Path to output lang.jsonl")
    args = parser.parse_args(argv)
    run_cli(args.in_path, args.out_path)


if __name__ == "__main__":
    main()
