import os
import re
import sys

def check_html_links(directory):
    html_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(directory) for f in filenames if f.endswith('.html')]
    broken = False
    
    for html_file in html_files:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Find simple href links
            links = re.findall(r'href="([^"]+)"', content)
            for link in links:
                if link.startswith('http') or link.startswith('#'):
                    continue
                # Local link check
                target_path = os.path.join(os.path.dirname(html_file), link.strip('/'))
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
