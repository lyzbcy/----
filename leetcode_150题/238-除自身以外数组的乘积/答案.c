/**
 * LeetCode 238. 除自身以外数组的乘积
 *
 * 时间复杂度：O(n)
 * 空间复杂度：O(1) 额外空间（输出数组不计入）
 */

#include <stdlib.h>

int* productExceptSelf(int* nums, int numsSize, int* returnSize) {
    if (returnSize == NULL) {
        return NULL;
    }
    *returnSize = numsSize;
    if (numsSize == 0) {
        return NULL;
    }

    int* answer = (int*)malloc(sizeof(int) * numsSize);
    if (answer == NULL) {
        return NULL;
    }

    int prefix = 1;  // 记录当前位置左侧的乘积
    for (int i = 0; i < numsSize; i++) {
        answer[i] = prefix;
        prefix *= nums[i];
    }

    int suffix = 1;  // 记录当前位置右侧的乘积
    for (int i = numsSize - 1; i >= 0; i--) {
        answer[i] *= suffix;
        suffix *= nums[i];
    }

    return answer;
}














