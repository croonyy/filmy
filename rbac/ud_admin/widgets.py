from django import forms
from django.utils.html import format_html
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.safestring import mark_safe
from pprint import pprint
from django.forms import Media
from django.utils import formats
import json


class AceWidget(forms.Textarea):
    # def test111(self):
    #     print("test")
    script_str = """
    <script>
        $(function () {{
            var textarea = $('#id_{name}');
            var editp = $('<div>', {{
                    position: 'absolute',
                    id:'id_{name}_editor',
                    width: textarea.width(),
                    height: textarea.height(),
                    'class': textarea.attr('class')
                }}).insertBefore(textarea);
                
            textarea.css('display', 'none');    
            
            var editor = ace.edit(editp[0]);
            editor.getSession().setValue(textarea.val());
            editor.getSession().setMode("ace/mode/{mode}");
            editor.setTheme("ace/theme/{theme}");
        
            textarea.closest('form').submit(function () {{
                textarea.val(editor.getSession().getValue());
            }});
        }});
        
        function test_a(dom,id) {{
            editor = ace.edit(id)
            if (dom.checked) {{
                editor.getSession().setUseWrapMode(true)
            }}
            else {{
                editor.getSession().setUseWrapMode(false)
            }}
        }};
    </script>
    
    """
    dom_str = """
    <div style="margin:5px">
        <span>
            <input type="checkbox" name="_selected_action" value="1" 
            onclick="test_a(this,'id_{name}_editor')"
            class="action-select">
            自动换行
        </span>
    </div>
    """

    def __init__(self, mode="", theme="", attrs=None):
        """
        为了能在调用的时候自定义代码类型和样式
        :param mode:
        :param theme:
        :param attrs:
        :return:
        """
        default_attrs = {"cols": "150", "rows": "30"}
        if attrs:
            default_attrs.update(attrs)
        self.mode = mode or 'python'
        self.theme = theme or 'dracula'
        super().__init__(default_attrs)

        # setattr(attrs, attrs.get['cols'] or 100)
        # setattr(attrs, attrs.get['rows'] or 20)
        # attrs['rows'] = attrs.get['rows'] or 20

    # @property
    # def media(self):
    #     return vendor()

    @property
    def media(self):
        return forms.Media(
            css={
                # "all": ["pretty.css"],
            },
            js=[
                # "/static/vendors/jquery/jquery-2.2.4.min.js",
                "/static/vendors/ace_editor/src_min/ace.js",
                f"/static/vendors/ace_editor/src_min/mode-{self.mode}.js",
                f"/static/vendors/ace_editor/src_min/theme-{self.theme}.js",
                # "/static/vendors/ace_editor/src_min/mode-html.js",
                # "/static/vendors/ace_editor/src_min/mode-javascript.js",
                # "/static/vendors/ace_editor/src_min/mode-json.js",
                # "/static/vendors/ace_editor/src_min/mode-python.js",
                # "/static/vendors/ace_editor/src_min/mode-sh.js",
                # "/static/vendors/ace_editor/src_min/mode-sql.js",
                # "/static/vendors/ace_editor/src_min/theme-dawn.js",
                # "/static/vendors/ace_editor/src_min/theme-dracula.js",
                # "/static/vendors/ace_editor/src_min/theme-dreamweaver.js",
                # "/static/vendors/ace_editor/src_min/theme-eclipse.js",
                # "/static/vendors/ace_editor/src_min/theme-github.js",
                # "/static/vendors/ace_editor/src_min/theme-god.js",
                # "/static/vendors/ace_editor/src_min/theme-iplastic.js",
                # "/static/vendors/ace_editor/src_min/theme-twilight.js",
                # "/static/vendors/ace_editor/src_min/theme-xcode.js",
                # "/static/vendors/ace_editor/src_min/theme-xcode.js",
                # "/static/ud_admin/test.js",
            ]
        )

    def render(self, name, value, attrs=None, renderer=None):
        """
        关键方法
        :param name:
        :param value:
        :param attrs:
        :return:
        """
        context = self.get_context(name, value, attrs)
        attrs = context['widget']['attrs']
        attrs['name'] = name
        # flatatt(attrs) 生成dom属性部分的字符串
        # <textarea name="code"  cols="100" id="id_code" rows="20" required>aaa</textarea>
        textarea = f"""<textarea {flatatt(attrs)}>{self.format_value(value)}</textarea>"""
        script_str = self.script_str.format(name=name, mode=self.mode, theme=self.theme)
        html_ = f"{script_str}{self.dom_str.format(name=name)}{textarea}"
        return mark_safe(html_)

    def format_value(self, value):
        try:
            if self.mode.lower() == 'json':
                value = json.dumps(json.loads(value), indent=2,
                                   ensure_ascii=False, sort_keys=True)
            # these lines will try to adjust size of TextArea to fit to content
            # row_lengths = [len(r) for r in value.split('\n')]
            # self.attrs['rows'] = min(max(len(row_lengths) + 2, 10), 30)
            # self.attrs['cols'] = min(max(max(row_lengths) + 2, 40), 120)
            # print(f"format_value:{type(value)}:{value}")
            if value == 'null':
                return ""
            if value:
                return value
            else:
                return ''
        except Exception as e:
            print("*" * 80, e)
            # logger.warning("Error while formatting JSON: {}".format(e))
            # if value == "" or value is None:
            #     return None
            if value is None:
                return ""
            if self.is_localized:
                return formats.localize_input(value)
            return str(value)


class JsonWidget(forms.JSONField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
