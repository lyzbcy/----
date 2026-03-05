/**
 * 二维最接近点对问题
 * 
 * 使用分治算法求解
 * 时间复杂度：O(n log² n)
 * 空间复杂度：O(n)
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>

// 定义点结构体
typedef struct {
    int x;
    int y;
} Point;

// 按x坐标排序的比较函数
int compareX(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (p1->x != p2->x) {
        return p1->x - p2->x;
    }
    return p1->y - p2->y;
}

// 按y坐标排序的比较函数
int compareY(const void *a, const void *b) {
    Point *p1 = (Point *)a;
    Point *p2 = (Point *)b;
    if (p1->y != p2->y) {
        return p1->y - p2->y;
    }
    return p1->x - p2->x;
}

// 计算两点间距离
double distance(Point p1, Point p2) {
    int dx = p1.x - p2.x;
    int dy = p1.y - p2.y;
    return sqrt((double)dx * dx + (double)dy * dy);
}

// 暴力枚举计算n≤3时的最短距离
double bruteForce(Point points[], int n) {
    double min_dist = DBL_MAX;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            double dist = distance(points[i], points[j]);
            if (dist < min_dist) {
                min_dist = dist;
            }
        }
    }
    return min_dist;
}

// 计算条带区域内的最短距离
double stripClosest(Point strip[], int size, double d) {
    double min_dist = d;
    
    // 按y坐标排序条带中的点
    qsort(strip, size, sizeof(Point), compareY);
    
    // 对于每个点，只需检查其后的最多6个点
    for (int i = 0; i < size; i++) {
        for (int j = i + 1; j < size && (strip[j].y - strip[i].y) < min_dist; j++) {
            double dist = distance(strip[i], strip[j]);
            if (dist < min_dist) {
                min_dist = dist;
            }
        }
    }
    
    return min_dist;
}

// 分治算法主函数
double closestUtil(Point points[], int n) {
    // 递归终止条件：点数≤3时使用暴力法
    if (n <= 3) {
        return bruteForce(points, n);
    }
    
    // 找到中点
    int mid = n / 2;
    Point midPoint = points[mid];
    
    // 递归求解左右两部分
    double dl = closestUtil(points, mid);
    double dr = closestUtil(points + mid, n - mid);
    
    // 取左右两部分的最小距离
    double d = (dl < dr) ? dl : dr;
    
    // 构建条带：距离中线d范围内的点
    Point *strip = (Point *)malloc(n * sizeof(Point));
    int stripSize = 0;
    for (int i = 0; i < n; i++) {
        if (abs(points[i].x - midPoint.x) < d) {
            strip[stripSize++] = points[i];
        }
    }
    
    // 计算条带内的最短距离

    free(strip);
    
    // 返回全局最小距离
    return (d < stripMin) ? d : stripMin;
}

// 主函数：计算最近点对距离
double closest(Point points[], int n) {
    // 按x坐标排序
    qsort(points, n, sizeof(Point), compareX);
    
    // 调用分治算法
    return closestUtil(points, n);
}

int main() {
    int n;
    scanf("%d", &n);
    
    Point *points = (Point *)malloc(n * sizeof(Point));
    for (int i = 0; i < n; i++) {
        scanf("%d %d", &points[i].x, &points[i].y);
    }
    
    double result = closest(points, n);
    printf("%.2f\n", result);
    
    free(points);
    return 0;
}

