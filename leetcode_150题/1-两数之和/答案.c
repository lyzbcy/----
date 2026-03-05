/**
 * LeetCode 1. 两数之和
 *
 * 方法：暴力枚举
 * 时间复杂度：O(n^2)
 * 空间复杂度：O(1)
 */

#include <stdlib.h>

int* twoSum(int* nums, int numsSize, int target, int* returnSize) {
    // 1. 寻找答案
    for (int i = 0; i < numsSize - 1; i++) {
        for (int j = i + 1; j < numsSize; j++) {
            if (nums[i] + nums[j] == target) {
                // 找到目标！分配内存并返回
                int* result = (int*)malloc(sizeof(int) * 2);
                result[0] = i;
                result[1] = j;
                
                // 设置返回数组的大小为 2
                *returnSize = 2;
                return result;
            }
        }
    }
    
    // 2. 如果没找到（题目保证一定会找到，但为了代码完整性）
    *returnSize = 0;
    return NULL;
}
