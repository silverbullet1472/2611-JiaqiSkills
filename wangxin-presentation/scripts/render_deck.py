"""按网信中心主题生成内嵌素材的离线HTML；输入为本机可信制作数据。"""
import argparse
import base64
import html
import json
import mimetypes
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def image_uri(path):
    path = Path(path)
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()


def render(data, output, base):
    title, unit, date = (html.escape(data[k]) for k in ('title', 'unit', 'date'))
    pages = data['pages']
    if not pages:
        raise ValueError('至少需要一页正文')
    chapters = list(dict.fromkeys(p['chapter'] for p in pages))
    sections = []
    nav = []
    # 封面、正式目录、正文、结束页共同使用一个顺序索引。
    for chapter in chapters:
        first = next(i for i, p in enumerate(pages) if p['chapter'] == chapter) + 2
        nav.append((chapter, first))
    images = {p.stem: image_uri(p) for p in (ROOT / 'assets').iterdir()
              if p.suffix.lower() in ('.jpg', '.png')}
    cover_title = '<br>'.join(html.escape(s) for s in data.get('title_lines', [data['title']]))
    circles = ''.join(f'<img class="circle circle-{i}" src="{images[n]}" alt="{a}">'
                      for i, (n, a) in enumerate([('building-portrait', '建筑'), ('dam', '坝体'), ('river', '河流')]))
    sections.append(f'<section class="slide cover-page" aria-label="封面"><img class="ribbon" src="{images["cover-ribbon"]}" alt="">{circles}<h1>{cover_title}</h1><div class="signature">{unit}<br>{date}</div></section>')
    entries = ''.join(f'<button data-go="{idx}"><span>{i+1}</span>{html.escape(name)}</button>' for i, (name, idx) in enumerate(nav))
    sections.append(f'<section class="slide contents-page" aria-label="目录"><div class="contents-left"><h1>目 录</h1><p>CONTENTS</p><div class="contents-entries">{entries}</div></div><div class="contents-art"><img src="{images["building-landscape"]}" alt="建筑照片"></div><i class="slash slash-one"></i><i class="slash slash-two"></i></section>')
    for index, p in enumerate(pages, start=2):
        mains = ''.join(f'<button class="{"current" if c == p["chapter"] else ""}" data-go="{i}" {"aria-current=\"true\"" if c == p["chapter"] else ""}>{html.escape(c)}</button>' for c, i in nav)
        subtopics = list(dict.fromkeys(x['topic'] for x in pages if x['chapter'] == p['chapter'] and x.get('topic')))
        subs = ''
        for topic in subtopics:
            target = next(i for i, x in enumerate(pages, start=2) if x['chapter'] == p['chapter'] and x.get('topic') == topic)
            current = topic == p.get('topic')
            subs += f'<button class="{"current" if current else ""}" data-go="{target}" {"aria-current=\"true\"" if current else ""}>{html.escape(topic)}</button>'
        content = p.get('html', '')
        if 'html_file' in p:
            content = (base / p['html_file']).read_text(encoding='utf-8')
        # 本机正文中的图片在打包时内嵌，不把本机路径带到交付文件。
        def embed(match):
            src = html.unescape(match[1])
            if src.startswith('data:'):
                return match[0]
            if re.match(r'^[a-z]+:', src, re.I):
                raise ValueError(f'图片必须下载到本地后内嵌：{src}')
            return 'src="' + image_uri(base / src) + '"'
        content = re.sub(r'src="([^"]+)"', embed, content)
        pid = html.escape(p.get('id', f'page-{index+1}'), quote=True)
        sections.append(f'<section class="slide content-page" id="{pid}" aria-label="{html.escape(p["title"], quote=True)}"><nav class="chapter-nav" aria-label="章节">{mains}</nav><nav class="topic-nav" aria-label="主题">{subs}</nav><h2>{html.escape(p["title"])}</h2><div class="body">{content}</div><footer class="slide-foot"><span>{unit}</span><span>{index+1:02d} / {len(pages)+3:02d}</span></footer></section>')
    closing = html.escape(data.get('closing', '请批评指正，谢谢！'))
    river = (ROOT / 'assets/closing-frame.svg').read_text(encoding='utf-8').replace('IMAGE_URI', images['closing-river'])
    river = river.replace('<svg ', '<svg class="closing-river" ', 1)
    sections.append(f'<section class="slide closing-page" aria-label="结束页"><h1>{closing}</h1>{river}<div class="signature">{unit}<br>{date}</div></section>')
    css = data.get('content_css', '')
    if 'content_css_file' in data:
        css += (base / data['content_css_file']).read_text(encoding='utf-8')
    # 统一既有正文中单独指定的中英文字体，保留字号、字重及斜体设置。
    for old in ('"Microsoft YaHei","PingFang SC",sans-serif',
                '"Microsoft YaHei",sans-serif', 'Arial,sans-serif',
                'Arial', 'Georgia,serif', 'Georgia'):
        css = css.replace(old, 'var(--report-font)')
    css += (ROOT / 'assets/theme.css').read_text(encoding='utf-8')
    css = css.replace('MAP_IMAGE', images['map-background'])
    js = (ROOT / 'assets/player.js').read_text(encoding='utf-8')
    labels = ['封面', '目录'] + [p['title'] for p in pages] + ['结束页']
    labels_json = json.dumps(labels, ensure_ascii=False).replace('<', '\\u003c')
    js = 'const titles=' + labels_json + ';\n' + js
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="font-attribution" content="使用 MiSans 字体，版权归小米所有；许可协议：https://hyperos.mi.com/font-download/MiSans字体知识产权许可协议.pdf"><link rel="preconnect" href="https://cdn-font.hyperos.mi.com" crossorigin><link rel="preconnect" href="https://cdn-file.hyperos.mi.com" crossorigin><link rel="stylesheet" href="https://cdn-font.hyperos.mi.com/font/css?family=MiSans_VF:VF:Chinese_Simplify,Latin&amp;display=swap"><style>{css}</style></head><body><main id="viewport"><div id="deck">{"".join(sections)}</div></main><nav class="controls" aria-label="演示控制"><div class="progress"></div><button id="prev">← 上一页</button><span id="counter" aria-live="polite"></span><button id="next">下一页 →</button><button id="toc">目录</button><button id="overview">全部页面</button><button id="fullscreen">全屏</button><button id="pointer" aria-pressed="true" title="H键切换鼠标高亮">鼠标高亮：开</button><button id="print">打印 / PDF</button></nav><dialog id="toc-dialog"><button class="close">关闭 ×</button><h3>全部页面</h3><div id="toc-list"></div></dialog><dialog id="lightbox"><button class="close">关闭 ×</button><img alt=""></dialog><script>{js}</script></body></html>', encoding='utf-8')
    return len(sections)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = json.loads(args.input.read_text(encoding='utf-8-sig'))
    count = render(data, args.output, args.input.resolve().parent)
    print(f'已生成 {count} 页：{args.output.resolve()}')
