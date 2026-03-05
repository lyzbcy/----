"""
LeetCode 12. 整数转罗马数字 - 动画演示
使用 matplotlib 手动控制整数转罗马数字的贪心执行过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class IntToRomanAnimation:
    def __init__(self, num):
        self.original_num = num
        self.steps = []
        self.current_step = 0

        # 13 个原子片段对照表（从大到小）
        self.values  = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        self.symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]

        self.code_lines = [
            "int values[]={1000,900,500,400,100,90,50,40,10,9,5,4,1};",
            "char *loma[]={\"M\",\"CM\",\"D\",\"CD\",\"C\",\"XC\",",
            "              \"L\",\"XL\",\"X\",\"IX\",\"V\",\"IV\",\"I\"};",
            "char *result = malloc(20*sizeof(char));",
            "result[0] = '\\0';",
            "int i = 0;",
            "while (num > 0) {",
            "    while (num >= values[i]) {",
            "        strcat(result, loma[i]);",
            "        num -= values[i];",
            "    }",
            "    i++;",
            "}",
            "return result;",
        ]

        self._simulate_algorithm()

        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(15, 9))
        self.fig.canvas.manager.set_window_title('整数转罗马数字 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, 18)
        self.ax.set_ylim(-2, 11)

        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录贪心算法执行的每一步"""
        num = self.original_num
        result_str = ""

        # 初始步骤
        self.steps.append({
            'num': num,
            'result': result_str,
            'table_highlight': None,  # 高亮对照表的哪行
            'action': f'初始化：num = {num}，result = ""，从最大符号 M(1000) 开始贪心匹配',
            'code_highlight': [0, 1, 2, 3, 4, 5],
            'explanations': [
                f'待转换的整数：{num}',
                '预建 13 个原子片段对照表（含 6 个特殊减法组合）。',
                '准备从最大值 M=1000 开始向下贪心匹配。'
            ]
        })

        i = 0
        while num > 0:
            # 记录"尝试当前符号"步骤
            if num >= self.values[i]:
                # 内层循环匹配
                while num >= self.values[i]:
                    old_num = num
                    result_str += self.symbols[i]
                    num -= self.values[i]
                    self.steps.append({
                        'num': num,
                        'result': result_str,
                        'table_highlight': i,
                        'action': (f'num={old_num} >= {self.values[i]}（{self.symbols[i]}）'
                                   f'  →  拼接 "{self.symbols[i]}"，num = {old_num} - {self.values[i]} = {num}'),
                        'code_highlight': [7, 8, 9],
                        'explanations': [
                            f'当前索引 i={i}，符号：{self.symbols[i]}，值：{self.values[i]}',
                            f'num = {old_num} ≥ {self.values[i]}，满足条件。',
                            f'拼接 "{self.symbols[i]}" 到结果，num 减去 {self.values[i]}，剩余 {num}。'
                        ]
                    })
                # 内层循环结束，推进 i
                if num > 0:
                    self.steps.append({
                        'num': num,
                        'result': result_str,
                        'table_highlight': i,
                        'action': (f'num={num} < {self.values[i]}（{self.symbols[i]}），当前档位用完，'
                                   f'i 推进到下一档 {self.symbols[i+1] if i+1 < 13 else "结束"}'),
                        'code_highlight': [10, 11],
                        'explanations': [
                            f'num = {num} 已经不满足 ≥ {self.values[i]}，',
                            f'内层 while 退出，i 从 {i} 推进到 {i+1}。',
                            '继续外层 while，切换到下一个符号档位。'
                        ]
                    })
                i += 1
            else:
                # 直接跳过
                self.steps.append({
                    'num': num,
                    'result': result_str,
                    'table_highlight': i,
                    'action': (f'num={num} < {self.values[i]}（{self.symbols[i]}），跳过此档，'
                               f'i 推进到 {self.symbols[i+1] if i+1 < 13 else "结束"} 档'),
                    'code_highlight': [7, 11],
                    'explanations': [
                        f'当前索引 i={i}，符号：{self.symbols[i]}，值：{self.values[i]}',
                        f'num = {num} < {self.values[i]}，不满足条件，跳过。',
                        f'i 从 {i} 推进到 {i+1}。'
                    ]
                })
                i += 1

        # 结束步骤
        self.steps.append({
            'num': 0,
            'result': result_str,
            'table_highlight': None,
            'action': f'✅ num = 0，循环结束，返回结果："{result_str}"',
            'code_highlight': [6, 13],
            'explanations': [
                f'所有债已还清，num = 0，外层 while 退出。',
                f'最终罗马数字：{self.original_num} → "{result_str}"'
            ]
        })

    def _draw_table(self, highlight_idx):
        """绘制 13 行对照表"""
        table_x = 0
        table_y_start = 9.8
        row_h = 0.6

        self.ax.text(table_x + 1, table_y_start + 0.3, '值-符号对照表',
                     fontsize=12, fontweight='bold', ha='center',
                     bbox=dict(boxstyle='round', facecolor='thistle', alpha=0.7))

        for idx in range(13):
            y = table_y_start - (idx + 1) * row_h
            color = 'gold' if idx == highlight_idx else 'white'
            # 值列
            self.ax.add_patch(patches.FancyBboxPatch(
                (table_x, y), 1.2, row_h * 0.85,
                boxstyle='round,pad=0.02',
                facecolor=color, edgecolor='gray', linewidth=0.8
            ))
            self.ax.text(table_x + 0.6, y + row_h * 0.4, str(self.values[idx]),
                         ha='center', va='center', fontsize=10,
                         fontweight='bold' if idx == highlight_idx else 'normal')
            # 符号列
            self.ax.add_patch(patches.FancyBboxPatch(
                (table_x + 1.25, y), 0.9, row_h * 0.85,
                boxstyle='round,pad=0.02',
                facecolor=color, edgecolor='gray', linewidth=0.8
            ))
            self.ax.text(table_x + 1.7, y + row_h * 0.4, self.symbols[idx],
                         ha='center', va='center', fontsize=11,
                         color='crimson', fontweight='bold')

    def _draw_result_bar(self, result_str, num):
        """绘制当前结果和剩余 num"""
        # 剩余 num
        self.ax.text(3.5, 8.6, f'剩余 num = {num}', fontsize=15,
                     fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))
        # 已生成结果
        self.ax.text(3.5, 7.7, f'当前结果 = "{result_str}"', fontsize=14,
                     color='darkblue', fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.9))

    def _draw_code_panel(self, step_data):
        start_x = 10.5
        start_y = 9.5
        line_height = 0.52
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 0.4, 'C 代码同步显示', fontsize=12,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=8.5, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.25)
            )

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, 18)
        self.ax.set_ylim(-2, 11)

        step_data = self.steps[step_index]

        # 标题
        self.ax.text(8, 10.6,
                     f'步骤 {step_index + 1}/{len(self.steps)}  |  LeetCode 12. 整数转罗马数字',
                     ha='center', fontsize=15, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        # 动作说明
        self.ax.text(6.5, 9.8, step_data['action'],
                     ha='center', fontsize=11,
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True)

        # 详细解释
        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(6.5, 8.3, explain_text,
                         ha='center', fontsize=10.5,
                         bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True)

        # 操作提示
        self.ax.text(6.5, 6.8,
                     '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出',
                     ha='center', fontsize=10,
                     bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6))

        # 结果和剩余 num
        self._draw_result_bar(step_data['result'], step_data['num'])

        # 对照表
        self._draw_table(step_data['table_highlight'])

        # 代码面板
        self._draw_code_panel(step_data)

        self.fig.canvas.draw()

    def _on_key_press(self, event):
        if event.key in ('right', ' ', 'enter'):
            if self.current_step < len(self.steps) - 1:
                self.current_step += 1
                self._draw_step()
        elif event.key == 'left':
            if self.current_step > 0:
                self.current_step -= 1
                self._draw_step()
        elif event.key == 'home':
            self.current_step = 0
            self._draw_step()
        elif event.key == 'end':
            self.current_step = len(self.steps) - 1
            self._draw_step()
        elif event.key in ('q', 'escape'):
            plt.close(self.fig)

    def show(self):
        self._draw_step(0)
        plt.tight_layout()
        plt.show()


def main():
    print("=" * 60)
    print("LeetCode 12. 整数转罗马数字 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: num=3749 (输出: MMMDCCXLIX)")
    print("2. 示例 2: num=58   (输出: LVIII)")
    print("3. 示例 3: num=1994 (输出: MCMXCIV)")
    print("4. 示例 4: num=4    (输出: IV)")
    print("5. 示例 5: num=3999 (输出: MMMCMXCIX)")
    print("6. 自定义输入")

    choice = input("\n请输入选择 (1-6): ").strip()

    if choice == '1':
        num = 3749
    elif choice == '2':
        num = 58
    elif choice == '3':
        num = 1994
    elif choice == '4':
        num = 4
    elif choice == '5':
        num = 3999
    elif choice == '6':
        num = int(input("请输入整数 (1-3999): ").strip())
    else:
        print("无效选择，使用示例 3")
        num = 1994

    print("\n开始演示...")
    print(f"输入: num = {num}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = IntToRomanAnimation(num)
    anim.show()


if __name__ == '__main__':
    main()
