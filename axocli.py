import argparse
import os

POM_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://apache.org"
         xmlns:xsi="http://w3.org"
         xsi:schemaLocation="http://apache.org http://apache.org">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>1.0-SNAPSHOT</version>

    <properties>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <dependency>
            <groupId>axo.jvm</groupId>
            <artifactId>axojvm-runtime</artifactId>
            <version>1.0.0</version>
            <scope>system</scope>
            <systemPath>${{project.basedir}}/libs/axojvm-runtime.jar</systemPath>
        </dependency>
    </dependencies>

</project>
"""

MOD_JSON_TEMPLATE = """{{
  "modId": "{mod_id}",
  "version": "1.0.0",
  "name": "{mod_name}",
  "author": "ExampleDev",
  "description": "Example description",
  "modIcon": "mod-icon.png",
  "side": "BOTH",
  "entrypoint": "axo.{package}.Main",
  "dependencies": [
    {{ "modId": "axojvm", "version": ">=1.0.0" }}
  ],
  "conflicts": []
}}"""

MAIN_JAVA_TEMPLATE = """package axo.{package};

import axo.jvm.AxoMod;
import axo.jvm.event.*;


public class Main implements AxoMod {{

    @Override
    public void onEnable() {{
        // Your code goes here
    }}

    @Override
    public void onDisable() {{
        // Your code goes here
    }}

    @Override
    public void onRegisterBlock(RegisterBlockEvent event){{
    }}
    @Override
    public void onRegisterItem(RegisterItemEvent event){{
    }}
    @Override
    public void onRegisterBiome(RegisterBiomeEvent event){{
    }}
    @Override
    public void onRegisterWorldGen(RegisterWorldGenEvent event) {{
    }}
}}"""

def main():
    parser = argparse.ArgumentParser(
        description="CLI Tool for creating AxoJVM Mods"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    create_parser = subparsers.add_parser(
        "createproject", help="Creates new AxoJVM mod project in current folder"
    )
    create_parser.add_argument("project_name", type=str, help="Project Name")
    create_parser.add_argument("package", type=str, help="Package Name")
    create_parser.add_argument("mod_id", type=str, help="Mod ID")
    args = parser.parse_args()

    if args.command == "createproject":
        src_path = os.path.join(args.project_name, "src", "main", "java", "axo", args.package)
        libs_path = os.path.join(args.project_name, "libs")
        resources_path = os.path.join(args.project_name, "src", "main", "resources")
        try:
            os.makedirs(src_path, exist_ok=False)
            os.makedirs(libs_path, exist_ok=False)

            lang_path = os.path.join(resources_path, "assets", args.mod_id, "lang")
            os.makedirs(lang_path, exist_ok=False)

            os.makedirs(os.path.join(resources_path, "assets", args.mod_id, "textures", "blocks"),exist_ok=False,)
            os.makedirs(os.path.join(resources_path, "assets", args.mod_id, "textures", "items"),exist_ok=False,)

            main_java_content = MAIN_JAVA_TEMPLATE.format(package=args.package)
            main_java_path = os.path.join(src_path, "Main.java")
            with open(main_java_path, "w", encoding="utf-8") as main_file:
                main_file.write(main_java_content)
            
            lang_file_path = os.path.join(lang_path, "en_US.lang")
            with open(lang_file_path, "w", encoding="utf-8") as lang_file:
                pass

            json_content = MOD_JSON_TEMPLATE.format(mod_id=args.mod_id,mod_name=args.project_name,package=args.package,)
            json_path = os.path.join(resources_path, "axo.mod.json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json_file.write(json_content)

            generated_group_id = f"axo.{args.package}"

            file_content = POM_TEMPLATE.format(group_id=generated_group_id, artifact_id=args.project_name)
            pom_path = os.path.join(args.project_name, "pom.xml")
            with open(pom_path, "w", encoding="utf-8") as pom_file:
                pom_file.write(file_content)
            print("Succesfuly created project with name: " + args.project_name)
        except FileExistsError:
            print("Failed creating project with name: " + args.project_name)
        except Exception as e:
            print("Failed creating project with name: " + args.project_name)


if __name__ == "__main__":
    main()
