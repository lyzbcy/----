/*
 * LeetCode 36. 有效的数独
 * 题目链接：https://leetcode.cn/problems/valid-sudoku/
 *
 * 思路：同 C 版本，用 vector<vector<bool>> 或直接 bool[9][10] 均可。
 * 此处使用与 C 相同的固定数组，保持逻辑一致；也可改用 unordered_set。
 *
 * 时间复杂度：O(1)
 * 空间复杂度：O(1)
 */

#include <vector>
#include <cstring>
using namespace std;

class Solution {
public:
    bool isValidSudoku(vector<vector<char>>& board) {
        bool row[9][10] = {};
        bool col[9][10] = {};
        bool box[9][10] = {};

        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                if (board[i][j] == '.') continue;

                int num      = board[i][j] - '0';
                int boxIndex = (i / 3) * 3 + j / 3;

                if (row[i][num] || col[j][num] || box[boxIndex][num]) {
                    return false;
                }

                row[i][num]        = true;
                col[j][num]        = true;
                box[boxIndex][num] = true;
            }
        }
        return true;
    }
};
