一. 通用代码规范

1. 不允许拼音（除人名），统一采用英汉对照表，有更新随时添加;
2. 数据库和源代码采用utf-8编码;
3. 注释必须含有传入参数，返回参数，修改作者，修改日期，复杂功能简要解释;
4. 不建议使用var1,var2,var3等数字连接变量;
5. 建议循环嵌套使用i,ii,k,kk,v,vv 表示循环及层级;
6. 返回值如果为数组，建议在函数名中用单复数体现，如 getElementsByTagName();
7. Git系统中各人在各自的分支上进行修改，Merge合并代码由少数具有高权限的人操作;

二. Python 风格规范

1. 每行不超过80个字符,不使用反斜杠，过长的表达式用()连接 例外: 注释中的Url;
2. 除非是跨行连接，条件语句和返回值不使用();
3. 配置vim tab 为4个空格;
4. 类定义与函数之间空一行;
5. 不要在逗号，分号，冒号前加空格，参数列表，索引或切片左括号不加空格，双目运算福左右各一个空格，赋值=不加空格，函数内多个参数逗号分隔，逗号后面有一个空格;
6. 除外部不可见，非常短小，简单明了的函数以外都应写文档，函数采用_doc_方式写明输入，输出，返回值，异常，复杂算法关键部分写行注释;
7. 类文档写明关键属性;
8. 避免在循环中使用+ /+= 来累加字符串，可采用列表在循环结束后通过 .join 连接;
9. 推荐使用with语句管理文件打开操作，python2.6之前版本需添加 from __future__ import with_statement;
10. 每个导入占一行，顺序为 标准库，第三方库，应用模块;
11. 变量命名避免单字符（除循环，迭代器） 避免包/模块名中使用- ;
12. 尽量避免全局变量，如需要全部大写;
13. 列表推倒禁止多重for语句或过滤器表达式，复杂情况用循环;
14. 生成器中使用yields;
15. 尽可能使用隐式的false, 例如: 使用 if foo: 而不是 if foo != [];
16. 尽量使用内建函数;

三. Python命名约定

1. 所谓”内部(Internal)”表示仅模块内可用, 或者, 在类内是保护或私有的;
2. 用单下划线(_)开头表示模块变量或函数是protected的(使用import * from时不会包含);
3. 用双下划线(__)开头的实例变量或方法表示类内私有;
4. 将相关的类和顶级函数放在同一个模块里. 不像Java, 没必要限制一个类一个模块;
5. 对类名使用大写字母开头的单词(如CapWords, 即Pascal风格), 但是模块名应该用小写加下划线的方式(如lower_with_under.py). 尽管已经有很多现存的模块使用类似于CapWords.py这样的命名, 但现在已经不鼓励这样做, 因为如果模块名碰巧和类名一致, 这会让人困扰;