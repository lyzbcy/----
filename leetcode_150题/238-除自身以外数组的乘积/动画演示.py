"""
LeetCode 238. 除自身以外数组的乘积 - 两趟乘积动画
使用 matplotlib 手动观察前缀积与后缀积的填表过程
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ProductExceptSelfAnimation:
    def __init__(self, nums):
        self.nums = nums.copy()
        self.length = len(nums)
        self.answer = [1] * self.length
        self.steps = []
        self.current_step = 0
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 15
        self.code_lines = [
            "int* productExceptSelf(int* nums, int numsSize, int* returnSize) {",
            "    int* answer = malloc(sizeof(int) * numsSize);",
            "    int prefix = 1;",
            "    for (int i = 0; i < numsSize; i++) {",
            "        answer[i] = prefix;",
            "        prefix *= nums[i];",
            "    }",
            "    int suffix = 1;",
            "    for (int i = numsSize - 1; i >= 0; i--) {",
            "        answer[i] *= suffix;",
            "        suffix *= nums[i];",
            "    }",
            "    *returnSize = numsSize;",
            "    return answer;",
            "}",
        ]

        self._simulate_algorithm()

        self.fig, self.ax = plt.subplots(figsize=(14, 9))
        self.fig.canvas.manager.set_window_title('除自身以外数组的乘积 - 动画演示（手动控制）')
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录前缀、后缀两趟扫描的每一步"""
        prefix_written = [False] * self.length
        finalized = [False] * self.length

        self.steps.append({
            'phase': 'init',
            'index': None,
            'nums': self.nums.copy(),
            'answer': self.answer.copy(),
            'prefix_value': 1,
            'suffix_value': 1,
            'prefix_written': prefix_written.copy(),
            'finalized': finalized.copy(),
            'action': '初始化：answer 全部设为 1，prefix=suffix=1，准备开始两趟扫描',
            'code_highlight': [0, 1, 2],
            'explanations': [
                '输出数组可以用于暂存前缀积，因此先全部设为 1。',
                'prefix 表示当前位置左边所有元素的乘积。',
                'suffix 将在第二趟从右往左累乘。'
            ]
        })

        prefix = 1
        for i in range(self.length):
            used_prefix = prefix
            self.answer[i] = used_prefix
            prefix_written[i] = True
            self.steps.append({
                'phase': 'prefix',
                'index': i,
                'nums': self.nums.copy(),
                'answer': self.answer.copy(),
                'prefix_value': used_prefix,
                'suffix_value': None,
                'prefix_written': prefix_written.copy(),
                'finalized': finalized.copy(),
                'action': (f'前缀阶段：answer[{i}] 记录左侧乘积 {used_prefix}，'
                           f'随后 prefix *= nums[{i}] = {self.nums[i]}'),
                'code_highlight': [2, 3, 4, 5],
                'explanations': [
                    f'answer[{i}] 先写入左边乘积 {used_prefix}。',
                    f'更新 prefix = {used_prefix} × {self.nums[i]} = {used_prefix * self.nums[i]}，'
                    '供下一格使用。'
                ]
            })
            prefix *= self.nums[i]

        suffix = 1
        for i in range(self.length - 1, -1, -1):
            used_suffix = suffix
            self.answer[i] *= used_suffix
            finalized[i] = True
            explanations = [
                f'answer[{i}] 原有前缀积为 {self.steps[-1]["answer"][i] if self.steps else 1}，'
                f'乘上右侧乘积 {used_suffix} 得到最终值 {self.answer[i]}。',
                f'suffix 更新为 {used_suffix} × nums[{i}] = {used_suffix * self.nums[i]}，'
                '为左侧元素准备。'
            ]
            self.steps.append({
                'phase': 'suffix',
                'index': i,
                'nums': self.nums.copy(),
                'answer': self.answer.copy(),
                'prefix_value': None,
                'suffix_value': used_suffix,
                'prefix_written': prefix_written.copy(),
                'finalized': finalized.copy(),
                'action': (f'后缀阶段：answer[{i}] 乘上右侧乘积 {used_suffix}，'
                           f'并将 suffix *= nums[{i}] = {self.nums[i]}'),
                'code_highlight': [7, 8, 9, 10],
                'explanations': explanations
            })
            suffix *= self.nums[i]

        self.steps.append({
            'phase': 'done',
            'index': None,
            'nums': self.nums.copy(),
            'answer': self.answer.copy(),
            'prefix_value': None,
            'suffix_value': None,
            'prefix_written': [True] * self.length,
            'finalized': [True] * self.length,
            'action': f'✅ 完成：answer = {self.answer}',
            'code_highlight': [11, 12, 13],
            'explanations': [
                '所有元素都经过前缀和后缀阶段，answer 即为最终结果。',
                '返回前别忘了设置 *returnSize = numsSize（C 版本）。'
            ]
        })

    def _draw_arrays(self, step_data):
        nums = step_data['nums']
        answer = step_data['answer']

        for idx in range(self.length):
            # nums 行
            rect = patches.Rectangle(
                (idx - 0.45, 2 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor='lightgray'
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 2, str(nums[idx]), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, 2.8, f'nums[{idx}]', ha='center', fontsize=10, color='gray')

            # answer 行
            if step_data['finalized'][idx]:
                face = 'lightgreen'
            elif step_data['prefix_written'][idx]:
                face = 'lightblue'
            else:
                face = 'whitesmoke'
            rect = patches.Rectangle(
                (idx - 0.45, 0 - 0.45), 0.9, 0.9,
                linewidth=2, edgecolor='black', facecolor=face
            )
            self.ax.add_patch(rect)
            self.ax.text(idx, 0, str(answer[idx]), ha='center', va='center',
                         fontsize=14, fontweight='bold')
            self.ax.text(idx, -0.8, f'answer[{idx}]', ha='center',
                         fontsize=10, color='gray')

        # 当前索引高亮
        idx = step_data['index']
        if idx is not None and 0 <= idx < self.length:
            rect = patches.Rectangle(
                (idx - 0.45, 2 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='orange', facecolor='none'
            )
            self.ax.add_patch(rect)
            rect = patches.Rectangle(
                (idx - 0.45, 0 - 0.45), 0.9, 0.9,
                linewidth=3, edgecolor='red', facecolor='none'
            )
            self.ax.add_patch(rect)

    def _draw_status_panel(self, step_data):
        start_y = 4.5
        self.ax.text(-0.5, start_y + 0.5,
                     f'阶段：{self._phase_text(step_data["phase"])}',
                     fontsize=13, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        if step_data['phase'] in ('prefix', 'init'):
            self.ax.text(-0.5, start_y - 0.2,
                         f'prefix = {step_data["prefix_value"] if step_data["prefix_value"] is not None else "待更新"}',
                         fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lavender', alpha=0.8))
        if step_data['phase'] in ('suffix', 'done'):
            label = 'suffix'
            value = step_data["suffix_value"] if step_data["suffix_value"] is not None else '已完成'
            self.ax.text(-0.5, start_y - 0.9,
                         f'{label} = {value}',
                         fontsize=12,
                         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    @staticmethod
    def _phase_text(phase):
        mapping = {
            'init': '初始化',
            'prefix': '前缀阶段',
            'suffix': '后缀阶段',
            'done': '结束'
        }
        return mapping.get(phase, phase)

    def _draw_code_panel(self, step_data):
        start_x = self.visual_width + 1.5
        start_y = 3.5
        line_height = 0.6
        highlight = set(step_data.get('code_highlight', []))

        self.ax.text(start_x, start_y + 2.2, 'C 代码同步显示', fontsize=13,
                     fontweight='bold', ha='left',
                     bbox=dict(boxstyle='round', facecolor='mistyrose', alpha=0.6))

        for idx, line in enumerate(self.code_lines):
            y = start_y - idx * line_height
            facecolor = 'peachpuff' if idx in highlight else 'white'
            self.ax.text(
                start_x, y, f'{idx + 1:02d} {line}',
                ha='left', va='center', fontsize=10, family='monospace',
                bbox=dict(boxstyle='round', facecolor=facecolor, alpha=0.9, pad=0.3)
            )

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index

        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-4, 9)

        step_data = self.steps[step_index]

        self.ax.text(
            max(self.length / 2, 3), 8,
            f'步骤 {step_index + 1}/{len(self.steps)}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8)
        )
        self.ax.text(
            max(self.length / 2, 3), 7.2,
            step_data['action'],
            ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.9), wrap=True
        )

        explanations = step_data.get('explanations', [])
        if explanations:
            explain_text = '\n'.join(f'· {line}' for line in explanations)
            self.ax.text(
                max(self.length / 2, 3), 6.1,
                explain_text,
                ha='center', fontsize=11,
                bbox=dict(boxstyle='round', facecolor='honeydew', alpha=0.9), wrap=True
            )

        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax.text(
            max(self.length / 2, 3), 5,
            controls_text,
            ha='center', fontsize=11,
            bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.6)
        )

        self._draw_status_panel(step_data)
        self._draw_arrays(step_data)
        self._draw_code_panel(step_data)

        legend_items = [
            ('lightblue', '已写入前缀积'),
            ('lightgreen', '前缀+后缀完成'),
            ('whitesmoke', '待处理'),
        ]
        for i, (color, text) in enumerate(legend_items):
            rect = patches.Rectangle((i * 2, -2.5), 0.7, 0.5,
                                     facecolor=color, edgecolor='black')
            self.ax.add_patch(rect)
            self.ax.text(i * 2 + 0.9, -2.25, text, fontsize=10, va='center')

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
    print("LeetCode 238. 除自身以外数组的乘积 - 动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("1. 示例 1: nums=[1,2,3,4]")
    print("2. 仅有一个 0: nums=[-1,1,0,-3,3]")
    print("3. 出现多个 0: nums=[0,2,0,4]")
    print("4. 自定义输入")

    choice = input("\n请输入选择 (1-4): ").strip()

    if choice == '1':
        nums = [1, 2, 3, 4]
    elif choice == '2':
        nums = [-1, 1, 0, -3, 3]
    elif choice == '3':
        nums = [0, 2, 0, 4]
    elif choice == '4':
        nums = list(map(int, input("请输入 nums（空格分隔）: ").split()))
    else:
        print("无效选择，默认使用示例 1")
        nums = [1, 2, 3, 4]

    print("\n开始演示...")
    print(f"nums = {nums}")
    print("\n操作提示：")
    print("  空格 / 右箭头：下一步")
    print("  左箭头       ：上一步")
    print("  Home / End   ：跳转到起点 / 终点")
    print("  Q / Esc      ：退出动画\n")
    print("⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")

    anim = ProductExceptSelfAnimation(nums)
    anim.show()


if __name__ == '__main__':
    main()














