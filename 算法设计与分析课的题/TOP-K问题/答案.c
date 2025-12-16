/**
 * TOP K问题 - 快速选择算法
 * 
 * 时间复杂度：O(n) 期望
 * 空间复杂度：O(1)
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define MAX_N 100005

int arr[MAX_N];

// 交换两个元素
void swap(int *a, int *b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// 分区操作
int partition(int left, int right) {
    int pivot = arr[right];
    int i = left - 1;
    
    for (int j = left; j < right; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[right]);
    return i + 1;
}

// 随机化分区，避免最坏情况
int randomPartition(int left, int right) {
    int randomIndex = left + rand() % (right - left + 1);
    swap(&arr[randomIndex], &arr[right]);
    return partition(left, right);
}

// 快速选择算法
int quickSelect(int left, int right, int k) {
    // 递归终止条件
    if (left == right) {
        return arr[left];
    }
    
    // 随机化分区
    int pivotIndex = randomPartition(left, right);
    
    // 根据 pivot 位置决定继续查找的方向
    if (k == pivotIndex) {
        return arr[k];
    } else if (k < pivotIndex) {
        return quickSelect(left, pivotIndex - 1, k);
    } else {
        return quickSelect(pivotIndex + 1, right, k);
    }
}

int main() {
    // 设置随机种子
    srand(time(NULL));
    
    int n, k;
    scanf("%d %d", &n, &k);
    
    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }
    
    // 找第k小的数（转为0-indexed）
    int result = quickSelect(0, n - 1, k - 1);
    
    printf("%d\n", result);
    
    return 0;
}
