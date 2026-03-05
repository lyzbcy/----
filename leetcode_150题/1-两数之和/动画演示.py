"""
LeetCode 1. 两数之和 - 动画演示
演示暴力枚举法：固定一个数，扫描其余数
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 设置中文字体
# 尝试多种常用中文字体，防止乱码
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class TwoSumAnimation:
    def __init__(self, nums, target):
        self.nums = nums
        self.target = target
        self.length = len(nums)
        self.steps = []
        self.current_step = 0
        
        # 可视化参数
        self.visual_width = max(self.length, 6)
        self.x_limit = self.visual_width + 8
        
        # 预先计算所有步骤
        self._simulate_algorithm()
        
        # 创建画布
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.fig.canvas.manager.set_window_title(f'两数之和 - 动画演示 (Target={target})')
        self.ax.axis('off')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)

    def _simulate_algorithm(self):
        """记录暴力解法的每一步"""
        
        # 初始状态
        self.steps.append({
            'i': -1, 'j': -1,
            'found': False,
            'action': '开始：准备双重循环暴力枚举',
            'explanation': f'目标值 target = {self.target}。我们需要找到两个数相加等于它。'
        })
        
        for i in range(self.length - 1):
            for j in range(i + 1, self.length):
                val_i = self.nums[i]
                val_j = self.nums[j]
                current_sum = val_i + val_j
                
                is_match = (current_sum == self.target)
                
                action_text = f'检查 nums[{i}] + nums[{j}] = {val_i} + {val_j} = {current_sum}'
                
                if is_match:
                    explanation = f'恭喜！ {val_i} + {val_j} == {self.target}。找到答案：[{i}, {j}]'
                else:
                    if current_sum < self.target:
                        explanation = f'当前和 {current_sum} 小于目标 {self.target}，继续寻找。'
                    else:
                        explanation = f'当前和 {current_sum} 大于目标 {self.target}，继续寻找。'

                self.steps.append({
                    'i': i, 'j': j,
                    'found': is_match,
                    'action': action_text,
                    'explanation': explanation
                })
                
                if is_match:
                    return

        # 如果没有找到（理论上本题一定有解）
        self.steps.append({
            'i': -1, 'j': -1,
            'found': False,
            'action': '结束',
            'explanation': '未找到答案。'
        })

    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
            
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        
        step_data = self.steps[step_index]
        
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim(-1, self.x_limit)
        self.ax.set_ylim(-2, 6)
        
        # 标题信息
        self.ax.text(
            self.visual_width / 2, 5.5,
            f'步骤 {step_index}/{len(self.steps)-1}: {step_data["action"]}',
            ha='center', fontsize=16, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )
        
        self.ax.text(
            self.visual_width / 2, 4.8,
            step_data["explanation"],
            ha='center', fontsize=14, color='darkblue'
        )
        
        # 绘制 Target
        self.ax.text(
            -0.5, 4.5, f'Target: {self.target}',
            fontsize=14, fontweight='bold',
            bbox=dict(boxstyle='square', facecolor='gold', alpha=0.6)
        )

        # 绘制数组元素
        for idx, val in enumerate(self.nums):
            # 默认颜色
            facecolor = 'white'
            edgecolor = 'black'
            linewidth = 2
            
            # 根据状态改变颜色
            i, j = step_data['i'], step_data['j']
            
            if step_data['found'] and (idx == i or idx == j):
                facecolor = 'lightgreen' # 找到答案
                edgecolor = 'green'
                linewidth = 4
            elif idx == i:
                facecolor = 'lightblue' # 当前固定的第一个数
            elif idx == j:
                facecolor = 'lightyellow' # 当前扫描的第二个数
            
            # 绘制方块
            rect = patches.Rectangle(
                (idx - 0.4, 2), 0.8, 0.8,
                linewidth=linewidth, edgecolor=edgecolor, facecolor=facecolor
            )
            self.ax.add_patch(rect)
            
            # 绘制数值
            self.ax.text(idx, 2.4, str(val), ha='center', va='center', fontsize=16)
            
            # 绘制索引
            self.ax.text(idx, 1.5, f'[{idx}]', ha='center', va='center', fontsize=10, color='gray')
            
            # 绘制指针标签
            if idx == i:
                self.ax.annotate('i', xy=(idx, 3), xytext=(idx, 3.5),
                                 arrowprops=dict(arrowstyle='->', color='blue'),
                                 ha='center', color='blue', fontsize=14, fontweight='bold')
            if idx == j:
                self.ax.annotate('j', xy=(idx, 1.8), xytext=(idx, 1.0),
                                 arrowprops=dict(arrowstyle='->', color='orange'),
                                 ha='center', color='orange', fontsize=14, fontweight='bold')

        # 操作提示
        instructions = "操作指南：空格/→ 下一步  |  ← 上一步  |  Home 重来  |  Q 退出"
        self.ax.text(self.visual_width / 2, -1, instructions, ha='center', fontsize=12, color='gray')

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
        elif event.key in ('q', 'escape'):
            plt.close(self.fig)

    def show(self):
        self._draw_step(0)
        plt.show()

def main():
    print("------------------------------------------------")
    print("LeetCode 1. 两数之和 - 暴力法演示")
    print("------------------------------------------------")
    print("1. 示例 1: nums=[2,7,11,15], target=9")
    print("2. 示例 2: nums=[3,2,4], target=6")
    print("3. 示例 3: nums=[3,3], target=6")
    print("4. 自定义输入")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == '1':
        nums, target = [2, 7, 11, 15], 9
    elif choice == '2':
        nums, target = [3, 2, 4], 6
    elif choice == '3':
        nums, target = [3, 3], 6
    elif choice == '4':
        try:
            nums_str = input("输入数组 (空格分隔): ")
            nums = list(map(int, nums_str.split()))
            target = int(input("输入 Target: "))
        except:
            print("输入格式错误，使用默认示例。")
            nums, target = [2, 7, 11, 15], 9
    else:
        nums, target = [2, 7, 11, 15], 9
        
    print(f"\n当前输入: nums={nums}, target={target}")
    print("正在启动动画窗口...")
    
    anim = TwoSumAnimation(nums, target)
    anim.show()

if __name__ == "__main__":
    main()
