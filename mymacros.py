import os
import datetime
import yaml
import json
import re  # 导入正则表达式模块


class DoubleQuotedDumper(yaml.Dumper):
    def represent_scalar(self, tag, value, style=None):
        if style is None:
            style = '"'
        return super().represent_scalar(tag, value, style)


def define_env(env):
    @env.macro
    def list_md_files(dir, depth=None):
        """列出指定目录及其子目录下的所有 .md 文件，直到指定的深度。"""
        md_files = []
        try:
            for entry in os.listdir(dir):
                full_path = os.path.join(dir, entry)
                if os.path.isdir(full_path):
                    if depth is not None and depth > 0:
                        md_files.extend(list_md_files(full_path, depth - 1))
                    elif depth == 0:
                        continue
                elif entry.endswith('.md'):
                    md_files.append(full_path)
            return md_files
        except Exception as e:
            return f"Error listing files: {e}"

    # 用于生成 grid 卡片
    @env.macro
    def generate_grid_cards(dir):
        """生成 grid 卡片内容，遍历指定目录下的所有以 '_' 开头的文件夹。"""
        grid_cards = []
        try:
            for folder_name in os.listdir(dir):
                folder_path = os.path.join(dir, folder_name)
                if os.path.isdir(folder_path) and folder_name.startswith('_'):
                    # 移除文件夹名前的下划线并转换为标题格式
                    title = folder_name[1:].replace('_', ' ').title()

                    # 使用文件夹名和 "index.md" 生成 MkDocs 路径
                    doc_path = f"{folder_name}"
                    grid_cards.append(
                        f"-   :material-clock-fast:{{ '.lg .middle' }} [__{title}__](/sagi_database/{doc_path})")
            return "\n".join(grid_cards)
        except Exception as e:
            return f"Error generating grid cards: {e}"

    @env.macro
    def generate_changelog_yaml():
        """生成符合 changelog 插件格式的 YAML 文件。"""
        changelog_data = []  # 最外层为列表
        debug_info = []  # 用于存储调试信息
        try:
            # 遍历 docs 目录下的所有以 '_' 开头的文件夹
            for folder_name in os.listdir('docs'):  # 列出docs目录中的所有文件和文件夹
                folder_path = os.path.join('docs', folder_name)  # 构建每个文件夹的完整路径
                # 检查路径是否为目录且目录名为_开头
                if os.path.isdir(folder_path) and folder_name.startswith('_'):
                    # 遍历文件夹下所有的以 yymdd- 开头的 md 文件
                    for file_name in os.listdir(folder_path):
                        if file_name.endswith('.md') and re.match(r'^\d{6}-', file_name):
                            # 构建文件的完整路径
                            full_path = os.path.join(folder_path, file_name)
                            # 从文件名中提取日期
                            date_str = file_name.split('-')[0]
                            try:
                                # 将日期字符串转换为日期对象
                                date_obj = datetime.datetime.strptime(
                                    date_str, "%y%m%d")
                                # 将日期对象转换为可读格式
                                readable_time = date_obj.strftime("%Y-%m-%d")
                                year = date_obj.strftime("%Y")
                                # 查找或创建年份条目
                                year_entry = next(
                                    (item for item in changelog_data if year in item), None)
                                if not year_entry:
                                    year_entry = {year: []}
                                    changelog_data.append(year_entry)
                                # 查找或创建日期条目
                                found = False
                                for entry in year_entry[year]:
                                    if readable_time in entry:  # 如果找到日期条目
                                        found = True
                                        entry[readable_time].append({
                                            "newpage": {
                                                "text": f" [ {folder_name.replace('_', '')} ] > {'-'.join(file_name.split('-')[1:]).replace('.md', '')}",
                                                "href": f"/sagi_database/{folder_name}/{file_name.replace('.md', '')}"
                                            }
                                        })
                                        break
                                # 如果没有找到日期条目，则创建新的
                                if not found:
                                    year_entry[year].append({
                                        readable_time: [{
                                            "newpage": {
                                                "text": f" [ {folder_name.replace('_', '')} ] > {'-'.join(file_name.split('-')[1:]).replace('.md', '')}",
                                                "href": f"/sagi_database/{folder_name}/{file_name.replace('.md', '')}"
                                            }
                                        }]
                                    })
                                # 对年份条目中的日期进行降序排序
                                year_entry[year] = sorted(
                                    year_entry[year], key=lambda x: list(x.keys())[0], reverse=True)
                            except ValueError:
                                # 如果日期格式不正确，记录调试信息
                                debug_info.append(
                                    f"Skipping file with invalid date format: {file_name}")
                                continue
            # 将调试信息添加到 changelog_data 中
            # changelog_data.append({"debug_info": debug_info})
            # 保存到 YAML 文件
            with open('docs/changelog.yml', 'w', encoding='utf-8') as yaml_file:
                yaml.dump(changelog_data, yaml_file, allow_unicode=True,
                          default_flow_style=False, sort_keys=False)
            return f"## Timeline "  # "Changelog YAML generated successfully."
        except Exception as e:
            # 记录错误信息
            # changelog_data.append({"error": f"Error generating changelog YAML: {e}"})
            # # 保存到 YAML 文件
            # with open('docs/changelog.yml', 'w', encoding='utf-8') as yaml_file:
            #     yaml.dump(changelog_data, yaml_file, allow_unicode=True, default_flow_style=False)
            return f"Error generating changelog YAML: {e}"

    @env.macro
    def generate_changelog_yaml_for_subfolder(subfolder_name):
        """生成指定次级文件夹中符合 changelog 插件格式的 YAML 内容，并添加到 changelog.yml 文件中。"""
        changelog_data = []  # 用于存储新的 changelog 数据
        debug_info = []  # 用于存储调试信息
        try:
            # 构建次级文件夹的完整路径
            subfolder_path = os.path.join('docs', subfolder_name)
            if os.path.isdir(subfolder_path):  # 检查路径是否为目录
                # 遍历次级文件夹下所有的以 yymdd- 开头的 md 文件
                for file_name in os.listdir(subfolder_path):
                    if file_name.endswith('.md') and re.match(r'^\d{6}-', file_name):
                        # 构建文件的完整路径
                        full_path = os.path.join(subfolder_path, file_name)
                        # 从文件名中提取日期
                        date_str = file_name.split('-')[0]
                        try:
                            # 将日期字符串转换为日期对象
                            date_obj = datetime.datetime.strptime(
                                date_str, "%y%m%d")
                            # 将日期对象转换为可读格式
                            readable_time = date_obj.strftime("%Y-%m-%d")
                            # 查找或创建日期条目
                            found = False
                            for entry in changelog_data:
                                if readable_time in entry:  # 如果找到日期条目
                                    found = True
                                    entry[readable_time].append({
                                        "newpage": {
                                            "text": f" [ {subfolder_name.replace('_', '')} ] > {'-'.join(file_name.split('-')[1:]).replace('.md', '')}",
                                            "href": f"/sagi_database/{subfolder_name}/{file_name.replace('.md', '')}"
                                        }
                                    })
                                    break
                            # 如果没有找到日期条目，则创建新的
                            if not found:
                                changelog_data.append({
                                    readable_time: [{
                                        "newpage": {
                                            "text": f" [ {subfolder_name.replace('_', '')} ] > {'-'.join(file_name.split('-')[1:]).replace('.md', '')}",
                                            "href": f"/sagi_database/{subfolder_name}/{file_name.replace('.md', '')}"
                                        }
                                    }]
                                })
                            # 对日期条目进行降序排序
                            changelog_data = sorted(
                                changelog_data, key=lambda x: list(x.keys())[0], reverse=True)
                        except ValueError:
                            # 如果日期格式不正确，记录调试信息
                            debug_info.append(
                                f"Skipping file with invalid date format: {file_name}")
                            continue
            else:
                return f"Error: {subfolder_name} is not a valid directory."

            # 读取现有的 changelog.yml 文件
            changelog_file_path = 'docs/changelog.yml'
            if os.path.exists(changelog_file_path):
                with open(changelog_file_path, 'r', encoding='utf-8') as yaml_file:
                    existing_data = yaml.load(
                        yaml_file, Loader=yaml.FullLoader) or []
            else:
                existing_data = []

            # 添加新的次级文件夹条目
            new_entry = {subfolder_name: changelog_data}
            existing_data.append(new_entry)

            # 保存合并后的数据到 changelog.yml 文件
            with open(changelog_file_path, 'w', encoding='utf-8') as yaml_file:
                yaml.dump(existing_data, yaml_file, allow_unicode=True,
                          default_flow_style=False, sort_keys=False)

            # "Changelog YAML updated successfully for {subfolder_name}."
            return f"## Timeline "
        except Exception as e:
            return f"Error generating changelog YAML for {subfolder_name}: {e}"

    @env.macro
    def read_changelog_yaml(file_path):
        """读取 YAML 文件并处理可能的编码问题。"""
        try:
            with open(file_path, 'r', encoding='utf-8') as yaml_file:
                return yaml.load(yaml_file, Loader=yaml.FullLoader)
        except UnicodeDecodeError:
            with open(file_path, 'rb') as yaml_file:
                content = yaml_file.read()
                return yaml.load(content.decode('utf-8', errors='ignore'), Loader=yaml.FullLoader)

    # 注册宏
    env.macro(generate_changelog_yaml)
    env.macro(list_md_files)
    env.macro(generate_grid_cards)
    env.macro(generate_changelog_yaml_for_subfolder)
