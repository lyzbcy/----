#include<stdio.h>
#include<stdlib.h>
int m,n;
int **a;
int min;
int count;
int y,x;
int min_count;

// 放置或撤销卫兵的覆盖：val=+1 放置，val=-1 撤销
void fangweibing(int val){
    a[y][x] += val;
    if(y > 0) a[y-1][x] += val;      // 上
    if(y < m-1) a[y+1][x] += val;    // 下
    if(x > 0) a[y][x-1] += val;      // 左
    if(x < n-1) a[y][x+1] += val;    // 右
}

void pailie(){
    if(count > min){
        return;
    }
    
    int x_cun = x;
    int y_cun = y;
    
    // 剪枝：如果上方格子没被覆盖，必须放卫兵
    if(y != 0){
        if(a[y-1][x] == 0){
            goto fangshibing;
        }
    }
    
    // 分支1：不放卫兵
    if(x == n-1){
        if(y == m-1){
            // 到达终点但不放卫兵，检查是否全覆盖
            for(int i = 0; i < m; i++){
                for(int j = 0; j < n; j++){
                    if(a[i][j] == 0) goto fangshibing; // 有未覆盖，必须回去放
                }
            }
            // 全覆盖了
            if(count < min){
                min = count;
                min_count = 1;
            }else if(count == min){
                min_count++;
            }
            goto fangshibing; // 继续尝试放卫兵的分支
        }
        y++;
        x = 0;
    }else{
        x++;
    }
    pailie();
    
    // 恢复位置
    x = x_cun;
    y = y_cun;

fangshibing:;
    // 分支2：放卫兵
    x = x_cun;
    y = y_cun;
    
    fangweibing(1);  // 放置
    count++;
    
    if(x == n-1 && y == m-1){
        // 到达终点
        // 检查是否全覆盖
        int all_covered = 1;
        for(int i = 0; i < m; i++){
            for(int j = 0; j < n; j++){
                if(a[i][j] == 0){
                    all_covered = 0;
                    break;
                }
            }
            if(!all_covered) break;
        }
        if(all_covered){
            if(count < min){
                min = count;
                min_count = 1;
            }else if(count == min){
                min_count++;
            }
        }
        // 回溯
        fangweibing(-1);
        count--;
        return;
    }
    
    // 移动到下一格
    if(x == n-1){
        y++;
        x = 0;
    }else{
        x++;
    }
    pailie();
    
    // 回溯
    x = x_cun;
    y = y_cun;
    fangweibing(-1);
    count--;
    return;
}

int main(){
    scanf("%d %d", &m, &n);
    
    if(m < 1 || n < 1){
        printf("0\n0\n");
        return 0;
    }
    
    a = (int**)malloc(m * sizeof(int*));
    for(int i = 0; i < m; i++){
        a[i] = (int*)malloc(n * sizeof(int));
        for(int j = 0; j < n; j++){
            a[i][j] = 0;
        }
    }
    
    min = m * n;
    count = 0;
    y = 0;
    x = 0;
    min_count = 0;
    
    pailie();
    printf("%d\n%d\n", min, min_count);
    
    for(int i = 0; i < m; i++){
        free(a[i]);
    }
    free(a);
    return 0;
}