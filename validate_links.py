import os
import re
import sys
from html.parser import HTMLParser

STANDARD_HTML_TAGS = {
    'a', 'abbr', 'address', 'area', 'article', 'aside', 'audio', 'b', 'base', 'bdi', 'bdo',
    'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'cite', 'code', 'col', 'colgroup',
    'data', 'datalist', 'dd', 'del', 'details', 'dfn', 'dialog', 'div', 'dl', 'dt', 'em', 'embed',
    'fieldset', 'figcaption', 'figure', 'footer', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'head', 'header', 'hgroup', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'kbd',
    'label', 'legend', 'li', 'link', 'main', 'map', 'mark', 'menu', 'meta', 'meter', 'nav',
    'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'picture', 'pre',
    'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small',
    'source', 'span', 'strong', 'style', 'sub', 'summary', 'sup', 'svg', 'table', 'tbody', 'td',
    'template', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'u', 'ul',
    'var', 'video', 'wbr', 'path', 'g', 'circle', 'rect', 'line', 'polygon', 'polyline', '!doctype'
}

VOID_TAGS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr', '!doctype'
}

class HTMLValidator(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tag_stack = []
        self.errors = []

    def handle_starttag(self, tag, attrs):
        tag_lower = tag.lower()
        if tag_lower not in STANDARD_HTML_TAGS:
            self.errors.append(f"Invalid/unknown HTML tag `<{tag}>` found in {self.filename}")
        if tag_lower not in VOID_TAGS:
            self.tag_stack.append(tag_lower)

    def handle_endtag(self, tag):
        tag_lower = tag.lower()
        if tag_lower in VOID_TAGS:
            return
        if not self.tag_stack:
            self.errors.append(f"Unexpected closing tag `</{tag}>` without matching start tag in {self.filename}")
            return
        last_tag = self.tag_stack.pop()
        if last_tag != tag_lower:
            self.errors.append(f"Mismatched HTML tag: expected `</{last_tag}>`, got `</{tag}>` in {self.filename}")

    def check_unclosed(self):
        if self.tag_stack:
            self.errors.append(f"Unclosed HTML tags in {self.filename}: {', '.join(self.tag_stack)}")

def get_baseurl():
    baseurl = ""
    try:
        with open('_config.yml', 'r') as f:
            for line in f:
                if line.startswith('baseurl:'):
                    match = re.search(r'baseurl:\s*["\']?([^"\']+)["\']?', line)
                    if match:
                        baseurl = match.group(1).strip()
    except Exception:
        pass
    return baseurl

def check_html_links(directory, baseurl_override=None):
    IGNORED_DIRS = {'vendor', '.git', '.jekyll-cache', 'node_modules'}
    
    html_files = []
    for dp, dn, filenames in os.walk(directory):
        dn[:] = [d for d in dn if d not in IGNORED_DIRS]
        for f in filenames:
            if f.endswith('.html'):
                html_files.append(os.path.join(dp, f))

    broken = False
    baseurl = baseurl_override if baseurl_override is not None else get_baseurl()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Strict HTML Structure & Tag Check
            validator = HTMLValidator(html_file)
            try:
                validator.feed(content)
                validator.check_unclosed()
                if validator.errors:
                    for err in validator.errors:
                        print(f"❌ HTML Error: {err}")
                    broken = True
            except Exception as e:
                print(f"❌ HTML Parsing Error in {html_file}: {e}")
                broken = True

            # Strip script tags to avoid checking href attributes inside JS code strings
            content_no_js = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', content, flags=re.IGNORECASE)
            
            # Find href and src attribute links
            href_links = re.findall(r'href="([^"]+)"', content_no_js)
            src_links = re.findall(r'src="([^"]+)"', content_no_js)
            all_links = set(href_links + src_links)
            
            for link in all_links:
                if link.startswith(('http', '//', 'data:', '#', 'mailto:', 'tel:', 'javascript:', '{{')):
                    continue
                
                # Resolve target path based on whether the link is absolute or relative
                if baseurl and link.startswith(baseurl):
                    relative_to_root = link[len(baseurl):].lstrip('/')
                    target_path = os.path.join(directory, relative_to_root)
                elif link.startswith('/'):
                    target_path = os.path.join(directory, link.lstrip('/'))
                else:
                    target_path = os.path.join(os.path.dirname(html_file), link)

                if not os.path.exists(target_path) and not os.path.exists(target_path + '.html') and not os.path.exists(target_path + '/index.html'):
                    print(f"❌ Broken link/asset found in {html_file}: {link}")
                    broken = True

    if broken:
        print("Validation failed: HTML errors, broken links, or missing asset paths detected!")
        sys.exit(1)
    else:
        print("✅ All HTML syntax, local links, and assets are valid!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        dir_to_check = sys.argv[1]
    else:
        dir_to_check = './_site' if os.path.exists('./_site') else '.'
        
    baseurl_override = sys.argv[2] if len(sys.argv) > 2 else None
    check_html_links(dir_to_check, baseurl_override)
