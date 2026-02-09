# MySQL 数据库导入说明

此脚本用于将 WOS XML 解析器生成的 CSV 文件导入到 MySQL 数据库中。

## 快速开始

### 1. 生成 CSV 文件

首先运行 XML 解析器生成 CSV 文件：

```bash
cd for_xml
python xml_proc_main.py 你的XML文件路径/
```

这将在 `xml_output` 目录中生成 33 个 CSV 文件。

### 2. 导入到 MySQL

**方法一：使用便捷脚本（推荐）**

```bash
./import_csv_to_mysql.sh [MySQL密码] [数据库名]
```

例如：
```bash
./import_csv_to_mysql.sh mypassword wos_xml
```

**方法二：使用 Python 脚本**

1. 安装依赖：
   ```bash
   pip install -r requirements_mysql.txt
   ```

2. 运行导入脚本：
   ```bash
   python import_to_mysql.py
   ```

## 功能说明

导入脚本将会：
- 创建名为 `wos_xml` 的 MySQL 数据库
- 创建 33 个数据表，包含完整的表结构和索引
- 从 `xml_output` 目录导入所有 CSV 文件

## 自定义配置

指定数据库连接参数：

```bash
python import_to_mysql.py --host localhost --user root --password 密码 --database 数据库名
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--host` | MySQL 服务器地址 | localhost |
| `--user` | MySQL 用户名 | root |
| `--password` | MySQL 密码 | (空) |
| `--database` | 数据库名称 | wos_xml |
| `--csv-dir` | CSV 文件目录 | xml_output |
| `--drop-existing` | 删除现有数据库（警告：会删除所有数据） | False |

## 数据库结构

脚本会创建 33 个表，分为 6 个部分：

### 第 1 部分：论文基本信息（14 个表）
- `item` - 主要论文元数据
- `item_title` - 论文标题
- `item_abstract` - 论文摘要
- `item_doc_types` - 文档类型
- 等等...

### 第 2 部分：作者信息（12 个表）
- `item_authors` - 作者姓名和详细信息
- `item_addresses` - 作者地址
- `item_orgs` - 组织机构
- 等等...

### 第 3 部分：分类信息（2 个表）
- `item_headings` - 研究领域
- `item_subjects` - 研究主题

### 第 4 部分：参考文献（2 个表）
- `item_references` - 引用的参考文献
- `item_cite_locations` - 引用位置

### 第 5 部分：资助信息（2 个表）
- `item_acks` - 致谢
- `item_grants` - 资助信息

### 第 6 部分：会议信息（1 个表）
- `item_conferences` - 会议详情

## 示例查询

导入完成后，运行示例查询脚本：

```bash
python example_queries.py
```

该脚本演示了 15+ 种常见查询，包括：
- 按年份、国家、机构统计论文
- 作者和引用统计
- 研究主题分析
- 资助和基金信息
- 开放获取统计

## 详细文档

更多详细信息请参阅：
- [MYSQL_IMPORT_GUIDE.md](MYSQL_IMPORT_GUIDE.md) - 完整的导入指南（英文）
- [README.md](README.md) - 项目主文档

## 常见问题

### 连接错误

如果遇到连接错误，检查 MySQL 是否运行：
```bash
sudo systemctl status mysql
```

### 权限错误

授予必要的权限：
```sql
GRANT ALL PRIVILEGES ON wos_xml.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### 大数据集

对于大数据集：
- 考虑增加 MySQL 的 `max_allowed_packet` 设置
- 在导入期间监控磁盘空间
- 脚本会显示每个表的导入进度

## 安全注意事项

1. 不要在命令行中直接使用 `--password` 参数（生产环境）
2. 创建专用的 MySQL 用户，只授予必要的权限
3. 谨慎使用 `--drop-existing` 参数，它会永久删除数据

## 支持

如有问题，请查看：
- 主 README.md 文件
- tables.md 文件了解详细的表结构
- MySQL 错误日志：`/var/log/mysql/error.log`
