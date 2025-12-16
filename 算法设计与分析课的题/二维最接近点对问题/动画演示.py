"""
二维最接近点对问题 - 动画演示（增强版）
使用 matplotlib 手动控制分治算法的执行过程
特点：
- 完整的C语言代码同步显示
- 每一步的详细说明（做什么、为什么、目的）
- 更直观的可视化效果
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


class ClosestPairAnimation:
    def __init__(self, points):
        self.points = points.copy()
        self.n = len(points)
        self.steps = []
        self.current_step = 0
        
        # 按x坐标排序
        self.points.sort(key=lambda p: (p[0], p[1]))
        
        # ============== 完整的C语言代码 ==============
        self.c_code_sections = {
            'distance': {
                'title': '📐 距离计算函数',
                'code': [
                    'double distance(Point p1, Point p2) {',
                    '    double dx = p1.x - p2.x;',
                    '    double dy = p1.y - p2.y;',
                    '    return sqrt(dx*dx + dy*dy);',
                    '}',
                ],
                'purpose': '计算两点之间的欧几里得距离'
            },
            'brute_force': {
                'title': '🔍 暴力法（基准情况）',
                'code': [
                    'double bruteForce(Point P[], int n) {',
                    '    double min = DBL_MAX;',
                    '    for (int i = 0; i < n; i++) {',
                    '        for (int j = i+1; j < n; j++) {',
                    '            double d = distance(P[i], P[j]);',
                    '            if (d < min) min = d;',
                    '        }',
                    '    }',
                    '    return min;',
                    '}',
                ],
                'purpose': '当点数≤3时，暴力枚举所有点对'
            },
            'strip_closest': {
                'title': '📏 条带内最近点对',
                'code': [
                    'double stripClosest(Point strip[], int size, double d) {',
                    '    double min = d;  // 初始化为当前最小距离',
                    '    // 按y坐标排序条带内的点',
                    '    qsort(strip, size, sizeof(Point), compareY);',
                    '    // 对于每个点，只检查y坐标差<d的点',
                    '    for (int i = 0; i < size; i++) {',
                    '        // 最多检查后续6个点（数学证明）',
                    '        for (int j = i+1; j < size &&',
                    '             (strip[j].y - strip[i].y) < min; j++) {',
                    '            double dist = distance(strip[i], strip[j]);',
                    '            if (dist < min) min = dist;',
                    '        }',
                    '    }',
                    '    return min;',
                    '}',
                ],
                'purpose': '在条带区域内寻找可能的更近点对'
            },
            'closest_util': {
                'title': '🔄 分治递归主函数',
                'code': [
                    'double closestUtil(Point Px[], int n) {',
                    '    // ===== 基准情况 =====',
                    '    if (n <= 3)',
                    '        return bruteForce(Px, n);',
                    '',
                    '    // ===== 分割步骤 =====',
                    '    int mid = n / 2;',
                    '    Point midPoint = Px[mid];',
                    '',
                    '    // ===== 递归求解左右子问题 =====',
                    '    double dl = closestUtil(Px, mid);',
                    '    double dr = closestUtil(Px + mid, n - mid);',
                    '',
                    '    // ===== 合并：取左右最小值 =====',
                    '    double d = min(dl, dr);',
                    '',
                    '    // ===== 构建条带区域 =====',
                    '    Point strip[n];',
                    '    int j = 0;',
                    '    for (int i = 0; i < n; i++) {',
                    '        if (abs(Px[i].x - midPoint.x) < d)',
                    '            strip[j++] = Px[i];',
                    '    }',
                    '',
                    '    // ===== 检查条带内的点对 =====',
                    '    double stripMin = stripClosest(strip, j, d);',
                    '',
                    '    return min(d, stripMin);',
                    '}',
                ],
                'purpose': '分治算法的核心递归函数'
            },
            'main_func': {
                'title': '🚀 主函数入口',
                'code': [
                    'double closest(Point P[], int n) {',
                    '    // 首先按x坐标排序所有点',
                    '    qsort(P, n, sizeof(Point), compareX);',
                    '    // 调用递归工具函数',
                    '    return closestUtil(P, n);',
                    '}',
                ],
                'purpose': '预处理（排序）后调用递归函数'
            }
        }
        
        self._simulate_algorithm(0, self.n, 0)
        
        # 创建画布 - 更大的尺寸以容纳代码和说明
        self.fig, (self.ax_visual, self.ax_code) = plt.subplots(1, 2, figsize=(20, 10))
        self.fig.canvas.manager.set_window_title('二维最接近点对问题 - 增强版动画演示')
        
        # 绑定键盘事件
        self.fig.canvas.mpl_connect('key_press_event', self._on_key_press)
    
    def _distance(self, p1, p2):
        """计算两点间距离"""
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.sqrt(dx * dx + dy * dy)
    
    def _brute_force(self, points, left, right):
        """暴力法计算最短距离"""
        min_dist = float('inf')
        for i in range(left, right):
            for j in range(i + 1, right):
                dist = self._distance(self.points[i], self.points[j])
                if dist < min_dist:
                    min_dist = dist
        return min_dist
    
    def _simulate_algorithm(self, left, right, depth):
        """模拟分治算法，记录每一步"""
        n = right - left
        
        # ==================== 进入递归 ====================
        self.steps.append({
            'type': 'enter',
            'left': left,
            'right': right,
            'depth': depth,
            'action': f'进入递归：处理区间 [{left}, {right})，共 {n} 个点',
            'code_section': 'closest_util',
            'highlight_lines': [0],  # 函数入口
            'step_detail': {
                'what': f'进入 closestUtil 函数，处理包含 {n} 个点的子数组',
                'why': '分治算法需要递归处理每个子问题',
                'purpose': f'找出这 {n} 个点中的最近点对距离',
                'current_state': f'处理点 P{left} 到 P{right-1}'
            }
        })
        
        # ==================== 递归终止条件（暴力法）====================
        if n <= 3:
            min_dist = self._brute_force(self.points, left, right)
            self.steps.append({
                'type': 'brute',
                'left': left,
                'right': right,
                'depth': depth,
                'min_dist': min_dist,
                'action': f'基准情况：点数 ≤ 3，使用暴力法',
                'code_section': 'brute_force',
                'highlight_lines': list(range(10)),  # 整个暴力法函数
                'step_detail': {
                    'what': f'对 {n} 个点进行暴力枚举',
                    'why': '当点数很少时，暴力法比继续分治更高效',
                    'purpose': '直接计算所有点对的距离，找最小值',
                    'result': f'最短距离 = {min_dist:.4f}'
                }
            })
            return min_dist
        
        # ==================== 分割步骤 ====================
        mid = left + n // 2
        mid_x = self.points[mid][0]
        
        self.steps.append({
            'type': 'split',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'action': f'分割：选择中点 mid = {mid}，分割线 x = {mid_x}',
            'code_section': 'closest_util',
            'highlight_lines': [5, 6, 7],  # 分割相关代码
            'step_detail': {
                'what': f'将点集从索引 {mid} 处分成左右两部分',
                'why': '分治法的核心思想：将大问题分解为小问题',
                'purpose': '左半部分 [{left}, {mid})，右半部分 [{mid}, {right})',
                'division': f'左边 {mid - left} 个点，右边 {right - mid} 个点'
            }
        })
        
        # ==================== 递归左半部分 ====================
        dl = self._simulate_algorithm(left, mid, depth + 1)
        
        self.steps.append({
            'type': 'left_result',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'dl': dl,
            'action': f'左半部分递归返回：dl = {dl:.4f}',
            'code_section': 'closest_util',
            'highlight_lines': [9, 10],  # 递归左半部分
            'step_detail': {
                'what': f'左区间 [{left}, {mid}) 的递归调用完成',
                'why': '获取左半部分点集中的最近点对距离',
                'purpose': '为后续合并步骤提供左半部分的结果',
                'result': f'dl = {dl:.4f}'
            }
        })
        
        # ==================== 递归右半部分 ====================
        dr = self._simulate_algorithm(mid, right, depth + 1)
        
        self.steps.append({
            'type': 'right_result',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'dr': dr,
            'action': f'右半部分递归返回：dr = {dr:.4f}',
            'code_section': 'closest_util',
            'highlight_lines': [11],  # 递归右半部分
            'step_detail': {
                'what': f'右区间 [{mid}, {right}) 的递归调用完成',
                'why': '获取右半部分点集中的最近点对距离',
                'purpose': '为后续合并步骤提供右半部分的结果',
                'result': f'dr = {dr:.4f}'
            }
        })
        
        # ==================== 合并开始 ====================
        d = min(dl, dr)
        
        self.steps.append({
            'type': 'merge_start',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'd': d,
            'dl': dl,
            'dr': dr,
            'action': f'合并：d = min({dl:.4f}, {dr:.4f}) = {d:.4f}',
            'code_section': 'closest_util',
            'highlight_lines': [13, 14],  # 合并代码
            'step_detail': {
                'what': f'取左右两部分最小值：d = min(dl, dr) = {d:.4f}',
                'why': '分治的合并步骤：整合子问题的解',
                'purpose': '但这还不是最终答案！可能存在跨中线的更近点对',
                'note': '⚠️ 关键洞察：最近点对可能一个在左边，一个在右边'
            }
        })
        
        # ==================== 构建条带 ====================
        strip = []
        for i in range(left, right):
            if abs(self.points[i][0] - mid_x) < d:
                strip.append(i)
        
        strip_sorted = sorted(strip, key=lambda i: (self.points[i][1], self.points[i][0]))
        
        self.steps.append({
            'type': 'strip',
            'left': left,
            'right': right,
            'mid': mid,
            'mid_x': mid_x,
            'depth': depth,
            'd': d,
            'strip': strip_sorted,
            'action': f'构建条带：找到 {len(strip_sorted)} 个点在条带区域内',
            'code_section': 'closest_util',
            'highlight_lines': [15, 16, 17, 18, 19, 20, 21],  # 构建条带的代码
            'step_detail': {
                'what': f'筛选出距离中线 x={mid_x} 小于 d={d:.4f} 的所有点',
                'why': '只有这些点才可能与对面的点形成更近的点对',
                'purpose': '缩小搜索范围，提高效率',
                'optimization': f'从 {n} 个点缩减到 {len(strip_sorted)} 个点需要检查'
            }
        })
        
        # ==================== 检查条带内点对 ====================
        strip_min = d
        for i in range(len(strip_sorted)):
            for j in range(i + 1, len(strip_sorted)):
                idx1, idx2 = strip_sorted[i], strip_sorted[j]
                if self.points[idx2][1] - self.points[idx1][1] >= d:
                    break
                dist = self._distance(self.points[idx1], self.points[idx2])
                if dist < strip_min:
                    strip_min = dist
                    self.steps.append({
                        'type': 'strip_check',
                        'left': left,
                        'right': right,
                        'mid': mid,
                        'mid_x': mid_x,
                        'depth': depth,
                        'd': d,
                        'strip': strip_sorted,
                        'check_i': i,
                        'check_j': j,
                        'dist': dist,
                        'action': f'🎯 发现更近点对！P{idx1} ↔ P{idx2}，距离 = {dist:.4f}',
                        'code_section': 'strip_closest',
                        'highlight_lines': [5, 6, 7, 8, 9, 10],  # 检查点对的循环
                        'step_detail': {
                            'what': f'比较条带内的点 P{idx1} 和 P{idx2}',
                            'why': '这两个点可能一左一右，形成跨中线的最近点对',
                            'purpose': '检查是否能找到比当前 d 更小的距离',
                            'result': f'✅ 找到更近的点对！距离 {dist:.4f} < {d:.4f}',
                            'update': f'更新 strip_min = {dist:.4f}'
                        }
                    })
        
        result = min(d, strip_min)
        
        # ==================== 合并完成 ====================
        self.steps.append({
            'type': 'merge_end',
            'left': left,
            'right': right,
            'mid': mid,
            'depth': depth,
            'd': d,
            'strip_min': strip_min,
            'result': result,
            'action': f'合并完成：返回 min({d:.4f}, {strip_min:.4f}) = {result:.4f}',
            'code_section': 'closest_util',
            'highlight_lines': [23, 24, 26],  # 返回结果
            'step_detail': {
                'what': f'完成区间 [{left}, {right}) 的处理',
                'why': '比较条带内最短距离与子问题最短距离',
                'purpose': '返回该区间内的最终最短距离',
                'final_result': f'区间 [{left}, {right}) 的最短距离 = {result:.4f}'
            }
        })
        
        return result
    
    def _draw_step(self, step_index=None):
        if step_index is None:
            step_index = self.current_step
        
        step_index = max(0, min(step_index, len(self.steps) - 1))
        self.current_step = step_index
        
        step_data = self.steps[step_index]
        
        # ==================== 绘制可视化区域 ====================
        self.ax_visual.clear()
        
        # 设置坐标轴
        if self.points:
            xs = [p[0] for p in self.points]
            ys = [p[1] for p in self.points]
            x_min, x_max = min(xs), max(xs)
            y_min, y_max = min(ys), max(ys)
            x_range = x_max - x_min
            y_range = y_max - y_min
            margin = max(x_range, y_range, 1) * 0.15
        else:
            x_min = y_min = 0
            x_max = y_max = 10
            margin = 1
        
        self.ax_visual.set_xlim(x_min - margin, x_max + margin)
        self.ax_visual.set_ylim(y_min - margin, y_max + margin)
        self.ax_visual.set_aspect('equal')
        self.ax_visual.grid(True, alpha=0.3)
        self.ax_visual.set_xlabel('X 坐标', fontsize=12)
        self.ax_visual.set_ylabel('Y 坐标', fontsize=12)
        
        # 主标题
        self.ax_visual.set_title(
            f'步骤 {step_index + 1}/{len(self.steps)}: {step_data["action"]}',
            fontsize=13, fontweight='bold', pad=15
        )
        
        # 绘制分割线和条带
        if step_data['type'] in ['split', 'merge_start', 'strip', 'strip_check', 'merge_end']:
            mid_x = step_data.get('mid_x', None)
            d = step_data.get('d', 0)
            
            if mid_x is not None:
                self.ax_visual.axvline(x=mid_x, color='green', linestyle='--', 
                              linewidth=2.5, alpha=0.8, label=f'分割线 x={mid_x}', zorder=1)
                
                if d > 0:
                    rect = patches.Rectangle(
                        (mid_x - d, y_min - margin), 2 * d, y_max - y_min + 2 * margin,
                        linewidth=2, edgecolor='orange', facecolor='yellow', 
                        alpha=0.15, zorder=0, label=f'条带区域 (宽度=2d={2*d:.2f})'
                    )
                    self.ax_visual.add_patch(rect)
        
        # 绘制所有点
        for i, point in enumerate(self.points):
            color = '#3498db'  # 默认蓝色
            size = 120
            alpha = 0.7
            
            if step_data['type'] in ['split', 'merge_start', 'strip', 'strip_check', 'merge_end', 'left_result', 'right_result']:
                left = step_data.get('left', 0)
                right = step_data.get('right', self.n)
                mid = step_data.get('mid', 0)
                
                if left <= i < right:
                    if i < mid:
                        color = '#3498db'  # 左边 - 蓝色
                    else:
                        color = '#e74c3c'  # 右边 - 红色
                    
                    # 条带内的点
                    if step_data['type'] in ['strip', 'strip_check']:
                        strip = step_data.get('strip', [])
                        if i in strip:
                            color = '#f39c12'  # 条带内 - 橙色
                            size = 180
                            alpha = 0.9
                    
                    # 正在检查的点对
                    if step_data['type'] == 'strip_check':
                        check_i = step_data.get('check_i', -1)
                        check_j = step_data.get('check_j', -1)
                        strip = step_data.get('strip', [])
                        if check_i >= 0 and check_j >= 0 and i in [strip[check_i], strip[check_j]]:
                            color = '#9b59b6'  # 检查中 - 紫色
                            size = 250
                            alpha = 1.0
                else:
                    alpha = 0.3  # 不在当前区间的点变淡
            
            elif step_data['type'] == 'brute':
                left = step_data.get('left', 0)
                right = step_data.get('right', self.n)
                if left <= i < right:
                    color = '#27ae60'  # 暴力法处理 - 绿色
                    size = 180
                else:
                    alpha = 0.3
            
            self.ax_visual.scatter(point[0], point[1], c=color, s=size, alpha=alpha, 
                          edgecolors='black', linewidths=1.5, zorder=5)
            self.ax_visual.text(point[0], point[1] + margin * 0.08, f'P{i}', 
                        fontsize=10, ha='center', fontweight='bold', zorder=6)
        
        # 绘制正在检查的点对连线
        if step_data['type'] == 'strip_check':
            check_i = step_data.get('check_i', -1)
            check_j = step_data.get('check_j', -1)
            strip = step_data.get('strip', [])
            if check_i >= 0 and check_j >= 0:
                idx1, idx2 = strip[check_i], strip[check_j]
                p1, p2 = self.points[idx1], self.points[idx2]
                self.ax_visual.plot([p1[0], p2[0]], [p1[1], p2[1]], 
                           color='#9b59b6', linewidth=3, alpha=0.8, zorder=4,
                           marker='o', markersize=8)
                dist = step_data.get('dist', 0)
                mid_point_x = (p1[0] + p2[0]) / 2
                mid_point_y = (p1[1] + p2[1]) / 2
                self.ax_visual.text(mid_point_x, mid_point_y + 0.15, f'd={dist:.4f}', 
                           fontsize=11, ha='center', va='bottom', fontweight='bold',
                           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.9),
                           zorder=7)
        
        # 图例
        self.ax_visual.legend(loc='upper left', fontsize=9)
        
        # 操作提示
        controls_text = '操作：空格/→ 下一步 · ← 上一步 · Home 开始 · End 结束 · Q/Esc 退出'
        self.ax_visual.text(0.5, -0.08, controls_text, transform=self.ax_visual.transAxes,
                    ha='center', fontsize=10,
                    bbox=dict(boxstyle='round', facecolor='#ecf0f1', alpha=0.8))
        
        # ==================== 绘制代码和说明区域 ====================
        self.ax_code.clear()
        self.ax_code.axis('off')
        
        # 获取当前步骤的代码section
        code_section = step_data.get('code_section', 'closest_util')
        section = self.c_code_sections.get(code_section, self.c_code_sections['closest_util'])
        highlight_lines = set(step_data.get('highlight_lines', []))
        step_detail = step_data.get('step_detail', {})
        
        # ===== 当前步骤详细说明 =====
        y_pos = 0.98
        
        # 标题
        self.ax_code.text(0.02, y_pos, '📋 当前步骤说明', transform=self.ax_code.transAxes,
                         fontsize=14, fontweight='bold', color='#2c3e50')
        y_pos -= 0.06
        
        # 详细说明框
        detail_box = []
        if 'what' in step_detail:
            detail_box.append(f"🔹 做什么：{step_detail['what']}")
        if 'why' in step_detail:
            detail_box.append(f"🔹 为什么：{step_detail['why']}")
        if 'purpose' in step_detail:
            detail_box.append(f"🔹 目的：{step_detail['purpose']}")
        if 'result' in step_detail:
            detail_box.append(f"🔹 结果：{step_detail['result']}")
        if 'note' in step_detail:
            detail_box.append(f"💡 {step_detail['note']}")
        if 'optimization' in step_detail:
            detail_box.append(f"⚡ 优化：{step_detail['optimization']}")
        if 'update' in step_detail:
            detail_box.append(f"🔄 更新：{step_detail['update']}")
        if 'final_result' in step_detail:
            detail_box.append(f"✅ {step_detail['final_result']}")
        if 'division' in step_detail:
            detail_box.append(f"📊 {step_detail['division']}")
        if 'current_state' in step_detail:
            detail_box.append(f"📍 {step_detail['current_state']}")
        
        detail_text = '\n'.join(detail_box)
        self.ax_code.text(0.02, y_pos, detail_text, transform=self.ax_code.transAxes,
                         fontsize=11, verticalalignment='top', linespacing=1.6,
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='#e8f6f3', alpha=0.9))
        
        y_pos -= 0.02 + len(detail_box) * 0.045
        
        # ===== C语言代码显示 =====
        y_pos -= 0.05
        self.ax_code.text(0.02, y_pos, f'💻 {section["title"]}', transform=self.ax_code.transAxes,
                         fontsize=13, fontweight='bold', color='#8e44ad')
        y_pos -= 0.03
        
        self.ax_code.text(0.02, y_pos, f'({section["purpose"]})', transform=self.ax_code.transAxes,
                         fontsize=10, color='#7f8c8d', style='italic')
        y_pos -= 0.04
        
        # 代码内容
        code_lines = section['code']
        code_display = []
        for idx, line in enumerate(code_lines):
            if idx in highlight_lines:
                code_display.append(f'▶ {line}')
            else:
                code_display.append(f'  {line}')
        
        code_text = '\n'.join(code_display)
        self.ax_code.text(0.02, y_pos, code_text, transform=self.ax_code.transAxes,
                         fontsize=9, fontfamily='monospace',
                         verticalalignment='top', linespacing=1.4,
                         bbox=dict(boxstyle='round,pad=0.5', facecolor='#2c3e50', alpha=0.95),
                         color='#ecf0f1')
        
        # ===== 递归深度指示器 =====
        depth = step_data.get('depth', 0)
        depth_indicator = '│  ' * depth + '├─' if depth > 0 else '●'
        self.ax_code.text(0.98, 0.98, f'递归深度: {depth}\n{depth_indicator}', 
                         transform=self.ax_code.transAxes,
                         fontsize=10, fontweight='bold', ha='right', va='top',
                         bbox=dict(boxstyle='round', facecolor='#fdebd0', alpha=0.9))
        
        # ===== 当前状态概览 =====
        left = step_data.get('left', 0)
        right = step_data.get('right', self.n)
        status_text = f'当前区间: [{left}, {right})\n点数: {right - left}'
        if 'd' in step_data:
            status_text += f'\n当前d: {step_data["d"]:.4f}'
        
        self.ax_code.text(0.98, 0.75, status_text, 
                         transform=self.ax_code.transAxes,
                         fontsize=10, ha='right', va='top',
                         bbox=dict(boxstyle='round', facecolor='#d5f5e3', alpha=0.9))
        
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
    print("=" * 65)
    print("    二维最接近点对问题 - 增强版动画演示")
    print("    （包含完整C代码 + 每步详细说明）")
    print("=" * 65)
    print("\n选择示例：")
    print("  1. 示例 1: 4个点 (0,0), (0,1), (1,0), (1,1)")
    print("  2. 示例 2: 3个点 (0,0), (1,1), (2,2)")
    print("  3. 示例 3: 6个点（随机分布）")
    print("  4. 示例 4: 8个点（适合展示多层递归）")
    print("  5. 自定义输入")
    
    choice = input("\n请输入选择 (1-5): ").strip()
    
    if choice == '1':
        points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    elif choice == '2':
        points = [(0, 0), (1, 1), (2, 2)]
    elif choice == '3':
        import random
        random.seed(42)
        points = [(random.randint(0, 10), random.randint(0, 10)) for _ in range(6)]
    elif choice == '4':
        points = [(1, 2), (2, 5), (3, 1), (4, 4), (6, 2), (7, 5), (8, 3), (9, 1)]
    elif choice == '5':
        n = int(input("请输入点的个数: "))
        points = []
        for i in range(n):
            x, y = map(float, input(f"点 {i+1} 的坐标 (x y): ").split())
            points.append((x, y))
    else:
        print("无效选择，使用示例 4（8个点）")
        points = [(1, 2), (2, 5), (3, 1), (4, 4), (6, 2), (7, 5), (8, 3), (9, 1)]
    
    print("\n" + "─" * 65)
    print("开始演示...")
    print(f"点数: {len(points)}")
    print("─" * 65)
    print("\n📌 操作提示：")
    print("   空格 / 右箭头 ：下一步")
    print("   左箭头       ：上一步")
    print("   Home / End   ：跳转到起点 / 终点")
    print("   Q / Esc      ：退出动画")
    print("\n⚠️  请先点击弹出的窗口以获取焦点，再使用键盘控制\n")
    
    anim = ClosestPairAnimation(points)
    anim.show()


if __name__ == '__main__':
    main()
