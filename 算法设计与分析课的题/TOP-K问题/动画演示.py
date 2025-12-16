"""
TOP K问题 - 快速选择算法动画演示
使用 matplotlib 手动控制算法执行过程

特点：
- 可视化分区过程
- 每一步的详细说明
- 直观展示 pivot 选择和元素交换
"""

import matplotlib.pyplot as plt
import numpy as np
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class QuickSelectAnimation:
    def __init__(self, arr, k):
        self.original_arr = arr.copy()
        self.arr = arr.copy()
        self.k = k  # 1-indexed
        self.n = len(arr)
        self.steps = []
        self.current_step = 0
        
        # 模拟算法
        self._simulate(0, self.n - 1, k - 1)  # 转为0-indexed
        
        # 创建画布
        self.fig, (self.ax_arr, self.ax_info) = plt.subplots(2, 1, figsize=(14, 10),
                                                              gridspec_kw={'height_ratios': [2, 1]})
        self.fig.canvas.manager.set_window_title('TOP K问题 - 快速选择算法动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _simulate(self, left, right, k):
        """模拟快速选择算法"""
        
        if left == right:
            self.steps.append({
                'type': 'found',
                'arr': self.arr.copy(),
                'left': left,
                'right': right,
                'k': k,
                'action': f'找到了！第 {self.k} 小的数是 {self.arr[left]}',
                'detail': {
                    'what': f'区间只剩一个元素 arr[{left}] = {self.arr[left]}',
                    'why': '递归终止条件',
                    'purpose': '返回结果'
                }
            })
            return
        
        # 选择 pivot
        pivot_idx = right
        pivot = self.arr[pivot_idx]
        
        self.steps.append({
            'type': 'select_pivot',
            'arr': self.arr.copy(),
            'left': left,
            'right': right,
            'pivot_idx': pivot_idx,
            'pivot': pivot,
            'k': k,
            'action': f'选择 pivot = arr[{pivot_idx}] = {pivot}',
            'detail': {
                'what': f'选择最右边的元素 {pivot} 作为基准',
                'why': '分区的参考点',
                'purpose': '将数组分成 ≤pivot 和 >pivot 两部分'
            }
        })
        
        # 分区过程
        i = left - 1
        for j in range(left, right):
            if self.arr[j] <= pivot:
                i += 1
                if i != j:
                    self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
                    self.steps.append({
                        'type': 'swap',
                        'arr': self.arr.copy(),
                        'left': left,
                        'right': right,
                        'i': i,
                        'j': j,
                        'pivot_idx': pivot_idx,
                        'k': k,
                        'action': f'交换 arr[{i}] 和 arr[{j}]',
                        'detail': {
                            'what': f'arr[{j}]={self.arr[i]} ≤ pivot，需要移到左边',
                            'why': f'arr[{j}] 比 pivot 小或相等',
                            'purpose': '维护分区不变量'
                        }
                    })
        
        # 将 pivot 放到正确位置
        new_pivot_idx = i + 1
        if new_pivot_idx != right:
            self.arr[new_pivot_idx], self.arr[right] = self.arr[right], self.arr[new_pivot_idx]
        
        self.steps.append({
            'type': 'partition_done',
            'arr': self.arr.copy(),
            'left': left,
            'right': right,
            'pivot_idx': new_pivot_idx,
            'pivot': pivot,
            'k': k,
            'action': f'分区完成！pivot 放到位置 {new_pivot_idx}',
            'detail': {
                'what': f'pivot={pivot} 现在在位置 {new_pivot_idx}',
                'why': '左边都 ≤ pivot，右边都 > pivot',
                'purpose': '判断 k 在哪一边'
            }
        })
        
        # 决定递归方向
        if k == new_pivot_idx:
            self.steps.append({
                'type': 'found',
                'arr': self.arr.copy(),
                'left': left,
                'right': right,
                'pivot_idx': new_pivot_idx,
                'k': k,
                'action': f'找到了！第 {self.k} 小的数是 {self.arr[k]}',
                'detail': {
                    'what': f'k = {k} 正好等于 pivot 位置',
                    'why': '这意味着 pivot 就是第 k 小的数',
                    'purpose': '算法结束'
                }
            })
        elif k < new_pivot_idx:
            self.steps.append({
                'type': 'recurse_left',
                'arr': self.arr.copy(),
                'left': left,
                'right': new_pivot_idx - 1,
                'pivot_idx': new_pivot_idx,
                'k': k,
                'action': f'k={k} < pivot位置{new_pivot_idx}，在左边继续找',
                'detail': {
                    'what': f'递归到左半部分 [{left}, {new_pivot_idx-1}]',
                    'why': '第 k 小的数在 pivot 左边',
                    'purpose': '缩小搜索范围'
                }
            })
            self._simulate(left, new_pivot_idx - 1, k)
        else:
            self.steps.append({
                'type': 'recurse_right',
                'arr': self.arr.copy(),
                'left': new_pivot_idx + 1,
                'right': right,
                'pivot_idx': new_pivot_idx,
                'k': k,
                'action': f'k={k} > pivot位置{new_pivot_idx}，在右边继续找',
                'detail': {
                    'what': f'递归到右半部分 [{new_pivot_idx+1}, {right}]',
                    'why': '第 k 小的数在 pivot 右边',
                    'purpose': '缩小搜索范围'
                }
            })
            self._simulate(new_pivot_idx + 1, right, k)
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        step_data = self.steps[step_index]
        
        # 绘制数组
        self.ax_arr.clear()
        arr = step_data['arr']
        n = len(arr)
        
        colors = ['#3498db'] * n  # 默认蓝色
        
        left = step_data.get('left', 0)
        right = step_data.get('right', n - 1)
        pivot_idx = step_data.get('pivot_idx', -1)
        k = step_data.get('k', -1)
        
        # 设置颜色
        for i in range(n):
            if i < left or i > right:
                colors[i] = '#bdc3c7'  # 灰色（不在当前范围）
            elif i == pivot_idx:
                colors[i] = '#e74c3c'  # 红色（pivot）
            elif i == k and step_data['type'] == 'found':
                colors[i] = '#27ae60'  # 绿色（找到的答案）
        
        if step_data['type'] == 'swap':
            i = step_data.get('i', -1)
            j = step_data.get('j', -1)
            if i >= 0:
                colors[i] = '#f39c12'  # 橙色（交换的元素）
            if j >= 0:
                colors[j] = '#f39c12'
        
        bars = self.ax_arr.bar(range(n), arr, color=colors, edgecolor='black', linewidth=1.5)
        
        # 添加数值标签
        for i, (bar, val) in enumerate(zip(bars, arr)):
            self.ax_arr.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                            str(val), ha='center', va='bottom', fontsize=12, fontweight='bold')
            # 索引标签
            self.ax_arr.text(bar.get_x() + bar.get_width() / 2, -1,
                            f'[{i}]', ha='center', va='top', fontsize=10, color='gray')
        
        self.ax_arr.set_ylim(-2, max(arr) * 1.2)
        self.ax_arr.set_title(f'步骤 {step_index + 1}/{len(self.steps)}: {step_data["action"]}',
                              fontsize=14, fontweight='bold')
        self.ax_arr.set_xlabel('索引', fontsize=12)
        self.ax_arr.set_ylabel('数值', fontsize=12)
        
        # 图例
        legend_elements = [
            plt.Rectangle((0, 0), 1, 1, facecolor='#3498db', label='当前范围'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#e74c3c', label='Pivot'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#f39c12', label='交换元素'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#27ae60', label='找到的答案'),
            plt.Rectangle((0, 0), 1, 1, facecolor='#bdc3c7', label='已排除'),
        ]
        self.ax_arr.legend(handles=legend_elements, loc='upper right', fontsize=9)
        
        # 绘制信息区域
        self.ax_info.clear()
        self.ax_info.axis('off')
        
        detail = step_data.get('detail', {})
        info_text = f"📋 目标：找第 {self.k} 小的数\n\n"
        if 'what' in detail:
            info_text += f"🔹 做什么：{detail['what']}\n"
        if 'why' in detail:
            info_text += f"🔹 为什么：{detail['why']}\n"
        if 'purpose' in detail:
            info_text += f"🔹 目的：{detail['purpose']}\n"
        
        self.ax_info.text(0.05, 0.9, info_text, transform=self.ax_info.transAxes,
                         fontsize=12, verticalalignment='top', linespacing=1.6,
                         bbox=dict(boxstyle='round', facecolor='#e8f6f3', alpha=0.9))
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q 退出'
        self.ax_info.text(0.5, 0.1, controls_text, transform=self.ax_info.transAxes,
                         ha='center', fontsize=10,
                         bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
        
        self.fig.tight_layout()
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
        plt.show()


def main():
    print("=" * 60)
    print("    TOP K问题 - 快速选择算法动画演示")
    print("=" * 60)
    print("\n选择示例：")
    print("  1. 题目样例: [1, 3, 2, 5, 4], k=4")
    print("  2. 随机数组: 8个随机数")
    print("  3. 自定义输入")
    
    choice = input("\n请输入选择 (1-3): ").strip()
    
    if choice == '1':
        arr = [1, 3, 2, 5, 4]
        k = 4
    elif choice == '2':
        random.seed(42)
        arr = [random.randint(1, 20) for _ in range(8)]
        k = random.randint(1, 8)
    elif choice == '3':
        line = input("请输入 n 和 k: ").split()
        n, k = int(line[0]), int(line[1])
        arr = list(map(int, input("请输入数组元素: ").split()))
    else:
        print("无效选择，使用示例 1")
        arr = [1, 3, 2, 5, 4]
        k = 4
    
    print("\n" + "─" * 60)
    print(f"数组: {arr}")
    print(f"目标: 找第 {k} 小的数")
    print("─" * 60)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Home / End   ：跳转到起点 / 终点")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = QuickSelectAnimation(arr, k)
    anim.show()


if __name__ == '__main__':
    main()
