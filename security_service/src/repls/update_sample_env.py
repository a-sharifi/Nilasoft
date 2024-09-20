# Open the sample.env file and read its content
with open('../../.env', 'r') as file:
    lines = file.readlines()

# Replace the actual values with placeholders
new_lines = []
for line in lines:
    if "=" in line:
        key = line.split("=")[0]
        new_line = f"{key}=<YOUR-{key}>\n"
        new_lines.append(new_line)
    else:
        new_lines.append(line)

# Write the new content back to the sample.env file
with open('../../sample.env', 'w') as file:
    file.writelines(new_lines)
