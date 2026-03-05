# include<stdio.h>

int main(){
    int n,W,V;
    scanf("%d %d %d",&n,&W,&V);
    int w[n],c[n],v[n];
    for(int i=0;i<n;i++){
        scanf("%d %d %d",&w[i],&c[i],&v[i]);
    }
    //准备工作做完了
    //开始三维动态规划
    /*
    思路：对于a[x][y][z],以z轴为物品序列，x轴为重量，y轴为体积
    那么a[x][y][z]的值就是a[x][y][z-1]与a[x-z.w][y-z.c][z-1]的较大值
    这样一个一个遍历a[x][y][z]，就能得到a[W][V][n]的值,即为题解
    */

}