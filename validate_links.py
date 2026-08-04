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

def check_html_links(directory):
    html_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if f.endswith('.html')]
    broken = False
    baseurl = get_baseurl()
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find simple href links
            links = re.findall(r'href="([^"]+)"', content)
            for link in links:
                if link.startswith('http') or link.startswith('#'):
                    continue
                
                # Resolve target path based on whether the link is absolute or relative
                if baseurl and link.startswith(baseurl):
                    # Absolute link with baseurl (e.g. /zivops/assets/css/style.css)
                    relative_to_root = link[len(baseurl):].lstrip('/')
                    target_path = os.path.join(directory, relative_to_root)
                elif link.startswith('/'):
                    # Absolute link without baseurl (fallback)
                    target_path = os.path.join(directory, link.lstrip('/'))
                else:
                    # Relative link (e.g. assets/css/style.css or ../style.css)
                    target_path = os.path.join(os.path.dirname(html_file), link)

                if not os.path.exists(target_path) and not os.path.exists(target_path + '.html') and not os.path.exists(target_path + '/index.html'):
                    print(f"Broken link found in {html_file}: {link}")
                    broken = True

    if broken:
        sys.exit(1)
    else:
        print("All local links are valid!")

if __name__ == "__main__":
    dir_to_check = sys.argv[1] if len(sys.argv) > 1 else '.'
    check_html_links(dir_to_check)
