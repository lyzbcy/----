/*
思路：
变形的01背包问题
对于a[x][y],y轴代表不同硬币，x轴代表不同金额
a[x][y]的值就是

*/

#include<stdio.h>

int main(){
    int v[20];
    int w[20];
    int tar;
    
    // 读取硬币面值
    if (fgets(line, sizeof(line), stdin)) {
        char *p = strtok(line, " \n");
        while (p) {
            v[n++] = atoi(p);
            p = strtok(NULL, " \n");
        }
    }
    
    // 读取硬币重量
    if (fgets(line, sizeof(line), stdin)) {
        int idx = 0;
        char *p = strtok(line, " \n");
        while (p) {
            w[idx++] = atoi(p);
            p = strtok(NULL, " \n");
        }
    }
    
    // 读取目标金额
    scanf("%d", &tar);

    //准备结束 开始01背包问题
}
