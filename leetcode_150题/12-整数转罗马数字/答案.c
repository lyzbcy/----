/*
 * LeetCode 12. 整数转罗马数字
 * 题目链接：https://leetcode.cn/problems/integer-to-roman/
 *
 * 思路：贪心 + 预建对照表
 * 预先建立"数值-符号"对照表（含6个特殊组合），从大到小依次匹配，
 * 每次尽可能多地减去最大可用值并拼接对应符号，直到 num 归零。
 *
 * 时间复杂度：O(1)（输入范围 [1,3999]，循环次数有固定上界）
 * 空间复杂度：O(1)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* intToRoman(int num) {
    /* 数值对照表（从大到小，包含6个特殊减法组合） */
    int values[]     = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
    char *loma[]     = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

    /* 最长结果：3999 -> "MMMCMXCIX"，约15个字符，预留20位 */
    char *result = (char *)malloc(20 * sizeof(char));
    result[0] = '\0';

    int i = 0;
    /* 贪心：当 num 还剩余时，找第一个不超过 num 的符号并拼接 */
    while (num > 0) {
        while (num >= values[i]) {
            strcat(result, loma[i]);   /* 拼接对应罗马符号 */
            num -= values[i];          /* 减去对应数值 */
        }
        i++;
    }
    return result;
}

/* 本地测试入口（LeetCode 提交时删除 main） */
int main(void) {
    int tests[] = {3749, 58, 1994, 3999, 1};
    int n = sizeof(tests) / sizeof(tests[0]);
    for (int i = 0; i < n; i++) {
        char *r = intToRoman(tests[i]);
        printf("%d -> %s\n", tests[i], r);
        free(r);
    }
    return 0;
}
