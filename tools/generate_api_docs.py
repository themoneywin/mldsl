import json
import os
from pathlib import Path

API_PATH = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\api_aliases.json")
OUT_DIR = Path(r"C:\Users\ASUS\Documents\mlctmodified\out\docs")


def md_escape(text: str) -> str:
    return (text or "").replace("`", "\\`")


def main():
    api = json.loads(API_PATH.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    index_lines = ["# MLDSL API", ""]

    for module_name in sorted(api.keys()):
        mod_dir = OUT_DIR / module_name
        mod_dir.mkdir(parents=True, exist_ok=True)
        index_lines.append(f"## `{module_name}`")
        index_lines.append("")

        funcs = api[module_name]
        for func_name in sorted(funcs.keys()):
            spec = funcs[func_name]
            params = spec.get("params") or []
            enums = spec.get("enums") or []
            aliases = spec.get("aliases") or []
            description = (spec.get("description") or "").strip()
            description_raw = (spec.get("descriptionRaw") or "").strip()

            doc_path = mod_dir / f"{func_name}.md"
            sig = f"{module_name}.{func_name}(" + ", ".join(p["name"] for p in params) + ")"
            lines = [f"# `{sig}`", ""]
            if aliases:
                lines.append("- `aliases`: " + ", ".join(f"`{md_escape(a)}`" for a in aliases))
            lines.append(f"- `sign1`: `{md_escape(spec.get('sign1',''))}`")
            lines.append(f"- `sign2`: `{md_escape(spec.get('sign2',''))}`")
            if spec.get("gui"):
                lines.append(f"- `gui`: `{md_escape(spec.get('gui',''))}`")
            lines.append(f"- `id`: `{md_escape(spec.get('id',''))}`")
            lines.append("")

            if description:
                lines.append("## Description")
                lines.append("```")
                lines.append(description)
                lines.append("```")
                lines.append("")
            if description_raw and description_raw != description:
                lines.append("## DescriptionRaw")
                lines.append("```")
                lines.append(description_raw)
                lines.append("```")
                lines.append("")

            if params:
                lines.append("## Params")
                for p in params:
                    lines.append(f"- `{p['name']}`: `{p.get('mode','')}` slot `{p.get('slot')}`")
                lines.append("")

            if enums:
                lines.append("## Enums")
                for e in enums:
                    lines.append(f"- `{e.get('name')}`: slot `{e.get('slot')}`")
                    opts = e.get("options") or {}
                    for k, v in opts.items():
                        lines.append(f"  - `{md_escape(k)}` -> clicks `{v}`")
                lines.append("")

            doc_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            rel = os.path.relpath(doc_path, OUT_DIR)
            index_lines.append(f"- `{module_name}.{func_name}` → `{rel}`")

        index_lines.append("")

    (OUT_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"wrote docs to {OUT_DIR}")


if __name__ == "__main__":
    main()
