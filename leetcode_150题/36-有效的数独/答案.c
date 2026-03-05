/*
 * LeetCode 36. 有效的数独
 * 题目链接：https://leetcode.cn/problems/valid-sudoku/
 *
 * 思路：哈希表（布尔数组）+ 一次遍历
 * 预分配三张 9×10 的布尔数组，分别记录每行/列/宫中 1~9 是否已出现。
 * 遍历 81 个格子，跳过 '.'，对数字同时检查并更新三张表，发现重复立即返回 false。
 *
 * 宫编号公式：boxIndex = (i/3)*3 + j/3，将 9 个 3×3 宫编号为 0~8。
 *
 * 时间复杂度：O(81) = O(1)（棋盘大小固定）
 * 空间复杂度：O(243) = O(1)（三张布尔表大小固定）
 */

#include <stdio.h>
#include <stdbool.h>
#include <string.h>

bool isValidSudoku(char** board, int boardSize, int* boardColSize) {
    /* 三张标记表：下标 [行/列/宫编号][数字1~9] */
    bool row[9][10];
    bool col[9][10];
    bool box[9][10];
    memset(row, false, sizeof(row));
    memset(col, false, sizeof(col));
    memset(box, false, sizeof(box));

    for (int i = 0; i < 9; i++) {
        for (int j = 0; j < 9; j++) {
            if (board[i][j] == '.') {
                continue;                       /* 空格跳过 */
            }

            int num      = board[i][j] - '0';  /* 字符转数字 1~9 */
            int boxIndex = (i / 3) * 3 + j / 3; /* 宫编号 0~8 */

            /* 若当前数字已在对应行/列/宫出现过，返回 false */
            if (row[i][num] || col[j][num] || box[boxIndex][num]) {
                return false;
            }

            /* 标记已出现 */
            row[i][num]      = true;
            col[j][num]      = true;
            box[boxIndex][num] = true;
        }
    }
    return true;
}
