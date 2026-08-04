import os
import re
import sys

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
    html_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if f.endswith('.html')]
    broken = False
    baseurl = baseurl_override if baseurl_override is not None else get_baseurl()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Strip script tags to avoid checking href attributes inside JS code strings
            content_no_js = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', content, flags=re.IGNORECASE)
            
            # Find href and src attribute links
            href_links = re.findall(r'href="([^"]+)"', content_no_js)
            src_links = re.findall(r'src="([^"]+)"', content_no_js)
            all_links = set(href_links + src_links)
            
            for link in all_links:
                if link.startswith('http') or link.startswith('//') or link.startswith('data:') or link.startswith('#'):
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
        print("Validation failed: Broken links or missing asset paths detected!")
        sys.exit(1)
    else:
        print("✅ All local links and assets are valid!")

if __name__ == "__main__":
    dir_to_check = sys.argv[1] if len(sys.argv) > 1 else '.'
    baseurl_override = sys.argv[2] if len(sys.argv) > 2 else None
    check_html_links(dir_to_check, baseurl_override)
