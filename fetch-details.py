import requests

# Replace these with your actual Notion API key and database ID
NOTION_API_KEY = 'secret_pBswAuQerH5m5IA6sJHL9GsMW64DZIfLsJBoTdlHYJy'
DATABASE_ID = '4c07b2ef17f24d8fb7d4847ee9cf885f'
MARKDOWN_FILE = 'index/index.md'

def get_notion_database_content():
    url = f'https://api.notion.com/v1/databases/{DATABASE_ID}/query'
    headers = {
        'Authorization': f'Bearer {NOTION_API_KEY}',
        'Notion-Version': '2022-06-28'  # Use the latest Notion API version
    }
    
    response = requests.post(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch database content. Status code: {response.status_code}")
        print(response.json())
        return None

def extract_project_names(database_content):
    project_names = []
    for result in database_content.get('results', []):
        try:
            title = result['properties']['Project Name']['title'][0]['plain_text']
            project_names.append(title)
        except (KeyError, IndexError) as e:
            print(f"Error extracting project name from entry: {e}")
            continue
    return project_names

def update_markdown_file(project_names, file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    in_projects_section = False

    for line in lines:
        if line.strip() == '## Projects':
            in_projects_section = True
            new_lines.append(line)
            new_lines.append('\n'.join(f'- {name}' for name in project_names) + '\n')
        elif line.startswith('##') and in_projects_section:
            in_projects_section = False
            new_lines.append(line)
        elif not in_projects_section:
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    database_content = get_notion_database_content()
    if database_content:
        project_names = extract_project_names(database_content)
        if project_names:
            update_markdown_file(project_names, MARKDOWN_FILE)
            print("Project Names:")
            for name in project_names:
                print(f"- {name}")
        else:
            print("No project names found.")
