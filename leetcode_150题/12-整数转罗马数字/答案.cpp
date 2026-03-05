/*
 * LeetCode 12. 整数转罗马数字
 * 题目链接：https://leetcode.cn/problems/integer-to-roman/
 *
 * 思路：贪心 + 预建对照表（C++ string 版本）
 * 与 C 版本逻辑相同，借助 std::string 自动管理内存，代码更简洁。
 *
 * 时间复杂度：O(1)
 * 空间复杂度：O(1)
 */

#include <string>
#include <vector>
using namespace std;

class Solution {
public:
    string intToRoman(int num) {
        /* 数值-符号对照表，从大到小，含减法特殊情况 */
        vector<int>    values  = {1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1};
        vector<string> symbols = {"M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"};

        string result = "";
        /* 贪心：从最大值开始逐步匹配并拼接 */
        for (int i = 0; i < (int)values.size(); i++) {
            while (num >= values[i]) {
                result += symbols[i];   /* 拼接当前符号 */
                num -= values[i];       /* 减去当前数值 */
            }
        }
        return result;
    }
};

/* 本地测试入口（LeetCode 提交时删除 main） */
#include <iostream>
int main() {
    Solution sol;
    int tests[] = {3749, 58, 1994, 3999, 1};
    for (int t : tests) {
        cout << t << " -> " << sol.intToRoman(t) << "\n";
    }
    return 0;
}
