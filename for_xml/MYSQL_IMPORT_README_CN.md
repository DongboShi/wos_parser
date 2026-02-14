# MySQL/MariaDB 数据库导入说明

此脚本用于将 WOS XML 解析器生成的 CSV 文件导入到 MySQL 或 MariaDB 数据库中。

## 系统要求

1. **数据库服务器**：MySQL 5.7+ 或 MariaDB 10.3+
   - **Linux Debian 用户**：MariaDB 是默认的 SQL 服务器，完全支持
   - **其他 Linux 发行版**：MySQL 和 MariaDB 都支持

2. **Python 包**：安装 `pymysql` 包（兼容 MySQL 和 MariaDB）：
   ```bash
   pip install pymysql
   ```
   
   或者使用 `mysqlclient`（在 Linux 上对 MariaDB 有更好的原生支持）：
   ```bash
   pip install mysqlclient
   ```

## 快速开始

### 1. 生成 CSV 文件

首先运行 XML 解析器生成 CSV 文件：

```bash
cd for_xml
python xml_proc_main.py 你的XML文件路径/
```

这将在 `xml_output` 目录中生成 33 个 CSV 文件。

### 2. 导入到 MySQL/MariaDB

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
- 自动检测您使用的是 MySQL 还是 MariaDB
- 创建名为 `wos_xml` 的数据库
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
| `--host` | MySQL/MariaDB 服务器地址 | localhost |
| `--user` | MySQL/MariaDB 用户名 | root |
| `--password` | MySQL/MariaDB 密码 | (空) |
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

如果遇到连接错误：

**对于 MySQL：**
```bash
sudo systemctl status mysql
```

**对于 MariaDB（Debian/Ubuntu 默认）：**
```bash
sudo systemctl status mariadb
# 或
sudo systemctl status mysql  # mysql 命令也适用于 MariaDB
```

### 权限错误

授予必要的权限（MySQL 和 MariaDB 语法相同）：
```sql
GRANT ALL PRIVILEGES ON wos_xml.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

### MariaDB 特别说明

1. **默认认证方式**：在 Debian/Ubuntu 上，MariaDB 的 root 用户可能使用 unix_socket 认证：
   ```bash
   # 无需密码连接（使用 unix_socket 时）
   sudo mariadb
   
   # 创建使用密码认证的用户
   CREATE USER 'wos_user'@'localhost' IDENTIFIED BY 'password';
   GRANT ALL PRIVILEGES ON wos_xml.* TO 'wos_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **兼容性**：导入脚本自动检测并兼容 MySQL 和 MariaDB
   - MariaDB 是 MySQL 的替代品
   - 所有 SQL 语法都兼容两种系统
   - 脚本会在连接时显示检测到的数据库类型

### 大数据集

对于大数据集：
- 考虑增加 MySQL/MariaDB 的 `max_allowed_packet` 设置
- 在导入期间监控磁盘空间
- 脚本会显示每个表的导入进度

**MySQL 配置：**
```ini
# /etc/mysql/my.cnf
[mysqld]
max_allowed_packet=256M
```

**MariaDB 配置：**
```ini
# /etc/mysql/mariadb.conf.d/50-server.cnf
[mysqld]
max_allowed_packet=256M
```

## 安全注意事项

1. 不要在命令行中直接使用 `--password` 参数（生产环境）
2. 创建专用的数据库用户，只授予必要的权限
3. 谨慎使用 `--drop-existing` 参数，它会永久删除数据

## 兼容性说明

导入脚本完全兼容 MySQL 和 MariaDB：
- **测试版本**：MySQL 5.7+, MySQL 8.0+, MariaDB 10.3+, MariaDB 10.5+, MariaDB 10.11+
- **字符编码**：utf8mb4 Unicode 编码（支持所有国际字符）
- **SQL 语法**：使用两种数据库系统都兼容的标准 SQL
- **自动检测**：脚本自动检测您使用的数据库服务器类型
- **Python 库**：支持 `pymysql` 和 `mysqlclient` 两种 Python 包

## 支持

如有问题，请查看：
- 主 README.md 文件
- tables.md 文件了解详细的表结构
- MySQL 错误日志：`/var/log/mysql/error.log`
