import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

class MarkupRenderer:
    def __init__(self, root):
        self.root = root
        self.root.title("增强版自定义标记语言渲染器")
        self.root.geometry("1000x700")
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建左右分栏
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 左侧代码编辑区
        self.code_frame = ttk.Frame(self.paned_window, width=500)
        self.paned_window.add(self.code_frame, weight=1)
        
        # 右侧预览区
        self.preview_frame = ttk.Frame(self.paned_window, width=500)
        self.paned_window.add(self.preview_frame, weight=1)
        
        # 设置代码编辑器
        self.setup_code_editor()
        
        # 初始渲染区域
        self.render_frame = None
        self.clear_preview()
        
        # 设置底部控制按钮
        self.setup_bottom_controls()

    def setup_code_editor(self):
        """设置代码编辑区域"""
        ttk.Label(self.code_frame, text="自定义标记语言代码:").pack(anchor=tk.W, pady=(0, 5))
        
        self.code_editor = scrolledtext.ScrolledText(
            self.code_frame, wrap=tk.WORD, font=("Consolas", 10)
        )
        self.code_editor.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 示例代码
        example_code = """<window title="示例界面" width="400" height="300">
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
        <button text="测试命令" command="test_command" />
    </frame>
</window>"""
        self.code_editor.insert(tk.INSERT, example_code)

    def setup_bottom_controls(self):
        """设置底部控制按钮"""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 左侧按钮组
        button_group = ttk.Frame(control_frame)
        button_group.pack(side=tk.LEFT)
        
        ttk.Button(button_group, text="渲染", command=self.render_markup).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_group, text="清空代码", command=self.clear_code).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_group, text="清空预览", command=self.clear_preview).pack(side=tk.LEFT, padx=5)
        
        # XML解析器复选框
        self.xml_parser_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="使用XML解析器", variable=self.xml_parser_var).pack(side=tk.LEFT, padx=10)
        
        # 状态标签（右侧）
        self.status_label = ttk.Label(control_frame, text="就绪")
        self.status_label.pack(side=tk.RIGHT, padx=5)

    def clear_code(self):
        """清空代码编辑区"""
        self.code_editor.delete("1.0", tk.END)
        self.status_label.config(text="代码已清空", foreground="blue")

    def clear_preview(self):
        """清空预览区"""
        # 销毁现有渲染内容
        if self.render_frame:
            self.render_frame.destroy()
            
        # 创建新的渲染框架
        self.render_frame = ttk.Frame(self.preview_frame)
        self.render_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 重置变量和控件引用
        self.widgets = {}
        self.variables = {}  # 正确的变量名
        
        ttk.Label(self.render_frame, text="渲染结果将显示在这里", foreground="gray").pack(pady=20)
        self.status_label.config(text="预览已清空", foreground="blue")

    def render_markup(self):
        """解析并渲染标记语言"""
        try:
            # 清空预览区
            self.clear_preview()
            
            # 获取代码
            markup_code = self.code_editor.get("1.0", tk.END).strip()
            if not markup_code:
                self.status_label.config(text="错误：代码为空", foreground="red")
                return
                
            # 检查是否使用XML解析器
            if self.xml_parser_var.get():
                # 解析XML
                root_element = ET.fromstring(markup_code)
                
                # 检查根元素是否为window
                if root_element.tag != "window":
                    raise ValueError("根元素必须是window")
                    
                # 处理window属性
                window_title = root_element.get("title", "自定义界面")
                window_width = root_element.get("width", "400")
                window_height = root_element.get("height", "300")
                
                # 创建窗口容器标题
                ttk.Label(self.render_frame, text=window_title, font=("Arial", 12, "bold")).pack(anchor=tk.CENTER, pady=10)
                
                # 创建窗口容器
                window_frame = ttk.Frame(self.render_frame, relief=tk.SUNKEN, padding=10)
                window_frame.pack(fill=tk.BOTH, expand=True)
                window_frame.config(width=window_width, height=window_height)
                
                # 递归渲染子元素
                self.render_element(root_element, window_frame)
                
                self.status_label.config(text="渲染成功", foreground="green")
            else:
                # 非XML解析器模式
                ttk.Label(self.render_frame, text="使用非XML解析器模式", foreground="blue").pack(pady=20)
                self.status_label.config(text="已使用非XML解析器渲染", foreground="green")
                
        except ParseError as e:
            self.status_label.config(text=f"XML解析错误: {str(e)}", foreground="red")
            messagebox.showerror("解析错误", f"XML格式错误:\n{str(e)}")
        except Exception as e:
            self.status_label.config(text=f"错误: {str(e)}", foreground="red")
            messagebox.showerror("错误", f"渲染失败:\n{str(e)}")

    def render_element(self, element, parent):
        """递归渲染元素"""
        tag = element.tag
        attrs = element.attrib
        
        # 根据标签类型创建相应的Tkinter控件
        if tag == "window":
            # 已经处理过window元素，只渲染其子元素
            for child in element:
                self.render_element(child, parent)
                
        elif tag == "label":
            text = attrs.get("text", "")
            font = attrs.get("font", "")
            label = ttk.Label(parent, text=text)
            if font:
                try:
                    # 解析字体设置，如"Arial 14 bold"
                    font_parts = font.split()
                    family = font_parts[0]
                    size = int(font_parts[1]) if len(font_parts) > 1 else 10
                    weight = "bold" if "bold" in font_parts else "normal"
                    slant = "italic" if "italic" in font_parts else "roman"
                    label.config(font=(family, size, weight, slant))
                except:
                    pass
            label.pack(anchor=tk.W, padx=attrs.get("padx", 0), pady=attrs.get("pady", 5))
            if "id" in attrs:
                self.widgets[attrs["id"]] = label
                
        elif tag == "separator":
            orient = attrs.get("orient", "horizontal")
            separator = ttk.Separator(parent, orient=orient)
            separator.pack(fill=tk.X if orient == "horizontal" else tk.Y, 
                          padx=attrs.get("padx", 0), pady=attrs.get("pady", 5))
            if "id" in attrs:
                self.widgets[attrs["id"]] = separator
                
        elif tag == "frame":
            layout = attrs.get("layout", "vertical")
            frame = ttk.Frame(parent)
            
            # 根据布局设置pack方式
            if layout == "horizontal":
                frame.pack(fill=tk.X, padx=attrs.get("padx", 0), pady=attrs.get("pady", 0))
            else:  # vertical
                frame.pack(fill=tk.X, padx=attrs.get("padx", 0), pady=attrs.get("pady", 0))
                
            # 渲染子元素
            for child in element:
                self.render_element(child, frame)
                
            if "id" in attrs:
                self.widgets[attrs["id"]] = frame
                
        elif tag == "entry":
            width = attrs.get("width", 20)
            entry = ttk.Entry(parent, width=width)
            entry.pack(side=tk.LEFT, padx=attrs.get("padx", 2), pady=attrs.get("pady", 0))
            if "id" in attrs:
                self.widgets[attrs["id"]] = entry
                
        elif tag == "radio":
            text = attrs.get("text", "")
            variable = attrs.get("variable", "")
            value = attrs.get("value", "")
            
            # 确保变量存在（修复变量名拼写错误）
            if variable not in self.variables:
                self.variables[variable] = tk.StringVar()
                
            radio = ttk.Radiobutton(parent, text=text, 
                                   variable=self.variables[variable], 
                                   value=value)
            radio.pack(side=tk.LEFT, padx=attrs.get("padx", 2), pady=attrs.get("pady", 0))
            if "id" in attrs:
                self.widgets[attrs["id"]] = radio
                
        elif tag == "checkbox":
            text = attrs.get("text", "")
            variable = attrs.get("variable", "")
            
            # 确保变量存在（修复变量名拼写错误）
            if variable not in self.variables:
                self.variables[variable] = tk.BooleanVar()
                
            checkbox = ttk.Checkbutton(parent, text=text, 
                                      variable=self.variables[variable])
            checkbox.pack(side=tk.LEFT, padx=attrs.get("padx", 2), pady=attrs.get("pady", 0))
            if "id" in attrs:
                self.widgets[attrs["id"]] = checkbox
                
        elif tag == "combobox":
            width = attrs.get("width", 20)
            values = attrs.get("values", "").split(",")
            
            combobox = ttk.Combobox(parent, width=width, values=values)
            combobox.pack(side=tk.LEFT, padx=attrs.get("padx", 2), pady=attrs.get("pady", 0))
            if "id" in attrs:
                self.widgets[attrs["id"]] = combobox
                
        elif tag == "text":
            width = attrs.get("width", 50)
            height = attrs.get("height", 5)
            text_widget = scrolledtext.ScrolledText(parent, width=width, height=height, wrap=tk.WORD)
            text_widget.pack(fill=tk.X, padx=attrs.get("padx", 0), pady=attrs.get("pady", 5))
            if "id" in attrs:
                self.widgets[attrs["id"]] = text_widget
                
        elif tag == "button":
            text = attrs.get("text", "按钮")
            command = attrs.get("command", "")
            
            # 绑定命令
            btn_command = self.get_command_handler(command)
            button = ttk.Button(parent, text=text, command=btn_command)
            button.pack(side=tk.LEFT, padx=attrs.get("padx", 5), pady=attrs.get("pady", 0))
            if "id" in attrs:
                self.widgets[attrs["id"]] = button

    def get_command_handler(self, command_name):
        """获取命令处理函数"""
        handlers = {
            "show_message": self.show_message,
            "clear_text": self.clear_text,
            "test_command": self.test_command
        }
        return handlers.get(command_name, self.default_command)

    def show_message(self):
        """显示信息命令的处理函数"""
        try:
            # 获取姓名
            name = self.widgets["name_entry"].get() if "name_entry" in self.widgets else "未知"
            
            # 获取性别（修复变量名拼写错误）
            gender = self.variables["gender"].get() if "gender" in self.variables else ""
            gender_text = "男" if gender == "male" else "女" if gender == "female" else "未选择"
            
            # 获取爱好（修复变量名拼写错误）
            hobbies = []
            if "hobby_read" in self.variables and self.variables["hobby_read"].get():
                hobbies.append("阅读")
            if "hobby_sport" in self.variables and self.variables["hobby_sport"].get():
                hobbies.append("运动")
            if "hobby_code" in self.variables and self.variables["hobby_code"].get():
                hobbies.append("编程")
            hobby_text = ", ".join(hobbies) if hobbies else "未选择"
            
            # 获取职业
            job = self.widgets["job"].get() if "job" in self.widgets else "未选择"
            
            # 构建信息文本
            info = f"姓名：{name}\n性别：{gender_text}\n爱好：{hobby_text}\n职业：{job}"
            
            # 显示在文本框中
            if "info_text" in self.widgets:
                self.widgets["info_text"].delete("1.0", tk.END)
                self.widgets["info_text"].insert(tk.INSERT, info)
                
        except Exception as e:
            messagebox.showerror("错误", f"执行命令失败:\n{str(e)}")

    def clear_text(self):
        """清空文本命令的处理函数"""
        if "info_text" in self.widgets:
            self.widgets["info_text"].delete("1.0", tk.END)
        if "name_entry" in self.widgets:
            self.widgets["name_entry"].delete(0, tk.END)
        self.status_label.config(text="文本已清空", foreground="blue")

    def test_command(self):
        """测试命令处理函数"""
        messagebox.showinfo("测试命令", "这是一个测试命令按钮，功能可以自定义扩展")
        self.status_label.config(text="测试命令已执行", foreground="blue")

    def default_command(self):
        """默认命令处理函数"""
        messagebox.showinfo("提示", "该命令尚未实现")

if __name__ == "__main__":
    root = tk.Tk()
    app = MarkupRenderer(root)
    root.mainloop()
