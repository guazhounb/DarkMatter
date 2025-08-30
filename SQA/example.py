import tkinter as tk
from tkinter import ttk, scrolledtext
import re
from xml.etree.ElementTree import Element, SubElement

class MarkupParser:
    """解析类似HTML的自定义标记语言"""
    
    def __init__(self):
        # 定义支持的标签和它们对应的Tkinter组件
        self.supported_tags = {
            'window': ttk.Frame,
            'frame': ttk.Frame,
            'label': ttk.Label,
            'button': ttk.Button,
            'entry': ttk.Entry,
            'text': scrolledtext.ScrolledText,
            'checkbox': ttk.Checkbutton,
            'radio': ttk.Radiobutton,
            'combobox': ttk.Combobox,
            'separator': ttk.Separator
        }
        
        # 定义支持的属性 - 新增layout属性支持
        self.supported_attributes = {
            'id': None,
            'text': 'text',
            'width': 'width',
            'height': 'height',
            'bg': 'background',
            'fg': 'foreground',
            'font': 'font',
            'command': None,
            'variable': None,
            'values': None,
            'orient': 'orient',
            'title': None,
            'layout': None,  # 新增：布局方式 horizontal/vertical
            'padx': None,    # 新增：水平间距
            'pady': None     # 新增：垂直间距
        }
        
        # 存储解析后的元素
        self.elements = {}
        
        # 存储变量
        self.variables = {}
        
        # 存储命令回调
        self.commands = {}

    def parse(self, markup_text):
        """解析标记文本并返回根元素"""
        # 简单的标签提取正则表达式
        tag_pattern = re.compile(r'<(\/?)(\w+)([^>]*?)>')
        matches = list(tag_pattern.finditer(markup_text))
        
        if not matches:
            return None
            
        # 创建根元素
        root_tag = matches[0].group(2)
        root_attrs = self._parse_attributes(matches[0].group(3))
        root = Element(root_tag, root_attrs)
        
        # 使用栈来处理嵌套结构
        stack = [root]
        
        # 处理文本内容
        last_pos = matches[0].end()
        
        for i in range(1, len(matches)):
            match = matches[i]
            # 提取标签之间的文本
            text_content = markup_text[last_pos:match.start()].strip()
            if text_content and stack:
                current = stack[-1]
                current.text = text_content
            
            # 处理标签
            closing = match.group(1) == '/'
            tag = match.group(2)
            attrs = self._parse_attributes(match.group(3))
            
            if closing:
                # 关闭标签
                if stack and stack[-1].tag == tag:
                    stack.pop()
            else:
                # 开始标签
                if tag in self.supported_tags:
                    element = SubElement(stack[-1], tag, attrs)
                    stack.append(element)
            
            last_pos = match.end()
        
        return root

    def _parse_attributes(self, attr_str):
        """解析属性字符串为字典"""
        attrs = {}
        if not attr_str:
            return attrs
            
        # 简单的属性解析正则表达式
        attr_pattern = re.compile(r'(\w+)\s*=\s*["\'](.*?)["\']')
        for name, value in attr_pattern.findall(attr_str):
            if name in self.supported_attributes:
                attrs[name] = value
        
        return attrs

    def render(self, root_element, parent=None):
        """将解析后的元素渲染为Tkinter组件"""
        if not root_element:
            return None
            
        tag = root_element.tag
        if tag not in self.supported_tags:
            return None
            
        # 获取属性
        attrs = root_element.attrib
        
        # 创建组件
        component_class = self.supported_tags[tag]
        
        # 准备组件参数
        kwargs = {}
        for attr, tk_attr in self.supported_attributes.items():
            if attr in attrs and tk_attr:
                # 处理特殊类型的属性
                if attr in ['width', 'height', 'padx', 'pady']:
                    kwargs[tk_attr] = int(attrs[attr])
                else:
                    kwargs[tk_attr] = attrs[attr]
        
        # 处理命令
        if 'command' in attrs:
            cmd_name = attrs['command']
            if cmd_name in self.commands:
                kwargs['command'] = self.commands[cmd_name]
        
        # 处理变量
        if 'variable' in attrs:
            var_name = attrs['variable']
            if var_name not in self.variables:
                self.variables[var_name] = tk.StringVar()
            kwargs['variable'] = self.variables[var_name]
        
        # 处理选项值
        if 'values' in attrs and tag == 'combobox':
            kwargs['values'] = attrs['values'].split(',')
        
        # 创建组件实例
        component = component_class(parent, **kwargs)
        
        # 特殊处理window标签
        if tag == 'window':
            # 设置标题作为标签显示
            if 'title' in attrs:
                title_label = ttk.Label(component, text=attrs['title'], font=('Arial', 12, 'bold'))
                title_label.pack(pady=5)
            # 设置内部填充
            component.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # 存储带有ID的组件
        if 'id' in attrs:
            self.elements[attrs['id']] = component
        
        # 设置文本内容（如果有）
        if root_element.text and hasattr(component, 'insert'):
            component.insert(tk.END, root_element.text)
        elif root_element.text and hasattr(component, 'config'):
            component.config(text=root_element.text)
        
        # 获取布局方式和间距
        layout = attrs.get('layout', 'vertical')  # 默认垂直布局
        padx = int(attrs.get('padx', 5))         # 默认水平间距
        pady = int(attrs.get('pady', 5))         # 默认垂直间距
        
        # 渲染子元素 - 根据布局方式设置不同排列
        for child in root_element:
            child_component = self.render(child, component)
            
            # 对frame的子元素进行特殊布局处理
            if tag == 'frame':
                if layout == 'horizontal':
                    # 水平布局：左对齐，带间距
                    child_component.pack(side=tk.LEFT, padx=padx, pady=pady, anchor=tk.W)
                else:
                    # 垂直布局：填充X方向，带间距
                    child_component.pack(fill=tk.X, padx=padx, pady=pady)
        
        # 非window和frame标签的布局
        if tag not in ['window', 'frame']:
            component.pack(fill=tk.X, padx=padx, pady=pady)
        
        return component


