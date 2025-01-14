import os

def generate_project_hierarchy(directory):
    project_hierarchy = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.h') or file.endswith('.c'):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                project_hierarchy.append(relative_path)

    # Sort files: prioritize .h before .c for files with the same base name
    project_hierarchy.sort(key=lambda x: (os.path.splitext(x)[0], x.endswith('.c')))

    project_hierarchy_text = "\n".join(["├── " + file for file in project_hierarchy])
    return project_hierarchy_text, project_hierarchy

def generate_file_xml(file_path, file_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    file_xml = ("""
<file name="{file_name}">
<![CDATA[
{content}
]]>
</file>
""").format(file_name=file_name, content=content).strip()
    return file_xml

def generate_task_prompt(directory, output_file):
    project_hierarchy_text, project_hierarchy = generate_project_hierarchy(directory)
    files_content = []

    for relative_path in project_hierarchy:
        file_path = os.path.join(directory, relative_path)
        file_name = os.path.basename(file_path)
        file_xml = generate_file_xml(file_path, file_name)
        files_content.append(file_xml)

    output = ("""
<task_prompt>
<project_hierarchy>
AUTOTUNEIT/
{project_hierarchy_text}
</project_hierarchy>
<files>
{files_content}
</files>
<task_description>
</task_description>
</task_prompt>
""").format(
        project_hierarchy_text=project_hierarchy_text, 
        files_content="\n\n".join(files_content)
    ).strip()

    # Write to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

# Replace 'your_directory_path' with the path to your directory containing .h and .c files
# Replace 'output_file_path' with the path to the output file

input_directory = "./"
output_file_path = "./AI_helper/output.prompt"

generate_task_prompt(input_directory, output_file_path)
print(f"Task prompt generated and saved to {output_file_path}")