import xml.etree.ElementTree as ET
import os

PAPER_INPUT_DIR = "paper_input"
PAPER_OUTPUT_DIR = "paper_output"

def extract_edition_lines(xml_file):
    try:
        # 解析 XML 文件
        print(f"Processing file: {xml_file}")
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # 定义命名空间，以匹配带有命名空间的 XML 节点
        namespace = {'wok': 'http://clarivate.com/schema/wok5.30/public/FullRecord'}
        
        # 创建或覆盖输出文件
        # with open(os.path.join(os.getcwd(), PAPER_OUTPUT_DIR, "example.txt"), 'w', encoding='utf-8') as file:
            # 查找所有 <edition> 节点，并检查是否包含 value="WOS.ISTP"
        found = False
        for ewuid in root.findall(".//wok:EWUID", namespace):
                # 获取该 <EWUID> 节点下的所有 <edition>
                editions = ewuid.findall("wok:edition", namespace)

                # 检查是否只有一个 <edition>，且该 <edition> 的值为 "WOS.ISTP"
                if len(editions) == 1 and editions[0].get('value') == "WOS.ESCI":
                    # 将符合条件的 EWUID 节点写入文件
                    # print(f"Processing file: {xml_file}")
                    found = True
            
        if not found:
            print(f"未找到包含 value=\"WOS.ISTP\" 的 <edition> 节点。")

    except ET.ParseError as e:
        print(f"解析 XML 文件时出错: {e}")
    except FileNotFoundError:
        print(f"文件 {xml_file} 未找到。")
    except Exception as e:
        print(f"发生错误: {e}")

# 替换 'your_file.xml' 为实际 XML 文件路径，'example.txt' 为输出文件路径
# extract_edition_lines('your_file.xml', 'example.txt')
def check_doctype_count(file_name):
    try:
        # 加载并解析XML文件
        tree = ET.parse(file_name)
        root = tree.getroot()
        namespace = {'wok': 'http://clarivate.com/schema/wok5.30/public/FullRecord'}
        # 查找`doctypes`标签并获取属性`count`
        doctype_element = root.find('.//wok:doctypes', namespace)  # 假设 `doctypes` 是 XML 文件中独特的标签
        if doctype_element is not None:
            count = int(doctype_element.get('count', 0))  # 获取`count`属性值，默认为0
            if count > 1:
                print(f"文件 {file_name} 的 count 值大于 1: {count}")
            # else:
            #     print(f"文件 {file_name} 的 count 值小于或等于 1: {count}")
        else:
            print(f"文件 {file_name} 中没有找到 <doctypes> 标签。")
    except ET.ParseError as e:
        print(f"无法解析文件：{file_name}. 错误: {e}")
    except Exception as e:
        print(f"处理文件时发生错误：{file_name}. 错误: {e}")

def load_paper_input_dir(dir_path: str, load_proc):
    for dir_v in os.listdir(dir_path):
        dir_tmp = os.path.join(dir_path, dir_v)
        if os.path.isdir(dir_tmp):
            # 说明还是目录，那么继续遍历目录
            load_paper_input_dir(dir_tmp, load_proc)
        else:
            load_proc(dir_tmp)
    pass

def load_paper_input(load_proc, paper_input_dir):
    # 先遍历目录，找到所有的文件名
    paper_input_path = os.path.join(os.getcwd(), paper_input_dir)
    load_paper_input_dir(paper_input_path, load_proc)
    pass
#
if __name__ == '__main__':
    load_paper_input(check_doctype_count, PAPER_INPUT_DIR)
    pass