class MarkupDemoApp:
    """演示自定义标记语言的应用程序"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("自定义标记语言演示")
        self.root.geometry("800x600")
        
        # 创建解析器实例
        self.parser = MarkupParser()
        self.parser.commands = {
            'show_message': self.show_message,
            'clear_text': self.clear_text
        }
        
        # 创建界面
        self.create_ui()
        
        # 加载示例标记
        self.load_example_markup()
    
    def create_ui(self):
        """创建应用程序界面"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建左侧编辑器
        editor_frame = ttk.LabelFrame(main_frame, text="标记编辑器")
        editor_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.markup_editor = scrolledtext.ScrolledText(editor_frame, width=40, height=25)
        self.markup_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 按钮框架
        button_frame = ttk.Frame(editor_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.render_button = ttk.Button(button_frame, text="渲染界面", command=self.render_markup)
        self.render_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(button_frame, text="清空", command=self.clear_render)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # 创建右侧预览区
        self.preview_frame = ttk.LabelFrame(main_frame, text="界面预览")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 预览容器
        self.container = ttk.Frame(self.preview_frame)
        self.container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def load_example_markup(self):
        """加载示例标记代码 - 添加layout和间距属性"""
        example = """<window title="示例界面" width="400" height="300">
    <label text="欢迎使用自定义标记语言演示" font="Arial 14 bold" />
    <separator orient="horizontal" />
    <label text="请输入您的信息：" />
    <frame layout="horizontal" padx="3" pady="3">
        <label text="姓名：" />
        <entry id="name_entry" width="30" />
    </frame>
    <frame layout="horizontal" padx="3" pady="3">
        <label text="性别：" />
        <radio text="男" variable="gender" value="male" />
        <radio text="女" variable="gender" value="female" />
    </frame>
    <frame layout="horizontal" padx="3" pady="3">
        <label text="爱好：" />
        <checkbox text="阅读" variable="hobby_read" />
        <checkbox text="运动" variable="hobby_sport" />
        <checkbox text="编程" variable="hobby_code" />
    </frame>
    <frame layout="horizontal" padx="3" pady="3">
        <label text="职业：" />
        <combobox id="job" values="学生,教师,工程师,医生,其他" width="20" />
    </frame>
    <text id="info_text" width="50" height="5" />
    <frame layout="horizontal" padx="3" pady="3">
        <button text="显示信息" command="show_message" />
        <button text="清空文本" command="clear_text" />
    </frame>
</window>"""
        
        self.markup_editor.delete(1.0, tk.END)
        self.markup_editor.insert(tk.END, example)
    
    def render_markup(self):
        """渲染标记语言为界面"""
        # 清空预览容器
        self.clear_render()
        
        # 获取标记文本
        markup_text = self.markup_editor.get(1.0, tk.END)
        
        # 解析标记
        root_element = self.parser.parse(markup_text)
        
        if root_element:
            # 渲染界面
            self.parser.render(root_element, self.container)
    
    def clear_render(self):
        """清空预览区域"""
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # 重置解析器状态
        self.parser.elements = {}
        self.parser.variables = {}
    
    def show_message(self):
        """显示信息按钮的回调函数"""
        if 'name_entry' in self.parser.elements:
            name = self.parser.elements['name_entry'].get()
        else:
            name = "未知"
            
        if 'job' in self.parser.elements:
            job = self.parser.elements['job'].get()
        else:
            job = "未知"
        
        # 获取性别信息
        gender = self.parser.variables.get('gender', tk.StringVar(value="未知")).get()
        
        # 获取爱好信息
        hobbies = []
        if self.parser.variables.get('hobby_read', tk.StringVar()).get():
            hobbies.append("阅读")
        if self.parser.variables.get('hobby_sport', tk.StringVar()).get():
            hobbies.append("运动")
        if self.parser.variables.get('hobby_code', tk.StringVar()).get():
            hobbies.append("编程")
        hobby_text = ", ".join(hobbies) if hobbies else "无"
        
        info = f"姓名：{name}\n职业：{job}\n性别：{gender}\n爱好：{hobby_text}"
        
        if 'info_text' in self.parser.elements:
            self.parser.elements['info_text'].delete(1.0, tk.END)
            self.parser.elements['info_text'].insert(tk.END, info)
    
    def clear_text(self):
        """清空文本按钮的回调函数"""
        if 'info_text' in self.parser.elements:
            self.parser.elements['info_text'].delete(1.0, tk.END)
        
        if 'name_entry' in self.parser.elements:
            self.parser.elements['name_entry'].delete(0, tk.END)
        
        # 重置变量
        for var in self.parser.variables.values():
            var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = MarkupDemoApp(root)
    root.mainloop()