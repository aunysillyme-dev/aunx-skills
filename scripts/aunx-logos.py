#!/usr/bin/env python3
"""Draw original SVG marks and render all ten 512px PNG exports locally."""
import html
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKS = {
    "full-output-keeper": (["Full Output", "Keeper"], '<rect x="150" y="140" width="212" height="170" rx="18"/><path d="M177 173h115m-115 35h156m-156 35h100"/><path d="M298 285l25 25 43-51"/>'),
    "number-guard": (["Number", "Guard"], '<path d="M256 122l96 39v70c0 60-53 96-96 119-43-23-96-59-96-119v-70z"/><path d="M222 190v90m68-90v90m-92-65h114m-114 40h114"/>'),
    "x-spaces-transcriber": (["X Spaces", "Transcriber"], '<rect x="218" y="133" width="76" height="136" rx="38"/><path d="M188 226v14a68 68 0 00136 0v-14m-68 82v28m-35 0h70"/><path d="M155 177v46m202-46v46"/>'),
    "docs-fetch-ladder": (["Docs Fetch", "Ladder"], '<path d="M164 135h184v204H164zM203 135v204m55-204v204m-55-164h55m-55 44h55m-55 44h55m-55 44h55"/><path d="M287 180h34m-34 44h34m-34 44h34"/>'),
    "absence-check": (["Absence", "Check"], '<circle cx="233" cy="219" r="82"/><path d="M291 277l66 66m-166-122l28 28 58-58"/>'),
    "instruction-weight": (["Instruction", "Weight"], '<path d="M160 335h192M180 335v-45h36v45m22 0v-90h36v90m22 0V200h36v135"/><path d="M160 156h170m-170 38h107"/>'),
    "rename-sweep": (["Rename", "Sweep"], '<path d="M154 159h143l43 43-43 43H154zM340 283H197l-43 43 43 43h143z"/><path d="M185 202h105m20 124H205"/>'),
    "ticket-gate": (["Ticket", "Gate"], '<path d="M165 144h182v55a29 29 0 000 58v65H165v-65a29 29 0 000-58z"/><path d="M214 227l27 27 59-60"/>'),
    "client-work-to-template": (["Client Work", "to Template"], '<rect x="153" y="131" width="149" height="184" rx="12"/><rect x="205" y="179" width="149" height="184" rx="12" fill="#10252e"/><path d="M234 216h90m-90 38h55m-55 38h90m-90 38h55"/>'),
    "retro-to-rules": (["Retro", "to Rules"], '<path d="M173 197a93 93 0 1112 117M173 153v59h59"/><path d="M219 256l29 29 56-62"/>'),
}


def main():
    output = ROOT / "logos"
    output.mkdir(exist_ok=True)
    for slug, (lines, glyph) in MARKS.items():
        text = "".join(f'<text x="256" y="{408 + i * 41}" text-anchor="middle">{html.escape(line)}</text>'
                       for i, line in enumerate(lines))
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<rect width="512" height="512" rx="42" fill="#10252e"/>
<rect x="20" y="20" width="472" height="472" rx="30" fill="none" stroke="#73e3be" stroke-width="3"/>
<text x="44" y="65" fill="#73e3be" font-family="Arial,sans-serif" font-size="24" font-weight="700" letter-spacing="4">AUNX</text>
<g fill="none" stroke="#73e3be" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">{glyph}</g>
<g fill="#f5f2e9" font-family="Arial,sans-serif" font-weight="700" font-size="35">{text}</g>
</svg>
'''
        source = output / f"{slug}.svg"
        source.write_text(svg)
        subprocess.run(["rsvg-convert", "-w", "512", "-h", "512", "-o",
                        str(output / f"{slug}.png"), str(source)], check=True)
    print(f"Rendered {len(MARKS)} original SVG/PNG pairs at 512x512")


if __name__ == "__main__":
    main()
