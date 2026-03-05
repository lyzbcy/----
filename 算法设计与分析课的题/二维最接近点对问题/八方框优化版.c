/**
 * 二维最接近点对问题 - 优化版本
 * 
 * 基于分治算法，结合三项创新优化：
 * 1. 切比雪夫距离预筛选法（正方形包围圆）
 * 2. 距离平方比较法（延迟开方）
 * 3. 单调性剪枝（利用 X 排序的有序性）
 * 
 * 时间复杂度：O(n log n)
 * 空间复杂度：O(n)
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <limits.h>

// 定义点结构体
typedef struct {
    int x;  // 点的x坐标
    int y;  // 点的y坐标
} Point;

// ========== 辅助函数 ==========

// 按x坐标排序的比较函数
int compareX(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (p1->x != p2->x) {
        return p1->x - p2->x;
    }
    return p1->y - p2->y;  // x相同时按y排序
}

// 按y坐标排序的比较函数
int compareY(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (p1->y != p2->y) {
        return p1->y - p2->y;
    }
    return p1->x - p2->x;  // y相同时按x排序
}

// ========== 优化二：距离平方比较法 ==========
/**
 * 计算两点间距离的平方（完全避免 sqrt）
 * 使用 long long 防止整数溢出（坐标最大 1e9）
 * 数学原理：sqrt(a) < sqrt(b) <=> a < b（当 a, b >= 0）
 */
long long distSquared(Point p1, Point p2) {
    long long dx = (long long)(p1.x - p2.x);
    long long dy = (long long)(p1.y - p2.y);
    return dx * dx + dy * dy;
}

/**
 * 暴力枚举计算 n<=3 时的最短距离（返回距离的平方）
 * 结合优化一：切比雪夫距离预筛选
 * 结合优化二：距离平方比较
 */
long long bruteForce(Point points[], int n) {
    long long min_dist_sq = LLONG_MAX;  // 初始化为极大值
    
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            // 优化二：直接计算距离平方
            long long dist_sq = distSquared(points[i], points[j]);
            if (dist_sq < min_dist_sq) {
                min_dist_sq = dist_sq;
            }
        }
    }
    return min_dist_sq;
}

/**
 * 计算条带区域 strip 内的最短距离平方（不超过 d_sq）
 * 条带内点已按 y 坐标排序
 * 
 * 结合三项优化：
 * - 切比雪夫预筛选：用 max(|dx|, |dy|) 快速排除
 * - 距离平方比较：全程使用平方值比较
 * - 六方格理论：每点最多与后续 7 个点比较
 */
long long stripClosest(Point strip[], int size, long long d_sq) {
    long long min_dist_sq = d_sq;
    
    // 按 y 坐标排序，使空间上接近的点在数组中相邻
    qsort(strip, size, sizeof(Point), compareY);
    
    // 计算当前最小距离的平方根（用于切比雪夫预筛选）
    // 使用 ceil 确保不会错过候选点
    long long d_linear = (long long)ceil(sqrt((double)min_dist_sq));
    
    for (int i = 0; i < size; i++) {
        for (int j = i + 1; j < size; j++) {
            // 利用 y 排序：如果 y 差平方已超过 min_dist_sq，跳出
            long long dy = (long long)(strip[j].y - strip[i].y);
            
            // 单调性剪枝：y 差已超过阈值，后面的点 y 差只会更大
            if (dy * dy >= min_dist_sq) {
                break;  // 跳出内层循环
            }
            
            long long dx = (long long)abs(strip[j].x - strip[i].x);
            
            // 优化一：切比雪夫距离预筛选
            // 如果 max(|dx|, |dy|)^2 >= min_dist_sq，则欧氏距离必然 >= sqrt(min_dist_sq)
            if (dx * dx >= min_dist_sq) {
                continue;  // 跳过这一对
            }
            
            // 优化二：距离平方比较
            long long dist_sq = dx * dx + dy * dy;
            if (dist_sq < min_dist_sq) {
                min_dist_sq = dist_sq;
            }
        }
    }
    
    return min_dist_sq;
}

/**
 * 递归分治算法核心函数
 * 返回最短距离的平方
 */
long long closestUtil(Point points[], int n) {
    // 递归终止条件：点数 <= 3 时使用暴力法
    if (n <= 3) {
        return bruteForce(points, n);
    }
    
    // 找到中点，分割点集
    int mid = n / 2;
    Point midPoint = points[mid];
    
    // 递归求解左右两部分（返回距离的平方）
    long long d1_sq = closestUtil(points, mid);              // 左半部分
    long long d2_sq = closestUtil(points + mid, n - mid);    // 右半部分
    
    // 取左右两部分的最小距离平方
    long long d_sq = (d1_sq < d2_sq) ? d1_sq : d2_sq;
    
    // 计算当前最小距离（用于筛选条带）
    double d = sqrt((double)d_sq);
    
    // 构建条带：距离中线 d 范围内的点
    Point *strip = (Point *)malloc(n * sizeof(Point));
    int stripSize = 0;
    
    for (int i = 0; i < n; i++) {
        // 优化三：使用整数比较，避免浮点运算
        long long x_diff = (long long)abs(points[i].x - midPoint.x);
        
        // 如果 x 差都已经超过 d，则距离必然 >= d
        if ((double)x_diff < d) {
            strip[stripSize++] = points[i];
        }
    }
    
    // 计算条带内的最短距离平方
    long long stripMin_sq = stripClosest(strip, stripSize, d_sq);
    
    free(strip);  // 释放内存
    
    // 返回全局最小距离平方
    return (d_sq < stripMin_sq) ? d_sq : stripMin_sq;
}

/**
 * 主函数：计算最近点对距离
 * 整合所有优化，返回最终距离值
 */
double closest(Point points[], int n) {
    // 按 x 坐标排序（为单调性剪枝和分治做准备）
    qsort(points, n, sizeof(Point), compareX);
    
    // 调用分治算法，得到最短距离的平方
    long long min_dist_sq = closestUtil(points, n);
    
    // 优化二的核心：只在最后输出时开方一次
    return sqrt((double)min_dist_sq);
}

int main() {
    int n;
    scanf("%d", &n);
    
    // 特殊情况处理：少于 2 个点无有效点对
    if (n < 2) {
        printf("0.00\n");
        return 0;
    }
    
    // 动态分配点集内存（支持 n = 1e5）
    Point *points = (Point *)malloc(n * sizeof(Point));
    for (int i = 0; i < n; i++) {
        scanf("%d %d", &points[i].x, &points[i].y);
    }
    
    // 计算最短距离并保留 2 位小数输出（自动四舍五入）
    double result = closest(points, n);
    printf("%.2f\n", result);
    
    free(points);  // 释放内存
    return 0;
}
