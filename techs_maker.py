import os
import toml


def img_dir(id, format):
    return f"./icons/{id}.{format}"


def tech_to_row(tech_list):
    row = []

    for tech in tech_list:
        identifier = (
            tech.lower()
            .replace(" ", "")
            .replace("+", "plus")
            .replace(".", "dot")
        )
        src = img_dir(identifier, "svg")

        if not os.path.exists(src):
            src = img_dir(identifier, "png")
            if not os.path.exists(src):
                raise FileNotFoundError(
                    f"Image for {identifier} doesn't exist"
                )

        row.append(
            f'<picture><img alt="{tech}" title="{tech}" height=32 src="{src}" /></picture>'
        )

    return row


def join(list):
    return " ".join(list)


def generate_table():
    md_table = (
        "| Category | Proficient | Have worked with |\n"
        "| -------: | :-------: | :-------------: |\n"
    )

    table = toml.load("./tech.toml")

    for key, value in table.items():
        high = tech_to_row(value["high"])
        low = tech_to_row(value["low"])
        md_table += f"| {value['name']} | {join(high)} | {join(low)} |\n"

    return md_table


if __name__ == "__main__":
    with open("README.md", "r", encoding="utf-8") as file:
        content = file.read()

    start_marker = "<!-- start:tech -->"
    end_marker = "<!-- end:tech -->"

    startpos = content.find(start_marker)
    endpos = content.find(end_marker)

    if startpos == -1 or endpos == -1:
        raise ValueError("Start or end marker not found")

    startpos += len(start_marker)

    new_content = (
        f"{content[:startpos]}\n{generate_table()}\n{content[endpos:]}"
    )

    with open("README.md", "w", encoding="utf-8") as file:
        file.write(new_content)

    print("Done!")
